from BaseClasses import ItemClassification
from ..Subclasses import PHItem
from .Addresses import *

"""backwards-compatible fallback for AP v0.6.2 and prior
Code idea from @eternalcode0s minish cap implementation
"""
try:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_deprioritized_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression_deprioritized
except AttributeError as e:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression

ITEMS_DATA = {
    #   "Item Name": {
    #   'classification': ItemClassification,   # classification category
    #   'address': int,                         # address in memory. not used if progressive
    #   'value': int,                           # value to set in memory, if incremental added else bitwise or
    #   'incremental': bool                     # true for positive, False for negative
    #   'progressive': list[tuple[int, int]]    # address, value for each progressive stage
    #   'size': int,                            # size in bytes
    #   'set_bit': list[tuple[int, int]],       # for setting additional bits on acquisition
    #   'give_ammo': list[int]                  # how much ammo to give for each progressive stage
    #   'ammo_address': int                     # address for ammo
    #   'progressive_overwrite':                # for setting progressive stages as overwrites instead of bitwise or.
    # used for ammo upgrades cause setting the upgrade to 3 rather than 1 or 2 creates a glitched ammo upgrade
    #   'id': int                               # item id. no longer generated automatically :(
    #   'ammo_address': int                     # address for ammo
    #   'dungeon': int                          # Stage id for items tied to specific dungeons, like small keys
    #   'dummy': bool                           # ignores all item writing operations. Used for big keys and abstracts
    #   'force_vanilla': bool                   # forces item to be in it's vanilla location, probably not used?
    #   'hint_on_receive': list[str]            # locations to hint if conditions are met
    #   'ship': int                             # ship id for ships
    #   'refill': str                      # progressive item to draw data from
    #   'treasure': bool                   # treasure item tag
    #   'backup_filler': bool              # if item can safely be classified as filler when the filler pool runs out
    #    },

    # ======= Regular Items==========

    # Link items
    "Sword (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x1), (PHAddr.inventory_5, 0x20)],
        "set_bit": [(PHAddr.inventory_1, 0x1), (PHAddr.sword_count, 1)],
        "id": 1,
        "model": 0x3,
        "ghost_model": True,  # gives the item manually
        "model_reset": True,  # Removes what the model gives. Having both solves the progressive problem
    },
    "Oshus' Sword": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x1,
        "ammo_address": PHAddr.sword_count,  # used to remove sword model
        "set_bit": [(PHAddr.sword_count, 1)],
        "id": 2,
        "model": 0x3
    },
    "Phantom Sword": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x20,
        "id": 3,
        "model": 0x3,
        "ghost_model": True,
        "model_reset": True,
    },
    "Shield": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x2,
        "id": 4,
        "model": 0x4,
    },
    "Boomerang": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x4,
        "set_bit": [(PHAddr.boomerang_bit, 0x1)],
        "id": 5,
        "inventory_id": 2,
        "model": 0xC,
    },
    "Bombs (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x10), (PHAddr.bomb_upgrades, 0x1), (PHAddr.bomb_upgrades, 0x2)],
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": PHAddr.bomb_count,
        "set_bit": [(PHAddr.inventory_1, 0x10)],
        "id": 6,
        "inventory_id": 4,
        "tags": ["progressive_overwrite"],
        "model": 0x29,
        "vanilla_model": [0x29, 0x7],
        "ghost_model": True,
        "model_reset": True
    },
    "Bombchus (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x80), (PHAddr.chu_upgrades, 0x1), (PHAddr.chu_upgrades, 0x2)],
        "give_ammo": [0xa, 0x14, 0x1e],
        "ammo_address": PHAddr.chu_count,
        "tags": ["progressive_overwrite"],
        "set_bit": [(PHAddr.inventory_1, 0x80)],
        "id": 7,
        "inventory_id": 7,
        "model": 0x2a,
        "vanilla_model": [0x2a, 0xE],
        "ghost_model": True,
        "model_reset": True
    },
    "Bow (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.inventory_1, 0x20), (PHAddr.quiver_upgrades, 0x1), (PHAddr.quiver_upgrades, 0x2)],
        "give_ammo": [0x14, 0x1e, 0x32],
        "ammo_address": PHAddr.arrow_count,
        "tags": ["progressive_overwrite"],
        "set_bit": [(PHAddr.inventory_1, 0x20)],
        "id": 8,
        "inventory_id": 5,
        "model": 0x28,
        "vanilla_model": [0x28, 0x8],
        "ghost_model": True,
        "model_reset": True
    },
    "Grappling Hook": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x40,
        "set_bit": [(PHAddr.grapple_bit, 0x1)],
        "id": 9,
        "inventory_id": 6,
        "model": 0x20,
    },
    "Shovel": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_1,
        "value": 0x8,
        "set_bit": [(PHAddr.shovel_bit, 0x1)],
        "id": 10,
        "inventory_id": 3,
        "model": 0xd,
    },
    "Hammer": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_2,
        "value": 0x1,
        "set_bit": [(PHAddr.hammer_bit, 0x1)],
        "id": 11,
        "inventory_id": 8,
        "model": 0x1f,
    },

    # Spirits
    "Spirit of Power (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x20), (PHAddr.fairies_1, 0x1), (PHAddr.fairies_1, 0x8)],
        "id": 12,
        "model": 0x2d,
        "model_reset": True,
        "ghost_model": True,
    },
    "Spirit of Wisdom (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x40), (PHAddr.fairies_1, 0x2), (PHAddr.fairies_1, 0x10)],
        "id": 13,
        "model": 0x2e,
        "model_reset": True,
        "ghost_model": True,
    },
    "Spirit of Courage (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.fairies_0, 0x10), (PHAddr.fairies_0, 0x80), (PHAddr.fairies_1, 0x4)],
        "id": 14,
        "model": 0x2F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Spirit of Courage (White)": {  # Used to remove spirit from Temple of Courage
        "classification": ItemClassification.progression,
        "address": PHAddr.fairies_1,
        "value": 0x20,
        "id": 15,
    },

    # Upgrades
    "Heart Container": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.heart_containers,
        "value": 0x4,
        "tags": ["monotone_incremental"],
        "base_count": 12,
        "size": 2,
        "id": 16,
        "model": 0xa,
    },
    "Phantom Hourglass": {
        "classification": ItemClassification.progression,
        "address": PHAddr.phantom_hourglass_max,
        "value": "Sand PH",
        "tags": ["monotone_incremental"],
        "size": 4,
        "id": 17,
    },
    "Sand of Hours (Boss)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": 0x1c20,
        "tags": ["monotone_incremental", "backup_filler"],
        "size": 4,
        "id": 18,
        "model": 0x78,
        "ghost_model": True,
    },
    "Sand of Hours (Small)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": 0xe10,
        "tags": ["monotone_incremental", "backup_filler"],
        "size": 4,
        "id": 19,
        "model": 0x78,
        "ghost_model": True,
    },
    "Sand of Hours": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.phantom_hourglass_max,
        "value": "Sand",
        "tags": ["monotone_incremental"],
        "size": 4,
        "id": 20,
        "model": 0x78,
        "ghost_model": True,
        "model_reset": "Sand of Hours (Small)"
    },
    "Swordsman's Scroll": {
        "classification": ItemClassification.useful,
        "address": PHAddr.inventory_6,
        "value": 0x20,
        "id": 21,
        "model": 0x71,
    },

    # Ship Items
    "Cannon": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_cannon,
        "value": 0x1,
        "id": 22,
        "model": 0x25,
        "ghost_model": True,
        "blocked_scenes": [0x130B]
    },
    "Salvage Arm": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x10,
        "id": 23,
        "model": 0x3D,
        "ghost_model": True,
        "blocked_scenes": [0x130B]
    },
    "Fishing Rod": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x1,
        "id": 24,
        "model": 0x24,
        "ghost_model": True,
    },
    "Big Catch Lure": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x80,
        "id": 25,
        "model": 0x80,
        "ghost_model": True,
    },
    "Swordfish Shadows": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_43,
        "value": 0x10,
        "id": 26,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Cyclone Slate": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x40,
        "id": 27,
        "model": 0x7F,
        "ghost_model": True,
    },

    # Sea Charts
    "SW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x2,
        "id": 28,
        "disconnect_entrances": [
            "Ocean SW Mercay",
            "Ocean SW Cannon",
            "Ocean SW Ember",
            "Ocean SW Molida",
            "Ocean SW Spirit",
        ],
        "model": 0x13,
    },
    "NW Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x4,
        "id": 29,
        "disconnect_entrances": [
            "Ocean NW Gust",
            "Ocean NW Bannan",
            "Ocean NW Zauz",
            "Ocean NW Uncharted",
            "Ocean NW Board Ghost Ship",
        ],
        "model": 0x14,
    },
    "SE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x8,
        "set_bit": [(PHAddr.adv_flags_1, 0x8)],
        "id": 30,
        "disconnect_entrances": [
            "Ocean SE Goron",
            "Ocean SE Harrow",
            "Ocean SE Dee Ess",
            "Ocean SE Frost",
        ],
        "model": 0x15,
    },
    "NE Sea Chart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x10,
        "id": 31,
        "disconnect_entrances": [
            "Ocean NE IotD",
            "Ocean NE Ruins",
            "Ocean NE Maze",
        ],
        "model": 0x16,
    },
    # Spirit gems
    "Power Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.power_gem_count,
        "value": 0x1,
        "tags": ["incremental"],
        "id": 32,
        "model": 0x2D
    },
    "Wisdom Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.wisdom_gem_count,
        "value": 0x1,
        "tags": ["incremental"],
        "id": 33,
        "model": 0x2E
    },
    "Courage Gem": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.courage_gem_count,
        "value": 0x1,
        "tags": ["incremental"],
        "id": 34,
        "model": 0x2F
    },
    "Power Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.power_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 35,
        "model": 0x2D,
        "ghost_model": True,
        "model_reset": True
    },
    "Wisdom Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.wisdom_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 36,
        "model": 0x2E,
        "ghost_model": True,
        "model_reset": True
    },
    "Courage Gem Pack": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.courage_gem_count,
        "value": "pack_size",
        "tags": ["monotone_incremental"],
        "id": 37,
        "model": 0x2F,
        "ghost_model": True,
        "model_reset": True
    },

    # Rupees and filler
    "Green Rupee (1)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 2,
        "id": 38,
        "model": 0x2,
    },
    "Blue Rupee (5)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x5,
        "tags": ["incremental"],
        "size": 2,
        "id": 39,
        "model": 0x18,
    },
    "Red Rupee (20)": {
        "classification": ItemClassification.filler,
        "address": PHAddr.rupee_count,
        "value": 0x14,
        "tags": ["incremental"],
        "size": 2,
        "id": 40,
        "model": 0x19,
    },
    "Big Green Rupee (100)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0x64,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 41,
        "model": 0x9,
    },
    "Big Red Rupee (200)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0xc8,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 42,
        "model": 0x1a,
    },
    "Gold Rupee (300)": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.rupee_count,
        "value": 0x12c,
        "tags": ["incremental", "backup_filler"],
        "size": 2,
        "id": 43,
        "model": 0x1b,
    },
    "Rupoor (-10)": {
        "classification": ItemClassification.trap,
        "address": PHAddr.rupee_count,
        "value": -0xa,
        "tags": ["incremental"],
        "size": 2,
        "id": 44,
        "model": 0x81,
    },
    "Big Rupoor (-50)": {
        "classification": ItemClassification.trap,
        "address": PHAddr.rupee_count,
        "value": -0x32,
        "tags": ["incremental"],
        "size": 2,
        "id": 45,
        "model": 0x82,
    },
    "Pre-Alpha Rupee (5000)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.rupee_count,
        "value": 0x1388,
        "tags": ["incremental"],
        "size": 2,
        "id": 46,
    },
    "Treasure": {
        "classification": ItemClassification.filler,
        "tags": ["incremental"],
        "id": 47,
        "vanilla_model": [0x7D, 0x86]
    },
    "Ship Part": {
        "classification": ItemClassification.filler,
        "tags": ["ship_part"],
        "id": 48,
        "vanilla_model": [0x7E, 0x85]
    },
    "Potion": {
        "classification": ItemClassification.filler,
        "id": 49,
    },
    "Red Potion": {
        "classification": ItemClassification.filler,
        "value": 1,
        "id": 50,
        "overflow_item": "Big Green Rupee (100)",
        "model": 0x75,
    },
    "Purple Potion": {
        "classification": ItemClassification.filler,
        "value": 2,
        "id": 51,
        "overflow_item": "Big Green Rupee (100)",
        "model": 0x76,
    },
    "Yellow Potion": {
        "classification": ItemClassification.filler,
        "value": 3,
        "id": 52,
        "overflow_item": "Big Red Rupee (200)",
        "model": 0x77,
    },
    "Nothing!": {
        "classification": ItemClassification.filler,
        "dummy": True,
        "id": 53,
        "model": 0x0,
    },
    "Refill: Bombs": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": PHAddr.bomb_count,
        "refill": "Bombs (Progressive)",
        "id": 54,
        "model": 0x7,
        "model_reset": True
    },
    "Refill: Arrows": {
        "classification": ItemClassification.filler,
        "give_ammo": [0x14, 0x1e, 0x32],
        "address": PHAddr.arrow_count,
        "refill": "Bow (Progressive)",
        "id": 55,
        "model": 0x8,
        "model_reset": True
    },
    "Refill: Bombchus": {
        "classification": ItemClassification.filler,
        "give_ammo": [0xa, 0x14, 0x1e],
        "address": PHAddr.chu_count,
        "refill": "Bombchus (Progressive)",
        "id": 56,
        "model": 0xE,
        "model_reset": True
    },
    "Salvage Repair Kit": {
        "classification": ItemClassification.filler,
        "address": PHAddr.custom_storage,
        "value": 0x20,
        "tags": ["incremental"],
        "id": 57,
        "max": 0xFF,
        "model": 0x3D,
        "ghost_model": True,
        "model_reset": True
    },
    "Refill: Health": {
        "classification": ItemClassification.filler,
        "value": "full_heal",
        "id": 193,
    },

    # Treasure
    "Treasure: Pink Coral": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.pink_coral_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 58,
        "model": 0x30,
        "ghost_model": True,
    },
    "Treasure: White Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.wpl_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 59,
        "model": 0x31,
        "ghost_model": True,
    },
    "Treasure: Dark Pearl Loop": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.dpl_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 60,
        "model": 0x32,
        "ghost_model": True,
    },
    "Treasure: Zora Scale": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.zora_scale_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 61,
        "model": 0x33,
        "ghost_model": True,
    },
    "Treasure: Goron Amber": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.goron_amber_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 62,
        "model": 0x34,
        "ghost_model": True,
    },
    "Treasure: Ruto Crown": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.ruto_crown_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 63,
        "model": 0x35,
        "ghost_model": True,
    },
    "Treasure: Helmaroc Plume": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.roc_feather_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 64,
        "model": 0x36,
        "ghost_model": True,
    },
    "Treasure: Regal Ring": {
        "classification": DEPRIORITIZED_SKIP_BALANCING_FALLBACK,
        "address": PHAddr.regal_ring_count,
        "tags": ["incremental", "treasure", "backup_filler"],
        "id": 65,
        "model": 0x37,
        "ghost_model": True,
    },

    # Salvage
    "Courage Crest": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_16,
        "value": 0x4,
        "set_bit": [(PHAddr.treasure_maps_0, 0x1)],
        "id": 66,
        "model": 0x2F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Treasure Map #1 (Molida SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x80,
        "id": 67,
        "hint_on_receive": ["Ocean SW Salvage #1 Molida SW"],
        "model": 0x52
    },
    "Treasure Map #2 (Mercay NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x10,
        "id": 68,
        "hint_on_receive": ["Ocean SW Salvage #2 Mercay NE"],
        "model": 0x4F
    },
    "Treasure Map #3 (Gusts SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x20,
        "id": 69,
        "hint_on_receive": ["Ocean NW Salvage #3 Gusts SW"],
        "model": 0x58
    },
    "Treasure Map #4 (Bannan SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x80,
        "id": 70,
        "hint_on_receive": ["Ocean NW Salvage #4 Bannan SE"],
        "model": 0x5a
    },
    "Treasure Map #5 (Molida N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x40,
        "id": 71,
        "hint_on_receive": ["Ocean SW Salvage #5 Molida N"],
        "model": 0x51
    },
    "Treasure Map #6 (Bannan W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x1,
        "id": 72,
        "hint_on_receive": ["Ocean NW Salvage #6 Bannan W"],
        "model": 0x53
    },
    "Treasure Map #7 (Gusts E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x8,
        "id": 73,
        "hint_on_receive": ["Ocean NW Salvage #7 Gusts E"],
        "model": 0x56
    },
    "Treasure Map #8 (Mercay SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x8,
        "id": 74,
        "hint_on_receive": ["Ocean SW Salvage #8 Mercay SE"],
        "model": 0x4E
    },
    "Treasure Map #9 (Cannon W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x2,
        "id": 75,
        "hint_on_receive": ["Ocean SW Salvage #9 Cannon W"],
        "model": 0x4C,
        "blocked_scenes": [0xb03]
    },
    "Treasure Map #10 (Gusts SE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x10,
        "id": 76,
        "hint_on_receive": ["Ocean NW Salvage #10 Gusts SE"],
        "model": 0x57
    },
    "Treasure Map #11 (Gusts N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x2,
        "id": 77,
        "hint_on_receive": ["Ocean NW Salvage #11 Gusts N"],
        "model": 0x54
    },
    "Treasure Map #12 (Dee Ess N)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x20,
        "id": 78,
        "hint_on_receive": ["Ocean SE Salvage #12 Dee Ess N"],
        "model": 0x60
    },
    "Treasure Map #13 (Harrow E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x4,
        "id": 79,
        "hint_on_receive": ["Ocean SE Salvage #13 Harrow E"],
        "model": 0x5d
    },
    "Treasure Map #14 (Goron NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x1,
        "id": 80,
        "hint_on_receive": ["Ocean SE Salvage #14 Goron NW"],
        "model": 0x5b,
        "blocked_scenes": [0x1800]
    },
    "Treasure Map #15 (Goron W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x2,
        "id": 81,
        "hint_on_receive": ["Ocean SE Salvage #15 Goron W"],
        "model": 0x5c,
        "blocked_scenes": [0x1800]
    },
    "Treasure Map #16 (Goron NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x10,
        "id": 82,
        "hint_on_receive": ["Ocean SE Salvage #16 Goron NE"],
        "model": 0x5f
    },
    "Treasure Map #17 (Frost S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x40,
        "id": 83,
        "hint_on_receive": ["Ocean SE Salvage #17 Frost S"],
        "model": 0x61
    },
    "Treasure Map #18 (Cannon S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x4,
        "id": 84,
        "hint_on_receive": ["Ocean SW Salvage #18 Cannon S"],
        "model": 0x4D
    },
    "Treasure Map #19 (Gusts NE)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x4,
        "id": 85,
        "hint_on_receive": ["Ocean NW Salvage #19 Gusts NE"],
        "model": 0x55
    },
    "Treasure Map #20 (Bannan E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_1,
        "value": 0x40,
        "id": 86,
        "hint_on_receive": ["Ocean NW Salvage #20 Bannan E"],
        "model": 0x59
    },
    "Treasure Map #21 (Molida NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_0,
        "value": 0x20,
        "id": 87,
        "hint_on_receive": ["Ocean SW Salvage #21 Molida NW"],
        "model": 0x50

    },
    "Treasure Map #22 (Harrow S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x8,
        "id": 88,
        "hint_on_receive": ["Ocean SE Salvage #22 Harrow S"],
        "model": 0x5e,
        "blocked_scenes": [0x1400]
    },
    "Treasure Map #23 (Frost NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_2,
        "value": 0x80,
        "id": 89,
        "hint_on_receive": ["Ocean SE Salvage #23 Frost NW"],
        "model": 0x62
    },
    "Treasure Map #24 (Ruins W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x20,
        "id": 90,
        "hint_on_receive": ["Ocean NE Salvage #24 Ruins W"],
        "model": 0x68
    },
    "Treasure Map #25 (Dead E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x4,
        "id": 91,
        "hint_on_receive": ["Ocean NE Salvage #25 Dead E"],
        "model": 0x65,
        "blocked_scenes": [0x1800]
    },
    "Treasure Map #26 (Ruins SW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x2,
        "id": 92,
        "hint_on_receive": ["Ocean NE Salvage #26 Ruins SW"],
        "model": 0x64,
        "blocked_scenes": [0x1800]
    },
    "Treasure Map #27 (Maze E)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x8,
        "id": 93,
        "hint_on_receive": ["Ocean NE Salvage #27 Maze E"],
        "model": 0x66
    },
    "Treasure Map #28 (Ruins NW)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x1,
        "id": 94,
        "hint_on_receive": ["Ocean NE Salvage #28 Ruins NW"],
        "model": 0x63
    },
    "Treasure Map #29 (Maze W)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x10,
        "id": 95,
        "hint_on_receive": ["Ocean NE Salvage #29 Maze W"],
        "model": 0x67
    },
    "Treasure Map #30 (Ruins S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x40,
        "id": 96,
        "hint_on_receive": ["Ocean NE Salvage #30 Ruins S"],
        "model": 0x69
    },
    "Treasure Map #31 (Dead S)": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.treasure_maps_3,
        "value": 0x80,
        "id": 97,
        "hint_on_receive": ["Ocean NE Salvage #31 Dead S"],
        "model": 0x6a
    },

    # Keys
    "Small Key (Mountain Passage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x27,
        "tags": ["incremental"],
        "id": 98,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x25,
        "tags": ["incremental", "always_process"],
        "id": 99,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1c,
        "tags": ["incremental"],
        "id": 100,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "tags": ["incremental"],
        "id": 101,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "tags": ["incremental"],
        "id": 102,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1f,
        "tags": ["incremental"],
        "id": 103,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Small Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x21,
        "tags": ["incremental"],
        "id": 104,
        "model": 0x5,
        "vanilla_model": 0x1,
        "ghost_model": True,
    },
    "Boss Key (Temple of Fire)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1c,
        "id": 105,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Boss Key (Temple of Wind)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1d,
        "id": 106,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Boss Key (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "id": 107,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Boss Key (Goron Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x20,
        "id": 108,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Boss Key (Temple of Ice)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1f,
        "id": 109,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Boss Key (Mutoh's Temple)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x21,
        "id": 110,
        "tags": ["always_process"],
        "model": 0xf,
        "model_reset": True,
    },
    "Square Crystal (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "dungeon": 0x1e,
        "tags": ["always_process"],
        "id": 111,
        "set_bit_in_room": {0x1E00: [(PHAddr.toc_crystal_state, 0x10),
                                     ("stage_flag", 0x80)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Square Pedestal North (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x1e,
        "id": 194,
        "set_bit_in_room": {0x1E00: [(PHAddr.toc_crystal_state, 0x10)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Square Pedestal South (Temple of Courage)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x1e,
        "id": 195,
        "set_bit_in_room": {0x1E00: [("stage_flag", 0x80)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Triangle Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x29,
        "id": 112,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 8])]},
        "model": 0x23,
        "model_reset": True,
    },
    "Round Crystal (Ghost Ship)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x29,
        "id": 113,
        "set_bit_in_room": {0x2900: [("stage_flag", [0, 0, 0, 2])]},
        "model": 0x22,
        "model_reset": True,
    },
    "Round Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 114,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)],  # format: dict[room, list[tuple[addr, value, *dict(extra data)]]]
                            0x250C: [(PHAddr.totok_b9_state, 0x4)]},
        "model": 0x22,
        "model_reset": True,
    },
    "Round Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 196,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)]},
        "model": 0x22,
        "model_reset": True,
    },
    "Round Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 197,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x4)]},
        "model": 0x22,
        "model_reset": True,
    },
    "Round Crystals": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 204,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x2)],
                            0x250C: [(PHAddr.totok_b9_state, 0x4)],
                            0x2900: [("stage_flag", [0, 0, 0, 2])]},
        "model": 0x22,
        "model_reset": True,
    },
    "Triangle Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 115,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)],
                            0x250C: [(PHAddr.totok_b9_state, 0x8)]},
        "model": 0x23,
        "model_reset": True,
    },
    "Triangle Pedestal B8 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 198,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)]},
        "model": 0x23,
        "model_reset": True,
    },
    "Triangle Pedestal B9 (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 199,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x8)]},
        "model": 0x23,
        "model_reset": True,
    },
    "Triangle Crystals": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": True,
        "id": 203,
        "set_bit_in_room": {0x250B: [(PHAddr.totok_b8_state, 0x4)],
                            0x250C: [(PHAddr.totok_b9_state, 0x8)],
                            0x2900: [("stage_flag", [0, 8])]},
        "model": 0x23,
        "model_reset": True,
    },
    "Square Crystal (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 116,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x22)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Square Pedestal West (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 200,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x20)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Square Pedestal Center (Temple of the Ocean King)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 201,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x2)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Square Crystals": {
        "classification": ItemClassification.progression,
        "dungeon": True,
        "tags": ["always_process"],
        "id": 202,
        "set_bit_in_room": {0x250C: [(PHAddr.totok_b9_state, 0x22)],
                            0x1E00: [(PHAddr.toc_crystal_state, 0x10),
                                     ("stage_flag", 0x80)]},
        "model": 0x21,
        "model_reset": True,
    },
    "Force Gem (B3)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 117,
        "set_bit_in_room": {0x2503: [(PHAddr.totok_b3_state, 0xFE, {"count": 3}),
                                     (PHAddr.totok_b3_state_1, 0xF, {"count": 3})]},
        "model": 0x6,
        "model_reset": True,
    },
    "Force Gem (B12)": {
        "classification": ItemClassification.progression,
        "tags": ["always_process"],
        "dungeon": 0x25,
        "id": 118,
        "set_bit_in_room": {0x2510: [(PHAddr.totok_b12_state, 0xFE, {"count": 3}),
                                     (PHAddr.totok_b12_state_1, 0xF, {"count": 3}),
                                     (PHAddr.totok_b12_state, 0xC, {"count": 2}),
                                     (PHAddr.totok_b12_state, 0x4, {"count": 1})]},
        "model": 0x6,
        "model_reset": True,
    },
    "Force Gems": {
        "classification": ItemClassification.progression,
        "id": 205,
        "tags": ["always_process"],
        "set_bit_in_room": {0x2503: [(PHAddr.totok_b3_state, 0xFE),
                                     (PHAddr.totok_b3_state_1, 0xF)],
                            0x2510: [(PHAddr.totok_b12_state, 0xFE),
                                     (PHAddr.totok_b12_state_1, 0xF)]},
        "model": 0x6,
        "model_reset": True,
    },
    "Triforce Crest": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_4,
        "value": 0x2,
        "id": 119,
        "model": 0x1C,
    },
    "Sun Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_5,
        "value": 0x40,
        "id": 120,
        "model": 0x26,
    },
    "Ghost Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x8,
        "id": 121,
        "model": 0x38,
    },
    "King's Key": {
        "classification": ItemClassification.progression,
        "address": PHAddr.inventory_6,
        "value": 0x4,
        "id": 122,
        "model": 0x2c,
    },
    "Regal Necklace": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_6,
        "value": 0x8,
        "id": 123,
        "model": 0x3c,
        "ghost_model": True,
    },

    # Metals
    "Crimzonine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
        "value": 0x40,
        "id": 124,
        "model": 0x72,
        "blocked_scenes": [0x100a]
    },
    "Azurine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
        "value": 0x20,
        "id": 125,
        "model": 0x73,
    },
    "Aquanine": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_metals,
        "value": 0x80,
        "id": 126,
        "model": 0x74,
    },
    "Rare Metal": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 127,
        "model": 0x74,
        "model_reset": True
    },
    "Additional Rare Metal": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 128,
        "model": 0x74,
        "model_reset": True
    },
    "Verdanine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 129,
        "model": 0x74,
        "model_reset": True
    },
    "Lavendine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 130,
        "model": 0x73,
        "model_reset": True
    },
    "Amberine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 131,
        "model": 0x72,
        "model_reset": True
    },
    "Vermilline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 132,
        "model": 0x72,
        "model_reset": True
    },
    "Burgundine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 133,
        "model": 0x72,
        "model_reset": True
    },
    "Crystaline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 134,
        "model": 0x73,
        "model_reset": True
    },
    "Carrotine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 135,
        "model": 0x72,
        "model_reset": True
    },
    "Olivine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 136,
        "model": 0x74,
        "model_reset": True
    },
    "Chartreusine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 137,
        "model": 0x74,
        "model_reset": True
    },
    "Violetine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 138,
        "model": 0x73,
        "model_reset": True
    },
    "Ceruline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 139,
        "model": 0x73,
        "model_reset": True
    },
    "Fuchsianine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 140,
        "model": 0x72,
        "model_reset": True
    },
    "Saffrine": {  # oops duplicate
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 141,
        "model": 0x72,
        "model_reset": True
    },
    "Sepianine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 142,
        "model": 0x72,
        "model_reset": True
    },
    "Apricotine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 143,
        "model": 0x72,
        "model_reset": True
    },
    "Scarletine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 144,
        "model": 0x72,
        "model_reset": True
    },
    "Coraline": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 145,
        "model": 0x72,
        "model_reset": True
    },
    "Magentine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 146,
        "model": 0x72,
        "model_reset": True
    },
    "Cyanine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 147,
        "model": 0x73,
        "model_reset": True
    },
    "Mauvine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 148,
        "model": 0x73,
        "model_reset": True
    },
    "Indigorine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 149,
        "model": 0x73,
        "model_reset": True
    },
    "Junipine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 150,
        "model": 0x72,
        "model_reset": True
    },
    "Viridine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 151,
        "model": 0x74,
        "model_reset": True
    },
    "Limeinine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 152,
        "model": 0x74,
        "model_reset": True
    },
    "Mintine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 153,
        "model": 0x74,
        "model_reset": True
    },
    "Umberine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 154,
        "model": 0x74,
        "model_reset": True
    },
    "Lilacine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 155,
        "model": 0x73,
        "model_reset": True
    },
    "Saffronine": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 156,
        "model": 0x72,
        "model_reset": True
    },

    # Trade Quest
    "Hero's New Clothes": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x4,
        "id": 157,
        "model": 0x3e,
        "ghost_model": True,
        "blocked_scenes": [0x600]
    },
    "Kaleidoscope": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x8,
        "id": 158,
        "model": 0x3f,
        "ghost_model": True,
        "blocked_scenes": [0x700]
    },
    "Guard Notebook": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x10,
        "id": 159,
        "model": 0x40,
        "ghost_model": True,
        "blocked_scenes": [0x900]
    },
    "Wood Heart": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x80,
        "id": 160,
        "model": 0x43,
        "ghost_model": True,
        "blocked_scenes": [0xa00]
    },
    "Phantom Blade": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_22,
        "value": 0x20,
        "id": 161,
        "model": 0x44,
        "ghost_model": True,
        "blocked_scenes": [0x160A]
    },

    # Letters and cards
    "Freebie Card": {
        "classification": DEPRIORITIZED_FALLBACK,
        "address": PHAddr.adv_flags_14,
        "value": 0x40,
        "id": 162,
        "tags": ["backup_filler"],
        "model": 0x39,
        "ghost_model": True,
    },
    "Member's Card (Progressive)": {
        "classification": ItemClassification.progression,
        "progressive": [(PHAddr.adv_flags_12, 0x40), (PHAddr.adv_flags_18, 0x20), (PHAddr.adv_flags_18, 0x40), (PHAddr.adv_flags_18, 0x80), (PHAddr.adv_flags_19, 0x1)],
        "id": 163,
        "model": 0x3a,
        "ghost_model": True,
    },
    "Complimentary Card": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_14,
        "value": 0x20,
        "id": 164,
        "model": 0x3b,
        "ghost_model": True,
    },
    "Compliment Card": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_14,
        "value": 0x80,
        "id": 190,
        "model": 0x3a,
        "ghost_model": True,
    },
    "Jolene's Letter": {
        "classification": ItemClassification.progression,
        "address": PHAddr.flags_trade_quest,
        "value": 0x20,
        "id": 165,
        "model": 0x41,
        "ghost_model": True,
    },
    "Prize Postcard": {
        "classification": ItemClassification.filler,
        "address": PHAddr.adv_flags_19,
        "value": 0x8,
        "id": 166,
        "model": 0x42,
        "ghost_model": True,
    },
    "Beedle Points (10)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "tags": ["incremental"],
        "value": 10,
        "id": 167,
        "model": 0x39,
        "ghost_model": True,
    },
    "Beedle Points (20)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "value": 20,
        "tags": ["incremental"],
        "id": 191,
        "model": 0x39,
        "ghost_model": True,
    },
    "Beedle Points (50)": {
        "classification": ItemClassification.progression,
        "address": PHAddr.beedle_points,
        "value": 50,
        "tags": ["incremental"],
        "id": 192,
        "model": 0x39,
        "ghost_model": True,
    },

    # Frogs
    "Golden Frog Glyph X": {
        "classification": ItemClassification.progression,
        "address": PHAddr.adv_flags_38,
        "value": 0x80,
        "id": 168,
        "model": 0x7F,
        "ghost_model": True,
        "model_reset": True,
    },
    "Golden Frog Glyph Phi": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x1,
        "id": 169,
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Golden Frog Glyph N": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x2,
        "id": 170,
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Golden Frog Glyph Omega": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x4,
        "id": 171,
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Golden Frog Glyph W": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x8,
        "id": 172,
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Golden Frog Glyph Square": {
        "classification": ItemClassification.progression,
        "address": PHAddr.frog_glyphs,
        "value": 0x10,
        "id": 173,
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },

    # Ships
    "Ship: SS Linebeck": {
        "classification": ItemClassification.filler,
        "id": 174,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Bright Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x1,
        "id": 175,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Iron Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x2,
        "id": 176,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Stone Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x3,
        "id": 177,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Vintage Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x4,
        "id": 178,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Demon Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x5,
        "id": 179,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Tropical Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x6,
        "id": 180,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Dignified Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x7,
        "id": 181,
        "model": 0x25,
        "ghost_model": True,
    },
    "Ship: Golden Ship": {
        "classification": ItemClassification.useful,
        "tags": ["backup_filler"],
        "ship": 0x8,
        "id": 182,
        "model": 0x7B,
        "ghost_model": True,
    },

    # Fish
    "Fish: Skippyjack": {
        "classification": ItemClassification.filler,
        "address": PHAddr.skippyjack_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 183,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Fish: Toona": {
        "classification": ItemClassification.filler,
        "address": PHAddr.toona_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 184,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Fish: Loovar": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.loovar_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 185,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Fish: Rusty Swordfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.rsf_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 186,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Fish: Legendary Neptoona": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.neptoona_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 187,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "Fish: Stowfish": {
        "classification": ItemClassification.progression_skip_balancing,
        "address": PHAddr.stowfish_count,
        "value": 0x1,
        "tags": ["incremental"],
        "size": 1,
        "id": 188,
        "model": 0x80,
        "ghost_model": True,
        "model_reset": True
    },
    "_UT_Glitched_Logic": {
        "classification": ItemClassification.progression,
        "dummy": True,
        "id": 189,
    },
    "Map Warp: Mercay": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 206,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Cannon": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 207,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Ember": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 208,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Molida": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 209,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Spirit": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 210,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Gust": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 211,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Bannan": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 212,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Uncharted": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 213,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Zauz": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 214,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Goron": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 215,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Frost": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 216,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Harrow": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 217,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Dee Ess": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 218,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Isle of the Dead": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 219,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Ruins": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 220,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
    "Map Warp: Maze": {
        "classification": ItemClassification.useful,
        "dummy": True,
        "id": 221,
        "tags": ["backup_filler"],
        "model": 0x7F,
        "model_reset": True,
        "ghost_model": True,
    },
}
ITEMS: dict[str, "PHItem"] = dict()
item_id_to_name_dict: dict[int, str] = dict()

id_check = []
for name, data in ITEMS_DATA.items():
    if data["id"] in id_check:
        raise f"Duplicate ID Detected: {data['id']}"
    id_check.append(data["id"])
    item_id_to_name_dict[data["id"]] = name
    ITEMS[name] = PHItem(name, data, ITEMS)

# IDs are now fixed!!!
"""for i, k in enumerate(ITEMS_DATA):
    ITEMS_DATA[k]["id"] = i+1"""

# bulk data editing / export
if __name__ == "__main__":
    attributes = set()
    for name, data in ITEMS_DATA.items():
        for attribute in data:
            attributes.add(attribute)
    for attribute in attributes:
        print(f"self.{attribute}: ")
"""
    keys = set()
    for name, data in ITEMS_DATA.items():
        for key in data:
            keys.add(key)
    for i in keys:
        print(i)
    # print(f"\t\"{name}\": " + "{")
"""
"""
        for key, value in data.items():
            if type(value) is str:
                print(f"\t\t\"{key}\": \"{value}\",")
            elif key == "classification":
                print(f"\t\t\"{key}\": ItemClassification.{CLASSIFICATION[value]},")
            elif type(value) is int:
                if key in ["id", "size"]:
                    print(f"\t\t\"{key}\": {value},")
                else:
                    print(f"\t\t\"{key}\": {hex(value)},")
            elif type(value) is list:
                l_print = "["
                for i in value:
                    if type(i) is tuple or type(i) is list:
                        l_print += "("
                        for j in i:
                            if type(j) is int:
                                l_print += f"{hex(j)}, "
                            elif type(j) is str:
                                l_print += f"\"{j}\", "
                            else:
                                l_print += f"{j}, "
                        l_print = l_print[:-2]
                        l_print += "), "
                    else:
                        if type(i) is int:
                            l_print += f"{hex(i)}, "
                        elif type(i) is str:
                            l_print += f"\"{i}\", "
                        else:
                            l_print += f"{i}, "
                l_print = l_print[:-2]
                l_print += "]"
                print(f"\t\t\"{key}\": {l_print},")
            else:
                print(f"\t\t\"{key}\": {value},")
        print("\t},")
"""
