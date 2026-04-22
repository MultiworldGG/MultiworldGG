from BaseClasses import LocationProgressType
from test.bases import *


class TestGeneration(WorldTestBase):
    game = "Spirit Tracks"
    options = {
        "rabbitsanity": "unique_checks",
        "rabbit_max_location_count": 10,
        # "rabbit_location_count_distribution": "random_mixed",
        "rabbit_pack_size": "random_mixed",
        "rabbit_extra_items": 2,
        "goal": "beat_tos_section_6",
        "dark_realm_access": "both",

        "dungeons_required": 12,
        "tos_dungeon_options": "all_sections",

        "randomize_tears": "vanilla_items",
        "tear_size": "small",
        "tear_sections": "progressive",
        "spirit_weapons": "final_tear",

        "keysanity": "vanilla",
        "randomize_boss_keys": "anywhere",
        "keyrings": "all",
        "shuffle_tos_sections": "no_shuffle",
        "plando_dungeon_pool": {"ToS 1", "ToS 2", "ToS 5"},

        "shopsanity": {"all"},
        "rupee_farming_logic": "no_farming",
        "excess_random_treasure": "nothing",
        "logic": "normal",
        "randomize_passengers": "randomize",
        "randomize_cargo": "no_cargo",
        "randomize_stamps": "randomize",
        "stamp_pack_sizes": 1,
        "randomize_minigames": "hard",
        "exclude_dungeons": "remove",
        "exclude_sections": "remove",
        "track_pool": "mixed_small",
        "start_with_train": True,
        "cannon_logic": "open_train",
        "portal_behavior": "always_open",

    }