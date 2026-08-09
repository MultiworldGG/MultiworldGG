# These constants are for generation purposes.
# Constants for the client should be in SSClientUtils.py

DUNGEON_LIST = [
    "Skyview",
    "Earth Temple",
    "Lanayru Mining Facility",
    "Ancient Cistern",
    "Sandship",
    "Fire Sanctuary",
    "Sky Keep",
]

DUNGEON_ENTRANCE_LIST = [
    "Dungeon Entrance in Deep Woods",
    "Dungeon Entrance in Eldin Volcano",
    "Dungeon Entrance in Lanayru Desert",
    "Dungeon Entrance in Lake Floria",
    "Dungeon Entrance in Lanayru Sand Sea",
    "Dungeon Entrance in Volcano Summit",
    "Dungeon Entrance on Skyloft",
]

TRIAL_LIST = [
    "Skyloft Silent Realm",
    "Faron Silent Realm",
    "Eldin Silent Realm",
    "Lanayru Silent Realm"
]

TRIAL_GATE_LIST = [
    "Trial Gate on Skyloft",
    "Trial Gate in Faron Woods",
    "Trial Gate in Eldin Volcano",
    "Trial Gate in Lanayru Desert",
]

DUNGEON_HC_CHECKS = {
    "Skyview": "Skyview - Heart Container",
    "Earth Temple": "Earth Temple - Heart Container",
    "Lanayru Mining Facility": "Lanayru Mining Facility - Heart Container",
    "Ancient Cistern": "Ancient Cistern - Heart Container",
    "Sandship": "Sandship - Heart Container",
    "Fire Sanctuary": "Fire Sanctuary - Heart Container",
}

DUNGEON_FINAL_CHECKS = {
    "Skyview": "Skyview - Strike Crest",
    "Earth Temple": "Earth Temple - Strike Crest",
    "Lanayru Mining Facility": "Lanayru Mining Facility - Exit Hall of Ancient Robots",
    "Ancient Cistern": "Ancient Cistern - Farore's Flame",
    "Sandship": "Sandship - Nayru's Flame",
    "Fire Sanctuary": "Fire Sanctuary - Din's Flame",
}

DUNGEON_BOSS_NAMES = {
    "Skyview": "Ghirahim I",
    "Earth Temple": "Scaldera",
    "Lanayru Mining Facility": "Moldarach",
    "Ancient Cistern": "Koloktos",
    "Sandship": "Tentalus",
    "Fire Sanctuary": "Ghirahim II",
}

VANILLA_DUNGEON_CONNECTIONS = {
    "Skyview": "Dungeon Entrance in Deep Woods",
    "Earth Temple": "Dungeon Entrance in Eldin Volcano",
    "Lanayru Mining Facility": "Dungeon Entrance in Lanayru Desert",
    "Ancient Cistern": "Dungeon Entrance in Lake Floria",
    "Sandship": "Dungeon Entrance in Lanayru Sand Sea",
    "Fire Sanctuary": "Dungeon Entrance in Volcano Summit",
    "Sky Keep": "Dungeon Entrance on Skyloft",
}

VANILLA_TRIAL_CONNECTIONS = {
    "Skyloft Silent Realm": "Trial Gate on Skyloft",
    "Faron Silent Realm": "Trial Gate in Faron Woods",
    "Eldin Silent Realm": "Trial Gate in Eldin Volcano",
    "Lanayru Silent Realm": "Trial Gate in Lanayru Desert",
}

DUNGEON_INITIAL_REGIONS = {
    "Skyview": "Skyview - First Room",
    "Earth Temple": "Earth Temple - First Room",
    "Lanayru Mining Facility": "Lanayru Mining Facility - First Room",
    "Ancient Cistern": "Ancient Cistern - Main Room",
    "Sandship": "Sandship - Deck",
    "Fire Sanctuary": "Fire Sanctuary - First Room",
    "Sky Keep": "Sky Keep - First Room",
}

DUNGEON_ENTRANCE_REGIONS = {
    "Dungeon Entrance in Deep Woods": "Faron Woods - Deep Woods after Beehive",
    "Dungeon Entrance in Eldin Volcano": "Eldin Volcano - Near Temple Entrance",
    "Dungeon Entrance in Lanayru Desert": "Lanayru Desert - North Desert",
    "Dungeon Entrance in Lake Floria": "Lake Floria - Ancient Cistern Ledge",
    "Dungeon Entrance in Lanayru Sand Sea": "Lanayru Sand Sea - Sea",
    "Dungeon Entrance in Volcano Summit": "Volcano Summit - After Second Frog",
    "Dungeon Entrance on Skyloft": "Central Skyloft",
}

TRIAL_GATE_REGIONS = {
    "Trial Gate on Skyloft": "Central Skyloft",
    "Trial Gate in Faron Woods": "Faron Woods - Viewing Platform",
    "Trial Gate in Eldin Volcano": "Eldin Volcano - Volcano Ascent",
    "Trial Gate in Lanayru Desert": "Lanayru Desert - North Desert",
}

BED_REGIONS = [
    "Upper Skyloft - Knight Academy",
    # "Upper Skyloft - Zelda's Room", # Causes issues
    "Central Skyloft - Orielle and Parrow's House",
    "Central Skyloft - Kukiel's House",
    "Central Skyloft - Piper's House",
    "Central Skyloft - Peatrice's House",
    "Skyloft Village - Sparrot's House",
    "Skyloft Village - Bertie's House",
    "Skyloft Village - Gondo's House",
    "Skyloft Village - Pipit's House",
    "Skyloft Village - Rupin's House",
    "Beedle's Shop",
    "Sky - Lumpy Pumpkin - Inside",
]

BATREAUX_LOCATIONS = [
    # Does not include chest or seventh reward!!
    "Batreaux's House - First Reward",
    "Batreaux's House - Second Reward",
    "Batreaux's House - Third Reward",
    "Batreaux's House - Fourth Reward",
    "Batreaux's House - Fifth Reward",
    "Batreaux's House - Sixth Reward",
    "Batreaux's House - Final Reward",
]

HINT_REGIONS = [
    "Upper Skyloft",
    "Central Skyloft",
    "Skyloft Village",
    "Batreaux's House",
    "Beedle's Shop",
    "Skyloft Silent Realm",
    "Sky",
    "Thunderhead",
    "Sealed Grounds",
    "Hylia's Realm",
    "Faron Woods",
    "Lake Floria",
    "Flooded Faron Woods",
    "Faron Silent Realm",
    "Eldin Volcano",
    "Mogma Turf",
    "Volcano Summit",
    "Bokoblin Base",
    "Eldin Silent Realm",
    "Lanayru Mine",
    "Lanayru Desert",
    "Lanayru Caves",
    "Lanayru Gorge",
    "Lanayru Sand Sea",
    "Lanayru Silent Realm",
    "Skyview",
    "Earth Temple",
    "Lanayru Mining Facility",
    "Ancient Cistern",
    "Sandship",
    "Fire Sanctuary",
    "Sky Keep",
]

SWORD_COUNTS = {
    "swordless": 0,
    "practice_sword": 1,
    "goddess_sword": 2,
    "goddess_longsword": 3,
    "goddess_white_sword": 4,
    "master_sword": 5,
    "true_master_sword": 6,
}

POSSIBLE_RANDOM_STARTING_ITEMS = [
    "Progressive Bow",
    "Progressive Beetle",
    "Progressive Slingshot",
    "Progressive Mitts",
    "Progressive Pouch",
    "Bomb Bag",
    "Clawshots",
    "Whip",
    "Gust Bellows",
    "Water Dragon's Scale",
    "Fireshield Earrings",
    "Goddess's Harp",
    "Spiral Charge",
]

GONDO_UPGRADES = [
    "Progressive Beetle",
    "Progressive Beetle",
    "Progressive Slingshot",
    "Progressive Bow",
    "Progressive Bow",
    "Progressive Bug Net",
]
