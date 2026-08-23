from BaseClasses import LocationProgressType
from test.bases import *

options_old = {
        "rabbitsanity": "unique_checks",
        "rabbit_max_location_count": 1,
        "rabbit_location_count_distribution": "for_each",
        "rabbit_pack_size": 3,
        "rabbit_extra_items": 0,
        "goal": "beat_tos_section_6",
        "dark_realm_access": "both",

        "dungeons_required": 12,
        "tos_dungeon_options": "all_sections",

        "randomize_tears": "in_own_section",
        "tear_size": "large",
        "tear_sections": "unique_sections",
        "spirit_weapons": "final_tear",
        "shuffle_tos_sections": "no_shuffle",
        "exclude_sections": "remove",
        "plando_dungeon_pool": {},

        "keysanity": "vanilla",
        "randomize_boss_keys": "anywhere",
        "keyrings": "all",


        "shopsanity": {"all"},
        "rupee_farming_logic": "unlimited_farming",
        "excess_random_treasure": "nothing",
        "logic": "glitched",
        "randomize_passengers": "randomize",
        "randomize_cargo": "randomize",
        "randomize_stamps": "vanilla_with_location",
        "stamp_pack_sizes": 1,
        "randomize_minigames": "hard",
        "exclude_dungeons": "remove",

        "track_pool": "mixed_small",
        "start_with_train": True,
        "cannon_logic": "train_requires_cannon",
        "portal_behavior": "always_open",
        "start_inventory_from_pool": {
            "Wagon": 1,
            "Stamp Book": 1
        },
        "start_inventory": {
            "Completed Forest Glyph": 1,
            "Completed Snow Glyph": 1,
            "Completed Ocean Glyph": 1,
            "Completed Fire Glyph": 1,
        }
    }

compass_options = {
    "dark_realm_access": "both",
}

er_options = {
        "progressive_equipment": False,
        "randomize_shields": False,

        "shuffle_stations": "no_shuffle",
        "shuffle_train_transitions": "no_shuffle",

        "shuffle_caves": "no_shuffle",
        "shuffle_houses": "no_shuffle",

        "shuffle_hyrule_castle": "no_shuffle",
        "shuffle_eote": "no_shuffle",
        "shuffle_disorientation": "no_shuffle",

        "shuffle_tos_sections": "no_shuffle",
        "shuffle_tos_staircase": "no_shuffle",

        "shuffle_dungeon_entrances": "no_shuffle",
        "shuffle_bosses": "no_shuffle",
        "shuffle_dungeon_rooms": "no_shuffle",
        "shuffle_warps": "no_shuffle",

        "shuffle_portals": "shuffle_alone",
        "shuffle_las": "no_shuffle",

        "keyrings": "all",
        "dungeons_required": 5,
        "exclude_dungeons": "remove",

        "entrance_directionality": {},

        "randomize_start": {"niko"},
        "start_with_train": True,
        "free_starting_items": 2,

        "rabbitsanity": "both",

        "randomize_passengers": "vanilla",
        "randomize_cargo": "vanilla",
        "passenger_pickup": "visit"

        # "plando_transitions": [
        #     {"entrance": "Outset East House",
        #      "exit": "Tower of Spirits to Forest Realm"},
        #     {"entrance": "Anouki Village SW House",
        #      "exit": "Kofu's New House Exit"}
        # ]
    }

basic = {
        "start_with_train": True
}

class TestGeneration(WorldTestBase):
    game = "Spirit Tracks"
    options = basic