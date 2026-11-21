from enum import StrEnum
from typing import Any

from BaseClasses import ItemClassification


class ItemName(StrEnum):
    progressive_shield = "Progressive Shield"
    bombs_10 = "Bombs (10)"
    cane_of_somaria = "Cane of Somaria"
    progressive_sword = "Progressive Sword"
    progressive_boomerang = "Progressive Boomerang"
    rod_of_seasons_spring = "Rod of Seasons (Spring)"
    rod_of_seasons_summer = "Rod of Seasons (Summer)"
    rod_of_seasons_autumn = "Rod of Seasons (Autumn)"
    rod_of_seasons_winter = "Rod of Seasons (Winter)"
    magnetic_gloves = "Magnetic Gloves"
    switch_hook = "Progressive Hook"
    biggorons_sword = "Biggoron's Sword"
    bombchus_10 = "Bombchus (10)"
    rickys_flute = "Ricky's Flute"
    dimitris_flute = "Dimitri's Flute"
    mooshs_flute = "Moosh's Flute"
    seed_shooter = "Seed Shooter"
    progressive_slingshot = "Progressive Slingshot"
    shovel = "Shovel"
    power_bracelet = "Power Bracelet"
    progressive_feather = "Progressive Feather"
    seed_satchel = "Seed Satchel"
    fools_ore = "Fool's Ore"
    ember_seeds = "Ember Seeds"
    scent_seeds = "Scent Seeds"
    pegasus_seeds = "Pegasus Seeds"
    gale_seeds = "Gale Seeds"
    mystery_seeds = "Mystery Seeds"
    rupees_1 = "Rupees (1)"
    rupees_5 = "Rupees (5)"
    rupees_10 = "Rupees (10)"
    rupees_20 = "Rupees (20)"
    rupees_30 = "Rupees (30)"
    rupees_50 = "Rupees (50)"
    rupees_100 = "Rupees (100)"
    rupees_200 = "Rupees (200)"
    ore_chunks_10 = "Ore Chunks (10)"
    ore_chunks_25 = "Ore Chunks (25)"
    ore_chunks_50 = "Ore Chunks (50)"
    ore_chunks_100 = "Ore Chunks (100)"
    heart_container = "Heart Container"
    piece_of_heart = "Piece of Heart"
    rare_peach_stone = "Rare Peach Stone"
    flippers = "Flippers"
    potion = "Potion"
    small_key_heros_cave = "Small Key (Hero's Cave)"
    small_key_gnarled_root_dungeon = "Small Key (Gnarled Root Dungeon)"
    small_key_snakes_remains = "Small Key (Snake's Remains)"
    small_key_poison_moths_lair = "Small Key (Poison Moth's Lair)"
    small_key_dancing_dragon_dungeon = "Small Key (Dancing Dragon Dungeon)"
    small_key_unicorns_cave = "Small Key (Unicorn's Cave)"
    small_key_ancient_ruins = "Small Key (Ancient Ruins)"
    small_key_explorers_crypt = "Small Key (Explorer's Crypt)"
    small_key_sword_shield_dungeon = "Small Key (Sword & Shield Dungeon)"
    small_key_linked_heros_cave = "Small Key (Linked Hero's Cave)"
    master_key_heros_cave = "Master Key (Hero's Cave)"
    master_key_gnarled_root_dungeon = "Master Key (Gnarled Root Dungeon)"
    master_key_snakes_remains = "Master Key (Snake's Remains)"
    master_key_poison_moths_lair = "Master Key (Poison Moth's Lair)"
    master_key_dancing_dragon_dungeon = "Master Key (Dancing Dragon Dungeon)"
    master_key_unicorns_cave = "Master Key (Unicorn's Cave)"
    master_key_ancient_ruins = "Master Key (Ancient Ruins)"
    master_key_explorers_crypt = "Master Key (Explorer's Crypt)"
    master_key_sword_shield_dungeon = "Master Key (Sword & Shield Dungeon)"
    master_key_linked_heros_cave = "Master Key (Linked Hero's Cave)"
    boss_key_gnarled_root_dungeon = "Boss Key (Gnarled Root Dungeon)"
    boss_key_snakes_remains = "Boss Key (Snake's Remains)"
    boss_key_poison_moths_lair = "Boss Key (Poison Moth's Lair)"
    boss_key_dancing_dragon_dungeon = "Boss Key (Dancing Dragon Dungeon)"
    boss_key_unicorns_cave = "Boss Key (Unicorn's Cave)"
    boss_key_ancient_ruins = "Boss Key (Ancient Ruins)"
    boss_key_explorers_crypt = "Boss Key (Explorer's Crypt)"
    boss_key_sword_shield_dungeon = "Boss Key (Sword & Shield Dungeon)"
    compass_heros_cave = "Compass (Hero's Cave)"
    compass_gnarled_root_dungeon = "Compass (Gnarled Root Dungeon)"
    compass_snakes_remains = "Compass (Snake's Remains)"
    compass_poison_moths_lair = "Compass (Poison Moth's Lair)"
    compass_dancing_dragon_dungeon = "Compass (Dancing Dragon Dungeon)"
    compass_unicorns_cave = "Compass (Unicorn's Cave)"
    compass_ancient_ruins = "Compass (Ancient Ruins)"
    compass_explorers_crypt = "Compass (Explorer's Crypt)"
    compass_sword_shield_dungeon = "Compass (Sword & Shield Dungeon)"
    dungeon_map_heros_cave = "Dungeon Map (Hero's Cave)"
    dungeon_map_gnarled_root_dungeon = "Dungeon Map (Gnarled Root Dungeon)"
    dungeon_map_snakes_remains = "Dungeon Map (Snake's Remains)"
    dungeon_map_poison_moths_lair = "Dungeon Map (Poison Moth's Lair)"
    dungeon_map_dancing_dragon_dungeon = "Dungeon Map (Dancing Dragon Dungeon)"
    dungeon_map_unicorns_cave = "Dungeon Map (Unicorn's Cave)"
    dungeon_map_ancient_ruins = "Dungeon Map (Ancient Ruins)"
    dungeon_map_explorers_crypt = "Dungeon Map (Explorer's Crypt)"
    dungeon_map_sword_shield_dungeon = "Dungeon Map (Sword & Shield Dungeon)"
    gasha_seed = "Gasha Seed"
    cuccodex = "Cuccodex"
    lon_lon_egg = "Lon Lon Egg"
    ghastly_doll = "Ghastly Doll"
    iron_pot = "Iron Pot"
    lava_soup = "Lava Soup"
    goron_vase = "Goron Vase"
    fish = "Fish"
    megaphone = "Megaphone"
    mushroom = "Mushroom"
    wooden_bird = "Wooden Bird"
    engine_grease = "Engine Grease"
    phonograph = "Phonograph"
    gnarled_key = "Gnarled Key"
    floodgate_key = "Floodgate Key"
    dragon_key = "Dragon Key"
    star_ore = "Star Ore"
    ribbon = "Ribbon"
    spring_banana = "Spring Banana"
    rickys_gloves = "Ricky's Gloves"
    rusty_bell = "Rusty Bell"
    pirates_bell = "Pirate's Bell"
    treasure_map = "Treasure Map"
    round_jewel = "Round Jewel"
    pyramid_jewel = "Pyramid Jewel"
    square_jewel = "Square Jewel"
    x_shaped_jewel = "X-Shaped Jewel"
    red_ore = "Red Ore"
    blue_ore = "Blue Ore"
    hard_ore = "Hard Ore"
    members_card = "Member's Card"
    masters_plaque = "Master's Plaque"
    bombchu_upgrade = "Bombchu Upgrade"
    bomb_upgrade = "Bomb Upgrade"
    friendship_ring = "Friendship Ring"
    power_ring_l_1 = "Power Ring L-1"
    power_ring_l_2 = "Power Ring L-2"
    power_ring_l_3 = "Power Ring L-3"
    armor_ring_l_1 = "Armor Ring L-1"
    armor_ring_l_2 = "Armor Ring L-2"
    armor_ring_l_3 = "Armor Ring L-3"
    red_ring = "Red Ring"
    blue_ring = "Blue Ring"
    green_ring = "Green Ring"
    cursed_ring = "Cursed Ring"
    experts_ring = "Expert's Ring"
    blast_ring = "Blast Ring"
    rang_ring_l_1 = "Rang Ring L-1"
    gba_time_ring = "GBA Time Ring"
    maples_ring = "Maple's Ring"
    steadfast_ring = "Steadfast Ring"
    pegasus_ring = "Pegasus Ring"
    toss_ring = "Toss Ring"
    heart_ring_l_1 = "Heart Ring L-1"
    heart_ring_l_2 = "Heart Ring L-2"
    swimmers_ring = "Swimmer's Ring"
    charge_ring = "Charge Ring"
    light_ring_l_1 = "Light Ring L-1"
    light_ring_l_2 = "Light Ring L-2"
    bombers_ring = "Bomber's Ring"
    green_luck_ring = "Green Luck Ring"
    blue_luck_ring = "Blue Luck Ring"
    gold_luck_ring = "Gold Luck Ring"
    red_luck_ring = "Red Luck Ring"
    green_holy_ring = "Green Holy Ring"
    blue_holy_ring = "Blue Holy Ring"
    red_holy_ring = "Red Holy Ring"
    snowshoe_ring = "Snowshoe Ring"
    rocs_ring = "Roc's Ring"
    quicksand_ring = "Quicksand Ring"
    red_joy_ring = "Red Joy Ring"
    blue_joy_ring = "Blue Joy Ring"
    gold_joy_ring = "Gold Joy Ring"
    green_joy_ring = "Green Joy Ring"
    discovery_ring = "Discovery Ring"
    rang_ring_l_2 = "Rang Ring L-2"
    octo_ring = "Octo Ring"
    moblin_ring = "Moblin Ring"
    like_like_ring = "Like Like Ring"
    subrosian_ring = "Subrosian Ring"
    first_gen_ring = "First Gen Ring"
    spin_ring = "Spin Ring"
    bombproof_ring = "Bombproof Ring"
    energy_ring = "Energy Ring"
    dbl_edge_ring = "Dbl. Edge Ring"
    gba_nature_ring = "GBA Nature Ring"
    slayers_ring = "Slayer's Ring"
    rupee_ring = "Rupee Ring"
    victory_ring = "Victory Ring"
    sign_ring = "Sign Ring"
    _100th_ring = "100th Ring"
    whisp_ring = "Whisp Ring"
    gasha_ring = "Gasha Ring"
    peace_ring = "Peace Ring"
    zora_ring = "Zora Ring"
    fist_ring = "Fist Ring"
    whimsical_ring = "Whimsical Ring"
    protection_ring = "Protection Ring"
    bomb_flower = "Bomb Flower"
    fertile_soil = "Fertile Soil"
    gift_of_time = "Gift of Time"
    bright_sun = "Bright Sun"
    soothing_rain = "Soothing Rain"
    nurturing_warmth = "Nurturing Warmth"
    blowing_wind = "Blowing Wind"
    seed_of_life = "Seed of Life"
    changing_seasons = "Changing Seasons"
    maku_seed = "Maku Seed"
    heros_cave_keydoor_unlock = "Hero's Cave: Keydoor Unlock"
    gnarled_root_dungeon_keydoor_left_of_entrance_unlock = "Gnarled Root Dungeon: Keydoor Left of Entrance Unlock"
    gnarled_root_dungeon_miniboss_keydoor_unlock = "Gnarled Root Dungeon: Miniboss Keydoor Unlock"
    snakes_remains_keydoor_to_hardhats_unlock = "Snake's Remains: Keydoor to Hardhats Unlock"
    snakes_remains_miniboss_keydoor_unlock = "Snake's Remains: Miniboss Keydoor Unlock"
    snakes_remains_spinner_keyblock_unlock = "Snake's Remains: Spinner Keyblock Unlock"
    poison_moth_lair_keydoor_to_mimics_unlock = "Poison Moth's Lair: Keydoor to Mimics Unlock"
    poison_moth_lair_miniboss_keydoor_unlock = "Poison Moth's Lair: Miniboss Keydoor Unlock"
    dancing_dragon_dungeon_entrance_keydoor_unlock = "Dancing Dragon Dungeon: Entrance Keydoor Unlock"
    dancing_dragon_dungeon_minecart_keyblock_unlock = "Dancing Dragon Dungeon: Minecart Keyblock Unlock"
    dancing_dragon_dungeon_crumbling_floor_keydoor_unlock = "Dancing Dragon Dungeon: Crumbling Floor Keydoor Unlock"
    dancing_dragon_dungeon_pool_keyblock_unlock = "Dancing Dragon Dungeon: Pool Keyblock Unlock"
    dancing_dragon_dungeon_boss_keyblock_unlock = "Dancing Dragon Dungeon: Boss Keyblock Unlock"
    unicorns_cave_magnet_gloves_keydoor_unlock = "Unicorn's Cave: Magnet Gloves Keydoor Unlock"
    unicorns_cave_miniboss_keydoor_unlock = "Unicorn's Cave: Miniboss Keydoor Unlock"
    unicorns_cave_wall_of_flames_keydoor_unlock = "Unicorn's Cave: Wall of Flames Keydoor Unlock"
    unicorns_cave_basement_keydoor_unlock = "Unicorn's Cave: Basement Keydoor Unlock"
    unicorns_cave_boss_keyblock_unlock = "Unicorn's Cave: Boss Keyblock Unlock"
    ancient_ruins_entrance_keyblock_unlock = "Ancient Ruins: Entrance Keyblock Unlock"
    ancient_ruins_right_path_keydoor_unlock = "Ancient Ruins: Right Path Keydoor Unlock"
    ancient_ruins_miniboss_keydoor_unlock = "Ancient Ruins: Miniboss Keydoor Unlock"
    explorers_crypt_entrance_keydoor_unlock = "Explorer's Crypt: Entrance Keydoor Unlock"
    explorers_crypt_keydoor_to_enclosed_trampoline_unlock = "Explorer's Crypt: Keydoor to Enclosed Trampoline Unlock"
    explorers_crypt_margrets_keydoor_unlock = "Explorer's Crypt: Margret's Keydoor Unlock"
    explorers_crypt_flying_tile_keyblock_unlock = "Explorer's Crypt: Flying Tile Keyblock Unlock"
    explorers_crypt_shining_blue_puzzle_keydoor_unlock = "Explorer's Crypt: Shining Blue Puzzle Keydoor Unlock"
    sword_shield_dungeon_entrance_keyblock_unlock = "Sword & Shield Dungeon: Entrance Keyblock Unlock"
    sword_shield_dungeon_spinner_keydoor_unlock = "Sword & Shield Dungeon: Spinner Keydoor Unlock"
    sword_shield_dungeon_miniboss_keydoor_unlock = "Sword & Shield Dungeon: Miniboss Keydoor Unlock"
    sword_shield_dungeon_ice_crystals_keydoor_unlock = "Sword & Shield Dungeon: Ice Crystals Keydoor Unlock"
    sword_shield_dungeon_lava_hole_keyblock_unlock = "Sword & Shield Dungeon: Lava Hole Keyblock Unlock"
    sword_shield_dungeon_beamos_keydoor_unlock = "Sword & Shield Dungeon: Beamos Keydoor Unlock"
    sword_shield_dungeon_boss_keyblock_unlock = "Sword & Shield Dungeon: Boss Keyblock Unlock"
    linked_heros_cave_floor_2_keydoor_unlock = "Linked Hero's Cave: Floor 2 Keydoor Unlock"
    linked_heros_cave_floor_3_keyblock_unlock = "Linked Hero's Cave: Floor 3 Keyblock Unlock"
    linked_heros_cave_floor_3_keydoor_unlock = "Linked Hero's Cave: Floor 3 Keydoor Unlock"
    linked_heros_cave_boomerang_maze_keydoor_unlock = "Linked Hero's Cave: Boomerang Maze Keydoor Unlock"
    linked_heros_cave_final_challenge_keydoor_unlock = "Linked Hero's Cave: Final Challenge Keydoor Unlock"


ITEMS_DATA: dict[ItemName, dict[str, Any]] = {
    #   "No Item": {
    #   'classification': ItemClassification.filler,
    #   "",
    #    'id': 0x00,
    #    'subid': 0x00
    #    },
    ItemName.progressive_shield: {"classification": ItemClassification.progression, "id": 0x01},
    ItemName.bombs_10: {"classification": ItemClassification.filler, "id": 0x03, "repeatable": True},
    ItemName.cane_of_somaria: {"classification": ItemClassification.progression, "id": 0x04},
    ItemName.progressive_sword: {"classification": ItemClassification.progression, "id": 0x05},
    ItemName.progressive_boomerang: {"classification": ItemClassification.progression, "id": 0x06},
    ItemName.rod_of_seasons_spring: {"classification": ItemClassification.progression, "id": 0x07, "subid": 0x02},
    ItemName.rod_of_seasons_summer: {"classification": ItemClassification.progression, "id": 0x07, "subid": 0x03},
    ItemName.rod_of_seasons_autumn: {"classification": ItemClassification.progression, "id": 0x07, "subid": 0x04},
    ItemName.rod_of_seasons_winter: {"classification": ItemClassification.progression, "id": 0x07, "subid": 0x05},
    ItemName.magnetic_gloves: {"classification": ItemClassification.progression, "id": 0x08},
    ItemName.switch_hook: {"classification": ItemClassification.progression, "id": 0x0A},
    ItemName.biggorons_sword: {"classification": ItemClassification.progression, "id": 0x0C},
    ItemName.bombchus_10: {"classification": ItemClassification.filler, "id": 0x0D, "repeatable": True},
    ItemName.rickys_flute: {"classification": ItemClassification.progression, "id": 0x0E, "subid": 0x00},
    ItemName.dimitris_flute: {"classification": ItemClassification.progression, "id": 0x0E, "subid": 0x01},
    ItemName.mooshs_flute: {"classification": ItemClassification.progression, "id": 0x0E, "subid": 0x02},
    ItemName.seed_shooter: {"classification": ItemClassification.progression, "id": 0x0F},
    # "Progressive Harp": {
    #     'classification': ItemClassification.progression,
    #     'id': 0x11
    # },
    ItemName.progressive_slingshot: {"classification": ItemClassification.progression, "id": 0x13},
    ItemName.shovel: {"classification": ItemClassification.progression, "id": 0x15},
    ItemName.power_bracelet: {"classification": ItemClassification.progression, "id": 0x16},
    ItemName.progressive_feather: {"classification": ItemClassification.progression, "id": 0x17},
    ItemName.seed_satchel: {"classification": ItemClassification.progression, "id": 0x19},
    ItemName.fools_ore: {"classification": ItemClassification.progression, "id": 0x1E},
    ItemName.ember_seeds: {"classification": ItemClassification.progression, "id": 0x20},
    ItemName.scent_seeds: {"classification": ItemClassification.progression, "id": 0x21},
    ItemName.pegasus_seeds: {"classification": ItemClassification.progression, "id": 0x22},
    ItemName.gale_seeds: {"classification": ItemClassification.progression, "id": 0x23},
    ItemName.mystery_seeds: {"classification": ItemClassification.progression, "id": 0x24},
    ItemName.rupees_1: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x00, "repeatable": True},
    ItemName.rupees_5: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x01, "repeatable": True},
    ItemName.rupees_10: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x02, "repeatable": True},
    ItemName.rupees_20: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x03, "repeatable": True},
    ItemName.rupees_30: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x04, "repeatable": True},
    ItemName.rupees_50: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x05, "repeatable": True},
    ItemName.rupees_100: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x06, "repeatable": True},
    ItemName.rupees_200: {"classification": ItemClassification.filler, "id": 0x28, "subid": 0x08, "repeatable": True},
    ItemName.ore_chunks_10: {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x02,
        "repeatable": True,
    },
    ItemName.ore_chunks_25: {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x01,
        "repeatable": True,
    },
    ItemName.ore_chunks_50: {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x00,
        "repeatable": True,
    },
    ItemName.ore_chunks_100: {
        "classification": ItemClassification.filler,
        "id": 0x37,
        "subid": 0x03,
        "repeatable": True,
    },
    ItemName.heart_container: {"classification": ItemClassification.useful, "id": 0x2A},
    ItemName.piece_of_heart: {"classification": ItemClassification.filler, "id": 0x2B, "subid": 0x01},
    ItemName.rare_peach_stone: {"classification": ItemClassification.filler, "id": 0x2B, "subid": 0x02},
    ItemName.flippers: {"classification": ItemClassification.progression, "id": 0x2E},
    ItemName.potion: {"classification": ItemClassification.filler, "id": 0x2F, "repeatable": True},
    ItemName.small_key_heros_cave: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x00,
    },
    ItemName.small_key_gnarled_root_dungeon: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x01,
    },
    ItemName.small_key_snakes_remains: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x02,
    },
    ItemName.small_key_poison_moths_lair: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x03,
    },
    ItemName.small_key_dancing_dragon_dungeon: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x04,
    },
    ItemName.small_key_unicorns_cave: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x05,
    },
    ItemName.small_key_ancient_ruins: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x06,
    },
    ItemName.small_key_explorers_crypt: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x07,
    },
    ItemName.small_key_sword_shield_dungeon: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x08,
    },
    ItemName.small_key_linked_heros_cave: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x0B,
    },
    ItemName.master_key_heros_cave: {
        "classification": ItemClassification.progression_deprioritized,
        "id": 0x30,
        "subid": 0x80,
    },
    ItemName.master_key_gnarled_root_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x81,
    },
    ItemName.master_key_snakes_remains: {"classification": ItemClassification.progression, "id": 0x30, "subid": 0x82},
    ItemName.master_key_poison_moths_lair: {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x83,
    },
    ItemName.master_key_dancing_dragon_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x84,
    },
    ItemName.master_key_unicorns_cave: {"classification": ItemClassification.progression, "id": 0x30, "subid": 0x85},
    ItemName.master_key_ancient_ruins: {"classification": ItemClassification.progression, "id": 0x30, "subid": 0x86},
    ItemName.master_key_explorers_crypt: {"classification": ItemClassification.progression, "id": 0x30, "subid": 0x87},
    ItemName.master_key_sword_shield_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x88,
    },
    ItemName.master_key_linked_heros_cave: {
        "classification": ItemClassification.progression,
        "id": 0x30,
        "subid": 0x8B,
    },
    ItemName.boss_key_gnarled_root_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x00,
    },
    ItemName.boss_key_snakes_remains: {"classification": ItemClassification.progression, "id": 0x31, "subid": 0x01},
    ItemName.boss_key_poison_moths_lair: {"classification": ItemClassification.progression, "id": 0x31, "subid": 0x02},
    ItemName.boss_key_dancing_dragon_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x03,
    },
    ItemName.boss_key_unicorns_cave: {"classification": ItemClassification.progression, "id": 0x31, "subid": 0x04},
    ItemName.boss_key_ancient_ruins: {"classification": ItemClassification.progression, "id": 0x31, "subid": 0x05},
    ItemName.boss_key_explorers_crypt: {"classification": ItemClassification.progression, "id": 0x31, "subid": 0x06},
    ItemName.boss_key_sword_shield_dungeon: {
        "classification": ItemClassification.progression,
        "id": 0x31,
        "subid": 0x07,
    },
    ItemName.compass_heros_cave: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x00},
    ItemName.compass_gnarled_root_dungeon: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x01},
    ItemName.compass_snakes_remains: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x02},
    ItemName.compass_poison_moths_lair: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x03},
    ItemName.compass_dancing_dragon_dungeon: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x04},
    ItemName.compass_unicorns_cave: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x05},
    ItemName.compass_ancient_ruins: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x06},
    ItemName.compass_explorers_crypt: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x07},
    ItemName.compass_sword_shield_dungeon: {"classification": ItemClassification.useful, "id": 0x32, "subid": 0x08},
    ItemName.dungeon_map_heros_cave: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x00},
    ItemName.dungeon_map_gnarled_root_dungeon: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x01},
    ItemName.dungeon_map_snakes_remains: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x02},
    ItemName.dungeon_map_poison_moths_lair: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x03},
    ItemName.dungeon_map_dancing_dragon_dungeon: {
        "classification": ItemClassification.useful,
        "id": 0x33,
        "subid": 0x04,
    },
    ItemName.dungeon_map_unicorns_cave: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x05},
    ItemName.dungeon_map_ancient_ruins: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x06},
    ItemName.dungeon_map_explorers_crypt: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x07},
    ItemName.dungeon_map_sword_shield_dungeon: {"classification": ItemClassification.useful, "id": 0x33, "subid": 0x08},
    ItemName.gasha_seed: {"classification": ItemClassification.filler, "id": 0x34, "subid": 0x01},
    ItemName.cuccodex: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x55},
    ItemName.lon_lon_egg: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x56},
    ItemName.ghastly_doll: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x57},
    ItemName.iron_pot: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x35},
    ItemName.lava_soup: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x38},
    ItemName.goron_vase: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x39},
    ItemName.fish: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3A},
    ItemName.megaphone: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3B},
    ItemName.mushroom: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3C},
    ItemName.wooden_bird: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3D},
    ItemName.engine_grease: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3E},
    ItemName.phonograph: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x3F},
    ItemName.gnarled_key: {"classification": ItemClassification.progression, "id": 0x42},
    ItemName.floodgate_key: {"classification": ItemClassification.progression, "id": 0x43},
    ItemName.dragon_key: {"classification": ItemClassification.progression, "id": 0x44},
    ItemName.star_ore: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x45},
    ItemName.ribbon: {"classification": ItemClassification.progression, "id": 0x46},
    ItemName.spring_banana: {"classification": ItemClassification.progression, "id": 0x47},
    ItemName.rickys_gloves: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x48},
    ItemName.rusty_bell: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x4A},
    ItemName.pirates_bell: {"classification": ItemClassification.progression, "id": 0x25},
    ItemName.treasure_map: {"classification": ItemClassification.useful, "id": 0x4B},
    ItemName.round_jewel: {"classification": ItemClassification.progression, "id": 0x4C},
    ItemName.pyramid_jewel: {"classification": ItemClassification.progression, "id": 0x4D},
    ItemName.square_jewel: {"classification": ItemClassification.progression, "id": 0x4E},
    ItemName.x_shaped_jewel: {"classification": ItemClassification.progression, "id": 0x4F},
    ItemName.red_ore: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x50},
    ItemName.blue_ore: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x51},
    ItemName.hard_ore: {"classification": ItemClassification.progression_deprioritized_skip_balancing, "id": 0x52},
    ItemName.members_card: {"classification": ItemClassification.progression, "id": 0x53},
    ItemName.masters_plaque: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x54,
    },
    ItemName.bombchu_upgrade: {
        "classification": ItemClassification.progression,
        "id": 0x5F,
    },
    # 0x60 is the master diver challenge's ore
    ItemName.bomb_upgrade: {
        "classification": ItemClassification.progression,
        "id": 0x61,
    },
    #   "Satchel Upgrade": {
    #   'classification': ItemClassification.progression,
    #        'id': 0x62
    ItemName.friendship_ring: {
        "classification": ItemClassification.filler,
        "id": 0x2D,
        "subid": 0x04,
        "ring": "useless",
    },
    ItemName.power_ring_l_1: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x05, "ring": "good"},
    ItemName.power_ring_l_2: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x06, "ring": "good"},
    ItemName.power_ring_l_3: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x07, "ring": "good"},
    ItemName.armor_ring_l_1: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x08, "ring": "good"},
    ItemName.armor_ring_l_2: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x09, "ring": "good"},
    ItemName.armor_ring_l_3: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0A, "ring": "good"},
    ItemName.red_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0B, "ring": "good"},
    ItemName.blue_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0C, "ring": "good"},
    ItemName.green_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0D, "ring": "good"},
    ItemName.cursed_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0E, "ring": "useless"},
    ItemName.experts_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x0F, "ring": "good"},
    ItemName.blast_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x10, "ring": "good"},
    ItemName.rang_ring_l_1: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x11, "ring": "good"},
    ItemName.gba_time_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x12, "ring": "useless"},
    ItemName.maples_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x13, "ring": "good"},
    ItemName.steadfast_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x14, "ring": "good"},
    ItemName.pegasus_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x15, "ring": "good"},
    ItemName.toss_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x16, "ring": "good"},
    ItemName.heart_ring_l_1: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x17, "ring": "good"},
    ItemName.heart_ring_l_2: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x18, "ring": "good"},
    ItemName.swimmers_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x19, "ring": "good"},
    ItemName.charge_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1A, "ring": "good"},
    ItemName.light_ring_l_1: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1B, "ring": "good"},
    ItemName.light_ring_l_2: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1C, "ring": "good"},
    ItemName.bombers_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1D, "ring": "good"},
    ItemName.green_luck_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1E, "ring": "good"},
    ItemName.blue_luck_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x1F, "ring": "good"},
    ItemName.gold_luck_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x20, "ring": "good"},
    ItemName.red_luck_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x21, "ring": "good"},
    ItemName.green_holy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x22, "ring": "good"},
    ItemName.blue_holy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x23, "ring": "good"},
    ItemName.red_holy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x24, "ring": "good"},
    ItemName.snowshoe_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x25, "ring": "good"},
    ItemName.rocs_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x26, "ring": "good"},
    ItemName.quicksand_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x27, "ring": "good"},
    ItemName.red_joy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x28, "ring": "good"},
    ItemName.blue_joy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x29, "ring": "good"},
    ItemName.gold_joy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2A, "ring": "good"},
    ItemName.green_joy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2B, "ring": "good"},
    ItemName.discovery_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2C, "ring": "good"},
    ItemName.rang_ring_l_2: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2D, "ring": "good"},
    ItemName.octo_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2E, "ring": "useless"},
    ItemName.moblin_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x2F, "ring": "useless"},
    ItemName.like_like_ring: {
        "classification": ItemClassification.filler,
        "id": 0x2D,
        "subid": 0x30,
        "ring": "useless",
    },
    ItemName.subrosian_ring: {
        "classification": ItemClassification.filler,
        "id": 0x2D,
        "subid": 0x31,
        "ring": "useless",
    },
    ItemName.first_gen_ring: {
        "classification": ItemClassification.filler,
        "id": 0x2D,
        "subid": 0x32,
        "ring": "useless",
    },
    ItemName.spin_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x33, "ring": "good"},
    ItemName.bombproof_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x34, "ring": "good"},
    ItemName.energy_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x35, "ring": "good"},
    ItemName.dbl_edge_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x36, "ring": "good"},
    ItemName.gba_nature_ring: {
        "classification": ItemClassification.filler,
        "id": 0x2D,
        "subid": 0x37,
        "ring": "useless",
    },
    ItemName.slayers_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x38, "ring": "useless"},
    ItemName.rupee_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x39, "ring": "useless"},
    ItemName.victory_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3A, "ring": "useless"},
    ItemName.sign_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3B, "ring": "useless"},
    ItemName._100th_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3C, "ring": "useless"},
    ItemName.whisp_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3D, "ring": "good"},
    ItemName.gasha_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3E, "ring": "good"},
    ItemName.peace_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x3F, "ring": "good"},
    ItemName.zora_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x40, "ring": "good"},
    ItemName.fist_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x41, "ring": "good"},
    ItemName.whimsical_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x42, "ring": "good"},
    ItemName.protection_ring: {"classification": ItemClassification.filler, "id": 0x2D, "subid": 0x43, "ring": "good"},
    ItemName.bomb_flower: {"classification": ItemClassification.progression, "id": 0x49},
    ItemName.fertile_soil: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x00},
    ItemName.gift_of_time: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x01},
    ItemName.bright_sun: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x02},
    ItemName.soothing_rain: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x03},
    ItemName.nurturing_warmth: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x04},
    ItemName.blowing_wind: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x05},
    ItemName.seed_of_life: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x06},
    ItemName.changing_seasons: {"classification": ItemClassification.progression, "id": 0x40, "subid": 0x07},
    ItemName.maku_seed: {  # Mostly for debug
        "classification": ItemClassification.progression_skip_balancing,
        "id": 0x36,
    },
    # Key Unlocks
    ItemName.heros_cave_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x00,
    },
    ItemName.gnarled_root_dungeon_keydoor_left_of_entrance_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x01,
    },
    ItemName.gnarled_root_dungeon_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x02,
    },
    ItemName.snakes_remains_keydoor_to_hardhats_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x03,
    },
    ItemName.snakes_remains_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x04,
    },
    ItemName.snakes_remains_spinner_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x05,
    },
    ItemName.poison_moth_lair_keydoor_to_mimics_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x06,
    },
    ItemName.poison_moth_lair_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x07,
    },
    ItemName.dancing_dragon_dungeon_entrance_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x08,
    },
    ItemName.dancing_dragon_dungeon_minecart_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x09,
    },
    ItemName.dancing_dragon_dungeon_crumbling_floor_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0A,
    },
    ItemName.dancing_dragon_dungeon_pool_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0B,
    },
    ItemName.dancing_dragon_dungeon_boss_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0C,
    },
    ItemName.unicorns_cave_magnet_gloves_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0D,
    },
    ItemName.unicorns_cave_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0E,
    },
    ItemName.unicorns_cave_wall_of_flames_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x0F,
    },
    ItemName.unicorns_cave_basement_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x10,
    },
    ItemName.unicorns_cave_boss_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x11,
    },
    ItemName.ancient_ruins_entrance_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x12,
    },
    ItemName.ancient_ruins_right_path_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x13,
    },
    ItemName.ancient_ruins_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x14,
    },
    ItemName.explorers_crypt_entrance_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x15,
    },
    ItemName.explorers_crypt_keydoor_to_enclosed_trampoline_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x16,
    },
    ItemName.explorers_crypt_margrets_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x17,
    },
    ItemName.explorers_crypt_flying_tile_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x18,
    },
    ItemName.explorers_crypt_shining_blue_puzzle_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x19,
    },
    ItemName.sword_shield_dungeon_entrance_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1A,
    },
    ItemName.sword_shield_dungeon_spinner_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1B,
    },
    ItemName.sword_shield_dungeon_miniboss_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1C,
    },
    ItemName.sword_shield_dungeon_ice_crystals_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1D,
    },
    ItemName.sword_shield_dungeon_lava_hole_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1E,
    },
    ItemName.sword_shield_dungeon_beamos_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x1F,
    },
    ItemName.sword_shield_dungeon_boss_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x20,
    },
    ItemName.linked_heros_cave_floor_2_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x21,
    },
    ItemName.linked_heros_cave_floor_3_keyblock_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x22,
    },
    ItemName.linked_heros_cave_floor_3_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x23,
    },
    ItemName.linked_heros_cave_boomerang_maze_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x24,
    },
    ItemName.linked_heros_cave_final_challenge_keydoor_unlock: {
        "classification": ItemClassification.progression_deprioritized_skip_balancing,
        "id": 0x5E,
        "subid": 0x25,
    },
}

RING_LIST = [str(name) for name, idata in ITEMS_DATA.items() if "ring" in idata]
