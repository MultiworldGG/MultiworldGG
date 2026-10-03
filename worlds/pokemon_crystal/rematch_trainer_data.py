REMATCH_TRAINER_LOCATION_BASE = 9300
NUM_REMATCH_TRAINER_LOCATIONS = 76

GATE_GOLDENROD = "EVENT_VISITED_GOLDENROD"
GATE_OLIVINE = "EVENT_VISITED_OLIVINE"
GATE_ECRUTEAK = "EVENT_VISITED_ECRUTEAK"
GATE_MAHOGANY = "EVENT_VISITED_MAHOGANY"
GATE_LAKE_OF_RAGE = "EVENT_VISITED_LAKE_OF_RAGE"
GATE_CIANWOOD = "EVENT_VISITED_CIANWOOD"
GATE_BLACKTHORN = "EVENT_VISITED_BLACKTHORN"
GATE_ROCKET_HIDEOUT = "EVENT_CLEARED_ROCKET_HIDEOUT"
GATE_RADIO = "EVENT_CLEARED_RADIO_TOWER"
GATE_CHAMPION = "EVENT_BEAT_ELITE_FOUR"
GATE_POWER = "EVENT_RESTORED_POWER_TO_KANTO"

class RematchTrainer:
    __slots__ = ("display_name", "location_name", "trainer_const", "region",
                 "num_rematches", "tier_gates", "base_index", "pokemon_request_slot")

    def __init__(self, display_name: str, location_name: str, trainer_const: str,
                 region: str, tier_gates: list[str], base_index: int,
                 pokemon_request_slot: int | None = None):
        self.display_name = display_name
        self.location_name = location_name
        self.trainer_const = trainer_const
        self.region = region
        self.tier_gates = tier_gates
        self.num_rematches = len(tier_gates)
        self.base_index = base_index
        self.pokemon_request_slot = pokemon_request_slot


REMATCH_TRAINERS: dict[str, RematchTrainer] = {
    "ALAN": RematchTrainer(
        "Schoolboy Alan", "Route 36", "SCHOOLBOY_ALAN", "REGION_ROUTE_36:WEST",
        [GATE_OLIVINE, GATE_BLACKTHORN, GATE_CHAMPION, GATE_POWER], 0),
    "ANTHONY": RematchTrainer(
        "Hiker Anthony", "Route 33", "HIKER_ANTHONY", "REGION_ROUTE_33",
        [GATE_OLIVINE, GATE_RADIO, GATE_CHAMPION, GATE_POWER], 4),
    "ARNIE": RematchTrainer(
        "Bug Catcher Arnie", "Route 35", "BUG_CATCHER_ARNIE", "REGION_ROUTE_35",
        [GATE_LAKE_OF_RAGE, GATE_BLACKTHORN, GATE_CHAMPION, GATE_POWER], 8),
    "BETH": RematchTrainer(
        "Cool Trainer Beth", "Route 26", "COOLTRAINERF_BETH", "REGION_ROUTE_26",
        [GATE_CHAMPION, GATE_POWER], 12),
    "BRENT": RematchTrainer(
        "Pokemaniac Brent", "Route 43", "POKEMANIAC_BRENT", "REGION_ROUTE_43",
        [GATE_ROCKET_HIDEOUT, GATE_CHAMPION, GATE_POWER], 14),
    "CHAD": RematchTrainer(
        "Schoolboy Chad", "Route 38", "SCHOOLBOY_CHAD", "REGION_ROUTE_38",
        [GATE_MAHOGANY, GATE_RADIO, GATE_CHAMPION, GATE_POWER], 17),
    "DANA": RematchTrainer(
        "Lass Dana", "Route 38", "LASS_DANA", "REGION_ROUTE_38",
        [GATE_CIANWOOD, GATE_RADIO, GATE_CHAMPION, GATE_POWER], 21),
    "ERIN": RematchTrainer(
        "Picnicker Erin", "Route 46", "PICNICKER_ERIN", "REGION_ROUTE_46:NORTH",
        [GATE_CHAMPION, GATE_POWER], 25),
    "GAVEN": RematchTrainer(
        "Cool Trainer Gaven", "Route 26", "COOLTRAINERM_GAVEN", "REGION_ROUTE_26",
        [GATE_CHAMPION, GATE_POWER], 27),
    "GINA": RematchTrainer(
        "Picnicker Gina", "Route 34", "PICNICKER_GINA", "REGION_ROUTE_34",
        [GATE_MAHOGANY, GATE_RADIO, GATE_CHAMPION, GATE_POWER], 29),
    "HUEY": RematchTrainer(
        "Sailor Huey", "Olivine Lighthouse 2F", "SAILOR_HUEY", "REGION_OLIVINE_LIGHTHOUSE_2F",
        [GATE_RADIO, GATE_CHAMPION, GATE_POWER], 33),
    "JACK": RematchTrainer(
        "Schoolboy Jack", "National Park", "SCHOOLBOY_JACK", "REGION_NATIONAL_PARK",
        [GATE_OLIVINE, GATE_RADIO, GATE_CHAMPION, GATE_POWER], 36),
    "JOEY": RematchTrainer(
        "Youngster Joey", "Route 30", "YOUNGSTER_JOEY", "REGION_ROUTE_30:POST_MYSTERY_EGG",
        [GATE_GOLDENROD, GATE_OLIVINE, GATE_RADIO, GATE_CHAMPION], 40),
    "JOSE": RematchTrainer(
        "Bird Keeper Jose", "Route 27", "BIRD_KEEPER_JOSE", "REGION_ROUTE_27:EASTWHIRLPOOL",
        [GATE_CHAMPION, GATE_POWER], 44),
    "LIZ": RematchTrainer(
        "Picnicker Liz", "Route 32", "PICNICKER_LIZ", "REGION_ROUTE_32:SOUTH",
        [GATE_ECRUTEAK, GATE_ROCKET_HIDEOUT, GATE_RADIO, GATE_CHAMPION], 46),
    "PARRY": RematchTrainer(
        "Hiker Parry", "Route 45", "HIKER_PARRY", "REGION_ROUTE_45",
        [GATE_CHAMPION, GATE_POWER], 50),
    "RALPH": RematchTrainer(
        "Fisher Ralph", "Route 32", "FISHER_RALPH", "REGION_ROUTE_32:SOUTH",
        [GATE_ECRUTEAK, GATE_LAKE_OF_RAGE, GATE_CHAMPION, GATE_POWER], 52),
    "REENA": RematchTrainer(
        "Cool Trainer Reena", "Route 27", "COOLTRAINERF_REENA", "REGION_ROUTE_27:EAST",
        [GATE_CHAMPION, GATE_POWER], 56),
    "TIFFANY": RematchTrainer(
        "Picnicker Tiffany", "Route 43", "PICNICKER_TIFFANY", "REGION_ROUTE_43",
        [GATE_RADIO, GATE_CHAMPION, GATE_POWER], 58,
        pokemon_request_slot=7),
    "TODD": RematchTrainer(
        "Camper Todd", "Route 34", "CAMPER_TODD", "REGION_ROUTE_34",
        [GATE_CIANWOOD, GATE_BLACKTHORN, GATE_CHAMPION, GATE_POWER], 61),
    "TULLY": RematchTrainer(
        "Fisher Tully", "Route 42", "FISHER_TULLY", "REGION_ROUTE_42:EAST",
        [GATE_ROCKET_HIDEOUT, GATE_CHAMPION, GATE_POWER], 65),
    "VANCE": RematchTrainer(
        "Bird Keeper Vance", "Route 44", "BIRD_KEEPER_VANCE", "REGION_ROUTE_44",
        [GATE_CHAMPION, GATE_POWER], 68),
    "WADE": RematchTrainer(
        "Bug Catcher Wade", "Route 31", "BUG_CATCHER_WADE", "REGION_ROUTE_31",
        [GATE_GOLDENROD, GATE_MAHOGANY, GATE_RADIO, GATE_CHAMPION], 70),
    "WILTON": RematchTrainer(
        "Fisher Wilton", "Route 44", "FISHER_WILTON", "REGION_ROUTE_44",
        [GATE_CHAMPION, GATE_POWER], 74),
}


# Suffix label per gate, used to disambiguate rematch location names.
GATE_LABEL = {
    GATE_GOLDENROD: "Goldenrod",
    GATE_OLIVINE: "Olivine",
    GATE_ECRUTEAK: "Ecruteak",
    GATE_MAHOGANY: "Mahogany",
    GATE_LAKE_OF_RAGE: "Lake of Rage",
    GATE_CIANWOOD: "Cianwood",
    GATE_BLACKTHORN: "Blackthorn",
    GATE_ROCKET_HIDEOUT: "Rocket Hideout",
    GATE_RADIO: "Radio",
    GATE_CHAMPION: "Champion",
    GATE_POWER: "Kanto Power Restored",
}

# Suffix per gate as used in the level-scaling location naming scheme
# `<TRAINER_CONST>_<SUFFIX>` (matches the REMATCHES list in regions.py).
SCALING_SUFFIX = {
    GATE_GOLDENROD: "GOLDENROD",
    GATE_OLIVINE: "OLIVINE",
    GATE_ECRUTEAK: "ECRUTEAK",
    GATE_MAHOGANY: "MAHOGANY",
    GATE_LAKE_OF_RAGE: "LAKE",
    GATE_CIANWOOD: "CIANWOOD",
    GATE_BLACKTHORN: "BLACKTHORN",
    GATE_ROCKET_HIDEOUT: "ROCKETHQ",
    GATE_RADIO: "RADIO",
    GATE_CHAMPION: "CHAMPION",
    GATE_POWER: "POWER",
}


def rematch_location_name(trainer: RematchTrainer, rematch_idx_0: int) -> str:
    """Stable AP location label. rematch_idx_0 is 0..num_rematches-1."""
    gate = trainer.tier_gates[rematch_idx_0]
    return f"{trainer.location_name} - {trainer.display_name} Rematch - {GATE_LABEL[gate]}"


def all_rematch_locations() -> list[tuple[str, int, RematchTrainer, int]]:
    """Yield (label, ap_id, trainer, rematch_idx_0) for every rematch location."""
    out = []
    for trainer in REMATCH_TRAINERS.values():
        for i in range(trainer.num_rematches):
            label = rematch_location_name(trainer, i)
            ap_id = REMATCH_TRAINER_LOCATION_BASE + trainer.base_index + i
            out.append((label, ap_id, trainer, i))
    return out
