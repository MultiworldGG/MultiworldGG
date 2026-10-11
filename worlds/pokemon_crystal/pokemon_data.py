from .data import data

ALL_UNOWN = [
    f"UNOWN_{char}" for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
]

LEGENDARY_POKEMON = {"Articuno", "Zapdos", "Moltres", "Mewtwo", "Mew", "Entei", "Raikou", "Suicune", "Celebi",
                     "Lugia", "Ho-Oh"}

NON_LEGENDARY_POKEMON = {pokemon.friendly_name for pokemon in data.pokemon.values() if
                         pokemon.friendly_name not in LEGENDARY_POKEMON}

VANILLA_STARTERS = (
    ("CYNDAQUIL", "QUILAVA", "TYPHLOSION"),
    ("TOTODILE", "CROCONAW", "FERALIGATR"),
    ("CHIKORITA", "BAYLEEF", "MEGANIUM"),
)

SWARM_REGISTRATIONS = {
    "Dunsparce_Swarm": {"grass_host": "DARK_CAVE_VIOLET_ENTRANCE", "fishing_region": None,
                        "registration_event": "EVENT_REGISTERED_ANTHONY",
                        "friendly_name": "Dark Cave Violet Entrance (Swarm)"},
    "Yanma_Swarm":     {"grass_host": "ROUTE_35",                  "fishing_region": None,
                        "registration_event": "EVENT_REGISTERED_ARNIE",
                        "friendly_name": "Route 35 (Swarm)"},
    "Qwilfish_Swarm":  {"grass_host": None,                        "fishing_region": "REGION_ROUTE_32:SOUTH",
                        "registration_event": "EVENT_REGISTERED_RALPH",
                        "friendly_name": "Route 32 (Swarm)"},
}

LEGENDARY_STATIC_SLOTS = {"SUICUNE", "LUGIA", "HO_OH", "CELEBI"}

UNIQUE_STATIC_SLOTS = LEGENDARY_STATIC_SLOTS | {"SUDOWOODO", "GYARADOS", "SNORLAX", "LAPRAS"}

ODD_EGG_SPECIES = ["PICHU", "CLEFFA", "IGGLYBUFF", "SMOOCHUM", "MAGBY", "ELEKID", "TYROGUE"]
