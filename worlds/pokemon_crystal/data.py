import pkgutil
from collections import defaultdict
from collections.abc import Sequence, Mapping
from dataclasses import dataclass, field, replace
from enum import Enum, StrEnum, IntEnum, auto
from typing import Any
from re import sub

import orjson
import yaml

from BaseClasses import ItemClassification
from .item_data import GRASS_OFFSET, FLAG_ITEM_OFFSET, CANONICAL_ITEM_ID_MASK
from .mart_data import FRIENDLY_MART_NAMES, MART_CATEGORIES


@dataclass(frozen=True)
class ItemData:
    label: str
    item_id: int
    item_const: str
    price: int
    classification: ItemClassification
    tags: frozenset[str]
    flag_index: int | None
    pocket: str | None


@dataclass(frozen=True)
class LocationData:
    name: str
    label: str
    parent_region: str
    default_item: int
    rom_addresses: list[int]
    flag: int
    tags: frozenset[str]
    scripts: list[str]


@dataclass(frozen=True)
class EventData:
    name: str
    parent_region: str


@dataclass(frozen=True)
class TrainerPokemon:
    level: int
    pokemon: str
    item: str | None
    moves: Sequence[str]


@dataclass(frozen=True)
class TrainerData:
    name: str
    trainer_type: str
    pokemon: Sequence[TrainerPokemon]
    name_length: int


@dataclass(frozen=True)
class LearnsetData:
    level: int
    move: str


class EvolutionType(IntEnum):
    Level = 0
    Item = 1
    Happiness = 2
    Stats = 3
    Trade = 4

    @staticmethod
    def from_string(evo_type_string: str):
        if evo_type_string == "EVOLVE_LEVEL": return EvolutionType.Level
        if evo_type_string == "EVOLVE_ITEM": return EvolutionType.Item
        if evo_type_string == "EVOLVE_HAPPINESS": return EvolutionType.Happiness
        if evo_type_string == "EVOLVE_STAT": return EvolutionType.Stats
        if evo_type_string == "EVOLVE_TRADE": return EvolutionType.Trade
        raise ValueError(f"Invalid evolution type: {evo_type_string}")

    def __str__(self):
        if self is EvolutionType.Level: return "EVOLVE_LEVEL"
        if self is EvolutionType.Item: return "EVOLVE_ITEM"
        if self is EvolutionType.Happiness: return "EVOLVE_HAPPINESS"
        if self is EvolutionType.Stats: return "EVOLVE_STAT"
        if self is EvolutionType.Trade: return "EVOLVE_TRADE"

    def __len__(self) -> int:
        if self is EvolutionType.Stats:
            return 4
        return 3

    def friendly_name(self):
        if self is EvolutionType.Level: return "Level "
        if self is EvolutionType.Item: return "Use "
        if self is EvolutionType.Happiness: return "Happiness"
        if self is EvolutionType.Stats: return "Stats - "
        if self is EvolutionType.Trade: return "Trade"


@dataclass(frozen=True)
class EvolutionData:
    evo_type: EvolutionType
    level: int | None
    condition: str | None
    pokemon: str

    @property
    def method(self) -> str:
        if self.evo_type is EvolutionType.Level:
            return f"Level {self.level}"
        if self.evo_type is EvolutionType.Item:
            from .items import item_const_name_to_label
            return item_const_name_to_label(self.condition)
        if self.evo_type is EvolutionType.Trade:
            from .items import item_const_name_to_label
            return f"Link Cable + {item_const_name_to_label(self.condition)}"
        if self.evo_type is EvolutionType.Happiness:
            return "Happiness"
        if self.evo_type is EvolutionType.Stats:
            if self.condition == "ATK_GT_DEF":
                return "ATK > DEF"
            if self.condition == "ATK_LT_DEF":
                return "ATK < DEF"
            return "ATK == DEF"
        return "?"


class GrowthRate(IntEnum):
    MediumFast = 0
    SlightlyFast = 1
    SlightlySlow = 2
    MediumSlow = 3
    Fast = 4
    Slow = 5

    @staticmethod
    def from_string(growth_rate_string: str):
        if growth_rate_string == "GROWTH_MEDIUM_FAST": return GrowthRate.MediumFast
        if growth_rate_string == "GROWTH_SLIGHTLY_FAST": return GrowthRate.SlightlyFast
        if growth_rate_string == "GROWTH_SLIGHTLY_SLOW": return GrowthRate.SlightlySlow
        if growth_rate_string == "GROWTH_MEDIUM_SLOW": return GrowthRate.MediumSlow
        if growth_rate_string == "GROWTH_FAST": return GrowthRate.Fast
        if growth_rate_string == "GROWTH_SLOW": return GrowthRate.Slow
        raise ValueError(f"Invalid growth rate: {growth_rate_string}")


@dataclass(frozen=True)
class PokemonData:
    id: int
    friendly_name: str
    base_stats: Sequence[int]
    types: Sequence[str]
    evolutions: Sequence[EvolutionData]
    learnset: Sequence[LearnsetData]
    tm_hm: Sequence[str]
    is_base: bool
    bst: int
    egg_groups: Sequence[str]
    gender_ratio: str
    growth_rate: GrowthRate
    produces_egg: str


class MoveCategory(IntEnum):
    Physical = 0b01000000
    Special = 0b10000000
    Status = 0b11000000

    @staticmethod
    def from_string(move_category_string: str):
        if move_category_string == "PHYSICAL": return MoveCategory.Physical
        if move_category_string == "SPECIAL": return MoveCategory.Special
        if move_category_string == "STATUS": return MoveCategory.Status
        raise ValueError(f"Invalid move category: {move_category_string}")


@dataclass(frozen=True)
class MoveData:
    id: str
    rom_id: int
    type: str
    power: int
    accuracy: int
    pp: int
    is_hm: bool
    name: str
    category: MoveCategory


class TypeMatchup(IntEnum):
    NoEffect = 0
    NotVeryEffective = 5
    Effective = 10
    SuperEffective = 20

    @staticmethod
    def from_string(type_matchup_string: str):
        if type_matchup_string == "NO_EFFECT": return TypeMatchup.NoEffect
        if type_matchup_string == "NOT_VERY_EFFECTIVE": return TypeMatchup.NotVeryEffective
        if type_matchup_string == "EFFECTIVE": return TypeMatchup.Effective
        if type_matchup_string == "SUPER_EFFECTIVE": return TypeMatchup.SuperEffective
        raise ValueError(f"Invalid type matchup: {type_matchup_string}")


@dataclass(frozen=True)
class TypeData:
    id: str
    rom_id: int
    matchups: dict[str, TypeMatchup]


@dataclass(frozen=True)
class TMHMData:
    id: str
    tm_num: int
    type: str
    is_hm: bool
    move_id: int


@dataclass(frozen=True)
class MartItemData:
    item: str
    price: int
    flag: int | None
    address: int


@dataclass(frozen=True)
class MartData:
    index: int
    friendly_name: str
    category: str
    items: Sequence[MartItemData]


class MiscOption(IntEnum):
    FuchsiaGym = auto()
    SaffronGym = auto()
    RadioTowerQuestions = auto()
    Amphy = auto()
    FanClubChairman = auto()
    SecretSwitch = auto()
    EcruteakGym = auto()
    RedGyarados = auto()
    OhkoMoves = auto()
    RadioChannels = auto()
    MomItems = auto()
    IcePath = auto()
    TooManyDogs = auto()
    WhirlDexLocations = auto()
    Farfetchd = auto()
    DarkAreas = auto()
    VermilionGym = auto()
    UnLuckyEgg = auto()
    DontFuckleWithShuckle = auto()
    Fuschia = auto()
    NewItem = auto()
    BlueBlue = auto()
    Tracker = auto()
    MountMoon = auto()
    StatusMoves = auto()
    TeleportingAbra = auto()
    Ledge = auto()
    BlackthornGym = auto()
    MahoganyGym = auto()
    DB = auto()
    Chad = auto()
    Chuckster = auto()


@dataclass(frozen=True)
class MiscWarp:
    coords: tuple[int, int]
    id: int


@dataclass(frozen=True)
class MiscSaffronWarps:
    warps: Mapping[str, MiscWarp]
    pairs: Sequence[tuple[str, str]]


@dataclass(frozen=True)
class MiscMomItem:
    index: int
    item: str


@dataclass(frozen=True)
class MiscData:
    fuchsia_gym_trainers: Sequence[Sequence[int]]
    radio_tower_questions: Sequence[str]
    saffron_gym_warps: MiscSaffronWarps
    radio_channel_addresses: Sequence[int]
    mom_items: Sequence[MiscMomItem]
    selected: Sequence[MiscOption] = field(default_factory=lambda: list())

    mild: Sequence[MiscOption] = field(default_factory=lambda: \
        [MiscOption.FuchsiaGym,
         MiscOption.SaffronGym,
         MiscOption.RadioTowerQuestions,
         MiscOption.Amphy,
         MiscOption.FanClubChairman,
         MiscOption.EcruteakGym,
         MiscOption.RedGyarados,
         MiscOption.RadioChannels,
         MiscOption.MomItems,
         MiscOption.IcePath,
         MiscOption.Farfetchd,
         MiscOption.DarkAreas,
         MiscOption.UnLuckyEgg,
         MiscOption.DontFuckleWithShuckle,
         MiscOption.Fuschia,
         MiscOption.NewItem,
         MiscOption.BlueBlue,
         MiscOption.Tracker,
         MiscOption.MountMoon,
         MiscOption.TeleportingAbra,
         MiscOption.Ledge,
         MiscOption.BlackthornGym,
         MiscOption.MahoganyGym,
         MiscOption.DB,
         MiscOption.Chad,
         MiscOption.Chuckster]
                                       )
    wild: Sequence[MiscOption] = field(default_factory=lambda: \
        [MiscOption.SecretSwitch,
         MiscOption.OhkoMoves,  # Not "that bad" but can happen multiple times over an entire run
         MiscOption.TooManyDogs,
         MiscOption.VermilionGym,
         MiscOption.StatusMoves]
                                       )
    dynamic: Sequence[MiscOption] = field(default_factory=lambda: \
         [MiscOption.WhirlDexLocations]
                                          )

    assert len(set(mild.default_factory() + \
                   wild.default_factory() + \
                   dynamic.default_factory())) \
           == max(list(MiscOption)).value, \
        "Misc options are not properly categorized. Each must be assigned to one of 'tame', 'wild' or 'dynamic'."


@dataclass(frozen=True)
class MusicConst:
    id: int
    loop: bool


@dataclass(frozen=True)
class MusicData:
    consts: Mapping[str, MusicConst]
    maps: Mapping[str, str]
    encounters: Sequence[str]
    scripts: Mapping[str, str]

    def __copy__(self):
        return replace(
            self,
            consts=dict(self.consts),
            maps=dict(self.maps),
            encounters=list(self.encounters),
            scripts=dict(self.scripts)
        )


@dataclass(frozen=True)
class EncounterMon:
    level: int
    pokemon: str


class EncounterType(StrEnum):
    Grass = "WildGrass"
    Water = "WildWater"
    Fish = "WildFish"
    Tree = "WildTree"
    RockSmash = "WildRockSmash"
    Swarm = "WildSwarm"
    Static = "Static"


class GrassTimeOfDay(StrEnum):
    Morn = "Morn"
    Day = "Day"
    Nite = "Nite"

    @property
    def ordinal(self) -> int:
        return list(GrassTimeOfDay).index(self)

    @staticmethod
    def from_string(name: str) -> "GrassTimeOfDay | None":
        try:
            return GrassTimeOfDay(name)
        except ValueError:
            return None


class FishingRodType(StrEnum):
    Old = "Old"
    Good = "Good"
    Super = "Super"


class FishTimeOfDay(StrEnum):
    Day = "Day"
    Nite = "Nite"

    @property
    def ordinal(self) -> int:
        return list(FishTimeOfDay).index(self)

    @staticmethod
    def from_string(name: str) -> "FishTimeOfDay | None":
        try:
            return FishTimeOfDay(name)
        except ValueError:
            return None


class TreeRarity(StrEnum):
    Common = "Common"
    Rare = "Rare"


@dataclass(frozen=True)
class EncounterKey:
    encounter_type: EncounterType
    region_id: str | None = None
    time_of_day: "GrassTimeOfDay | FishTimeOfDay | None" = None
    fishing_rod: FishingRodType | None = None
    rarity: TreeRarity | None = None

    @property
    def is_swarm(self) -> bool:
        return self.encounter_type is EncounterType.Swarm

    def region_name(self):
        if (self.encounter_type is EncounterType.Grass
                or self.encounter_type is EncounterType.Water
                or self.encounter_type is EncounterType.Static
                or self.encounter_type is EncounterType.Swarm):
            if self.encounter_type is EncounterType.Grass and self.time_of_day is not None:
                return f"{str(self.encounter_type)}_{self.region_id}_{self.time_of_day.name}"
            return f"{str(self.encounter_type)}_{self.region_id}"
        elif self.encounter_type is EncounterType.Fish:
            if self.time_of_day is not None:
                return f"{str(self.encounter_type)}_{self.region_id}_{str(self.fishing_rod)}_{self.time_of_day.name}"
            return f"{str(self.encounter_type)}_{self.region_id}_{str(self.fishing_rod)}"
        elif self.encounter_type is EncounterType.Tree:
            return f"{str(self.encounter_type)}_{self.region_id}_{str(self.rarity)}"
        elif self.encounter_type is EncounterType.RockSmash:
            return f"{str(self.encounter_type)}"

    def friendly_region_name(self, kanto: bool = True, route_23: bool = False):
        qwilfish_routes = "Routes 12, 13, 32" if kanto else "Route 32"
        if self.encounter_type is EncounterType.Swarm:
            from .pokemon_data import SWARM_REGISTRATIONS
            return SWARM_REGISTRATIONS[self.region_id]["friendly_name"]
        if (self.encounter_type is EncounterType.Grass
                or self.encounter_type is EncounterType.Water):
            from re import search
            # Replace underscores with spaces, capitalize every word that isn't a floor or a cardinal direction
            pretty_region = " ".join([word.capitalize() if search("^(B?\\d+F|[NS][EW])$", word) is None else word
                                      for word in self.region_id.split("_")])
            pretty_region = pretty_region.replace("Digletts", "Diglett's") \
                .replace("Dragons", "Dragon's") \
                .replace(" Of ", " of ")
            if pretty_region.startswith("Whirl"):
                pretty_region = pretty_region.replace("Island", "Islands")
            if self.encounter_type is EncounterType.Grass:
                if self.time_of_day is not None:
                    return f"{pretty_region} (Land - {self.time_of_day.name})"
                return f"{pretty_region} (Land)"
            elif self.encounter_type is EncounterType.Water:
                return f"{pretty_region} (Surf)"
            elif self.encounter_type is EncounterType.Static:
                return f"{pretty_region} (Static)"
        elif self.encounter_type is EncounterType.Fish:
            replacement_table = {
                "WhirlIslands": "Whirl Islands",
                "Gyarados": "Lake of Rage / Fuchsia City" if kanto else "Lake of Rage",
                "Dratini": "Dragon's Den",
                "Dratini_2": "Routes 23, 45" if route_23 else "Route 45",
                "Qwilfish": qwilfish_routes,
            }
            fishing_spot = replacement_table[
                self.region_id] if self.region_id in replacement_table.keys() else self.region_id
            if self.time_of_day is not None:
                return f"{fishing_spot} ({str(self.fishing_rod)} Rod - {self.time_of_day.name})"
            return f"{fishing_spot} ({str(self.fishing_rod)} Rod)"
        elif self.encounter_type is EncounterType.Tree:
            return f"{self.region_id} Headbutt Trees ({str(self.rarity)})"
        elif self.encounter_type is EncounterType.Static:
            replacement_table = {
                "UnionCaveLapras": "Union Cave B2F (Static)",
                "EggTogepi": "Violet City (Egg from Aide)",
                "OddEgg": "Route 34 (Odd Egg)",
                "RocketHQTrap": "Rocket HQ (Trap)",
                "RocketHQElectrode": "Rocket HQ (Electrode)",
                "RedGyarados": "Lake of Rage (Static)",
                "Ho_Oh": "Tin Tower Roof (Static)",
                "Suicune": "Tin Tower 1F (Static)",
                "Lugia": "Whirl Islands Lugia Chamber (Static)",
                "Raikou": "Roaming",
                "Entei": "Roaming",
                "Sudowoodo": "Route 36 (Weird Tree)",
                "Snorlax": "Vermilion City (Static)",
                "CatchTutorial": "Catch Tutorial",
                "Kenya": "Route 35 (Gift from Guard)",
                "Celebi": "Ilex Forest (Shrine)",
                "Shuckie": "Cianwood City (Gift from Mania)",
                "Dratini": "Dragon's Den B1F (Gift from Elder)",
                "Eevee": "Goldenrod City (Gift from Bill)",
                "Tyrogue": "Mount Mortar B1F (Gift from Kiyo)",
                "GoldenrodGameCorner": "Goldenrod Game Corner (Prize)",
                "CeladonGameCornerPrizeRoom": "Celadon Game Corner (Prize)"
            }
            for key in [self.region_id, self.region_id[:-1]]:
                if key in replacement_table.keys():
                    return replacement_table[key]
            raise ValueError(f"Invalid static type: {self.region_id}")
        elif self.encounter_type is EncounterType.RockSmash:
            return "Rock Smash"
        else:
            raise ValueError(f"Invalid encounter type: {self.encounter_type}")

    def friendly_slot_region_name(self, slot_index: int, kanto: bool = True, route_23: bool = False):
        # shared fish slots are served at all times of day; label them without the Day suffix
        if self.encounter_type is EncounterType.Fish and self.time_of_day is FishTimeOfDay.Day:
            time_indexes = {i for i, _ in data.fish_time_slots[(self.region_id, self.fishing_rod)]}
            if slot_index not in time_indexes:
                return EncounterKey.fish(self.region_id, self.fishing_rod).friendly_region_name(kanto, route_23)
        return self.friendly_region_name(kanto, route_23)

    @staticmethod
    def grass(region_id: str, time_of_day: GrassTimeOfDay | None = None):
        return EncounterKey(EncounterType.Grass, region_id, time_of_day=time_of_day)

    @staticmethod
    def water(region_id: str):
        return EncounterKey(EncounterType.Water, region_id)

    @staticmethod
    def fish(region_id: str, fishing_rod: FishingRodType, time_of_day: "FishTimeOfDay | None" = None):
        return EncounterKey(EncounterType.Fish, region_id, fishing_rod=fishing_rod, time_of_day=time_of_day)

    @staticmethod
    def tree(region_id: str, rarity: TreeRarity):
        return EncounterKey(EncounterType.Tree, region_id, rarity=rarity)

    @staticmethod
    def rock_smash():
        return EncounterKey(EncounterType.RockSmash)

    @staticmethod
    def swarm(region_id: str):
        return EncounterKey(EncounterType.Swarm, region_id)

    @staticmethod
    def static(name: str):
        return EncounterKey(EncounterType.Static, name)

    @staticmethod
    def from_string(keystring: str):

        def resolve_components(expected_length: int) -> list[str]:
            components = keystring.split("_")
            if len(components) > expected_length:
                components = [components[0], "_".join(components[1:-1]), components[-1]]

            if len(components) > expected_length:
                components = [components[0], "_".join(components[1:])]
            return components

        if keystring.startswith(EncounterType.Grass):
            components = resolve_components(3)
            tod = GrassTimeOfDay.from_string(components[-1]) if len(components) == 3 else None
            if tod is not None:
                return EncounterKey.grass(components[1], tod)
            components = resolve_components(2)
            return EncounterKey(EncounterType.Grass, components[-1])
        elif keystring.startswith(EncounterType.Water):
            components = resolve_components(2)
            return EncounterKey.water(components[-1])
        elif keystring.startswith(EncounterType.Fish):
            parts = keystring.split("_")
            rod_names = {rod.value for rod in FishingRodType}
            tod_names = {tod.value for tod in FishTimeOfDay}
            if len(parts) >= 4 and parts[-1] in tod_names and parts[-2] in rod_names:
                return EncounterKey.fish("_".join(parts[1:-2]), FishingRodType(parts[-2]), FishTimeOfDay(parts[-1]))
            return EncounterKey.fish("_".join(parts[1:-1]), FishingRodType(parts[-1]))
        elif keystring.startswith(EncounterType.Tree):
            components = resolve_components(3)
            return EncounterKey.tree(components[1],
                                     next(rarity for rarity in TreeRarity if rarity == components[2]))
        elif keystring.startswith(EncounterType.RockSmash):
            return EncounterKey.rock_smash()
        elif keystring.startswith(EncounterType.Swarm):
            components = resolve_components(2)
            return EncounterKey.swarm(components[-1])
        elif keystring.startswith(EncounterType.Static):
            components = resolve_components(2)
            return EncounterKey.static(components[-1])
        else:
            raise ValueError(f"Invalid encounter type: {keystring}")


class LogicalAccess(Enum):
    InLogic = 0
    OutOfLogic = 1
    Inaccessible = 2


@dataclass(frozen=True)
class StaticPokemon:
    name: str
    pokemon: str
    addresses: list[str]
    level: int
    level_type: str
    level_address: str | None


@dataclass(frozen=True)
class TradeData:
    id: str
    index: int
    requested_pokemon: str
    received_pokemon: str
    requested_gender: int
    held_item: str
    ot_id: int
    friendly_name: str


@dataclass(frozen=True)
class RegionWildEncounterData:
    grass: str | None
    surfing: str | None
    fishing: str | None
    headbutt: str | None
    rock_smash: bool


@dataclass(frozen=True)
class RegionData:
    name: str
    johto: bool
    elite_4: bool
    silver_cave: bool
    east_west_underground: bool
    route_23_restored: bool
    flooded_mine: bool
    exits: list[str]
    trainers: list[TrainerData]
    statics: list[EncounterKey]
    locations: list[str]
    events: list[EventData]
    wild_encounters: RegionWildEncounterData | None
    marts: list[str]
    trades: list[str]
    signs: list[str]


@dataclass(frozen=True)
class StartingTown:
    id: int
    name: str
    region_id: str
    johto: bool
    restrictive_start: bool = False
    pokecenter_region: str | None = None


@dataclass(frozen=True)
class FlyRegion:
    id: int
    name: str
    base_identifier: str
    unlock_region: str
    exit_region: str
    johto: bool
    exclude_vanilla_start: bool = False
    unlock_sources: tuple[str, ...] = ()

    @property
    def spawn_flag(self) -> int:
        return self.id - 1


@dataclass(frozen=True)
class PhoneScriptData:
    name: str
    caller: str
    script: list[str]


@dataclass(frozen=True)
class PokemonCrystalGameSetting:
    option_byte_index: int
    offset: int
    length: int
    values: Mapping[str, int]
    default: int

    @staticmethod
    def normalize(option_selection: Any) -> Any:
        if option_selection is True:
            return "on"
        if option_selection is False:
            return "off"
        if isinstance(option_selection, int):
            return str(option_selection)
        return option_selection

    def set_option_byte(self, option_selection: str | None, option_bytes: bytearray):
        value = self.values.get(self.normalize(option_selection), self.default)
        mask = ((self.length * 2) - 1) << self.offset
        value = (value << self.offset) & mask

        option_bytes[self.option_byte_index] &= ~mask
        option_bytes[self.option_byte_index] |= value


ON_OFF = {"off": 0, "on": 1}
INVERTED_ON_OFF = {"off": 1, "on": 0}


class MapPalette(IntEnum):
    Auto = 0
    Day = 1
    Nite = 2
    Morn = 3
    Dark = 4

    @staticmethod
    def from_string(palette_string: str):
        if palette_string == "PALETTE_AUTO": return MapPalette.Auto
        if palette_string == "PALETTE_DAY": return MapPalette.Day
        if palette_string == "PALETTE_NITE": return MapPalette.Nite
        if palette_string == "PALETTE_MORN": return MapPalette.Morn
        if palette_string == "PALETTE_DARK": return MapPalette.Dark
        raise ValueError(f"Invalid palette string: {palette_string}")


class MapEnvironment(IntEnum):
    Town = 1
    Route = 2
    Indoor = 3
    Cave = 4
    IndoorEscapable = 5
    Gate = 6
    Dungeon = 7

    @staticmethod
    def from_string(map_env_string: str):
        if map_env_string == "TOWN": return MapEnvironment.Town
        if map_env_string == "ROUTE": return MapEnvironment.Route
        if map_env_string == "INDOOR": return MapEnvironment.Indoor
        if map_env_string == "CAVE": return MapEnvironment.Cave
        if map_env_string == "INDOOR_ESCAPABLE": return MapEnvironment.IndoorEscapable
        if map_env_string == "GATE": return MapEnvironment.Gate
        if map_env_string == "DUNGEON": return MapEnvironment.Dungeon
        raise ValueError(f"Invalid map environment string: {map_env_string}")


HM_COMPAT_TMS = ["HEADBUTT", "ROCK_SMASH"]

# Maps the player walks around on outdoors. Everything else is inside a building,
# cave or gate, which is what tells the two sides of a door apart.
OUTDOOR_ENVIRONMENTS = frozenset({MapEnvironment.Town, MapEnvironment.Route})


class Landmark(IntEnum):
    Special = 0
    NewBarkTown = auto()
    Route29 = auto()
    CherrygroveCity = auto()
    FloodedMine = auto()
    Route30 = auto()
    Route31 = auto()
    VioletCity = auto()
    SproutTower = auto()
    Route32 = auto()
    RuinsOfAlph = auto()
    UnionCave = auto()
    Route33 = auto()
    AzaleaTown = auto()
    SlowpokeWell = auto()
    IlexForest = auto()
    Route34 = auto()
    GoldenrodCity = auto()
    RadioTower = auto()
    Route35 = auto()
    NationalPark = auto()
    Route36 = auto()
    Route37 = auto()
    EcruteakCity = auto()
    TinTower = auto()
    BurnedTower = auto()
    Route38 = auto()
    Route39 = auto()
    OlivineCity = auto()
    Lighthouse = auto()
    BattleTower = auto()
    Route40 = auto()
    WhirlIslands = auto()
    Route41 = auto()
    CianwoodCity = auto()
    Route42 = auto()
    MtMortar = auto()
    MahoganyTown = auto()
    Route43 = auto()
    LakeOfRage = auto()
    Route44 = auto()
    IcePath = auto()
    BlackthornCity = auto()
    DragonsDen = auto()
    Route45 = auto()
    DarkCave = auto()
    Route46 = auto()
    SilverCave = auto()
    PalletTown = auto()
    Route1 = auto()
    ViridianCity = auto()
    Route2 = auto()
    PewterCity = auto()
    Route3 = auto()
    MtMoon = auto()
    Route4 = auto()
    CeruleanCity = auto()
    Route24 = auto()
    Route25 = auto()
    Route5 = auto()
    UndergroundPath = auto()
    Route6 = auto()
    VermilionCity = auto()
    DiglettsCave = auto()
    Route7 = auto()
    Route8 = auto()
    Route9 = auto()
    RockTunnel = auto()
    Route10 = auto()
    PowerPlant = auto()
    LavenderTown = auto()
    LavRadioTower = auto()
    CeladonCity = auto()
    SaffronCity = auto()
    Route11 = auto()
    Route12 = auto()
    Route13 = auto()
    Route14 = auto()
    Route15 = auto()
    Route16 = auto()
    Route17 = auto()
    Route18 = auto()
    FuchsiaCity = auto()
    Route19 = auto()
    Route20 = auto()
    SeafoamIslands = auto()
    CinnabarIsland = auto()
    Route21 = auto()
    Route22 = auto()
    VictoryRoad = auto()
    Route23 = auto()
    IndigoPlateau = auto()
    Route26 = auto()
    Route27 = auto()
    TohjoFalls = auto()
    Route28 = auto()
    FastShip = auto()

    @staticmethod
    def from_string(landmark_string: str):
        try:
            return Landmark["".join(s.title() for s in landmark_string.split("_"))]
        except KeyError:
            raise ValueError(f"Invalid Landmark string: {landmark_string}")

    @staticmethod
    def johto_only():
        landmarks = [l for l in list(Landmark) if Landmark.Special < l < Landmark.PalletTown]
        landmarks.extend([l for l in list(Landmark) if Landmark.Route22 < l < Landmark.FastShip])
        return landmarks

    @staticmethod
    def all():
        return [l for l in list(Landmark) if Landmark.Special < l < Landmark.FastShip]


@dataclass(frozen=True)
class MapData:
    name: str
    environment: MapEnvironment
    phone_service: bool
    palette: MapPalette
    landmark: Landmark
    width: int
    height: int


@dataclass(frozen=True)
class GrassTile:
    name: str
    xcoord: int
    ycoord: int
    rom_address: int
    flag: int


@dataclass(frozen=True)
class ManifestData:
    game: str
    world_version: str
    pokemon_crystal_version: str | None
    minimum_patch_version: str


@dataclass(frozen=True)
class BugContestEncounter:
    percentage: int
    pokemon: str
    min_level: int
    max_level: int


@dataclass(frozen=True)
class PaletteData:
    NPC_PAL_OFFSET = 8
    PRIORITY = 0x80
    name: str
    index: int
    id: str
    battle_palette: list[int]


@dataclass(frozen=True)
class UnownSignData:
    name: str
    address: int
    id: int


@dataclass(frozen=True)
class PokemonCrystalData:
    manifest: ManifestData
    rom_version: int
    rom_version_11: int
    rom_addresses: Mapping[str, int]
    ram_addresses: Mapping[str, int]
    sram_addresses: Mapping[str, int]
    event_flags: Mapping[str, int]
    engine_flags: Mapping[str, int]
    mart_flag_offset: int
    regions: Mapping[str, RegionData]
    locations: Mapping[str, LocationData]
    items: Mapping[int, ItemData]
    pocket_sizes: Mapping[str, int]
    max_item_stack: int
    trainers: Mapping[str, TrainerData]
    pokemon: Mapping[str, PokemonData]
    moves: Mapping[str, MoveData]
    types: Mapping[str, TypeData]
    wild: Mapping[EncounterKey, Sequence[EncounterMon]]
    fish_time_slots: Mapping[tuple[str, FishingRodType], Sequence[tuple[int, int]]]
    fish_rates: Mapping[tuple[str, FishingRodType], Sequence[int]]
    tmhm: Mapping[str, TMHMData]
    maps: Mapping[str, MapData]
    marts: Mapping[str, MartData]
    misc: MiscData
    music: MusicData
    static: Mapping[EncounterKey, StaticPokemon]
    trades: Mapping[str, TradeData]
    fly_regions: Sequence[FlyRegion]
    starting_towns: Sequence[StartingTown]
    game_settings: Mapping[str, PokemonCrystalGameSetting]
    phone_scripts: Sequence[PhoneScriptData]
    request_pokemon: Sequence[str]
    adhoc_trainersanity: Mapping[int, int]
    grass_tiles: Mapping[str, list[GrassTile]]
    grass_regions: Mapping[str, list[str]]
    bug_contest_encounters: Sequence[BugContestEncounter]
    palettes: Sequence[PaletteData]
    unown_signs: Mapping[str, UnownSignData]
    entrance_connections: Mapping[str, "EntranceConnection"]
    map_constants: Mapping[str, tuple[int, int]]      # MAP_CONST → (group, map_id)
    flypoints: Mapping[Landmark, list["FlypointWarp"]]
    spawnpoints: Sequence["SpawnPoint"]  # entries from SPAWN_HOME onward


@dataclass(frozen=True)
class SpawnPoint:
    map_group: int
    map_number: int
    x: int
    y: int

    def to_bytes(self) -> list[int]:
        return [self.map_group, self.map_number, self.x, self.y]


@dataclass(frozen=True)
class Warp:
    map_name: str
    warp_index: int        # 1-based, matches AP_Warp_<Map>_<N> label


@dataclass(frozen=True)
class FlypointWarp(Warp):
    x: int
    y: int
    warp_type: str

    DOWNPUSH_TILES = ["DOOR", "CAVE", "STAIRCASE", "WALL"]

    def spawn_data(self) -> list[int]:
        map_const_name = sub(r"([A-Z0-9]+)", r"_\1", self.map_name).lstrip("_").upper()
        if "ROUTE_10" in map_const_name: map_const_name = map_const_name.replace("10", "10_")
        if "ROUTE_23RESTORED" in map_const_name: map_const_name = map_const_name.replace("23RESTORED", "23_RESTORED")
        adjusted_y = self.y + (1 if self.warp_type in FlypointWarp.DOWNPUSH_TILES else 0)
        return [*data.map_constants[map_const_name], self.x, adjusted_y]


def is_flag_backed_warp(warp: dict) -> bool:
    """warp_ids.json record with a wWarpFlags bit (tile and elevator kinds)."""
    return warp["kind"] != "spawn"


def is_tile_warp(warp: dict) -> bool:
    """warp_ids.json record for a physical warp_event tile."""
    return warp["kind"] == "tile"


@dataclass(frozen=True)
class EntranceWarp(Warp):
    label: str | None = None       # explicit ROM label (overrides AP_Warp_ construction)
    addr_offset: int = 2   # byte offset to patchable warp data (2 for warp_event; 1/4 for elevfloor exit/entry map)
    warp_id: int | None = None  # canonical id, resolved at generation; None = not a traversal source


@dataclass(frozen=True)
class EntranceConnection:
    name: str
    exit_region: str
    entrance_region: str
    exit_warps: tuple[EntranceWarp, ...]
    arrival_map: str       # CamelCase map filename
    arrival_map_const: str # MAP_CONST key for map_constants lookup
    arrival_warp_index: int
    category: str          # one of the categories defined in entrance_types.json
    area: str              # johto / kanto
    one_way: bool


def _read_package_file(path: str) -> str:
    raw = pkgutil.get_data(__name__, path)
    if raw is None:
        raise FileNotFoundError(f"missing packaged file: {path}")
    return raw.decode('utf-8-sig')


def load_json_data(data_name: str) -> dict[str, Any]:
    return orjson.loads(_read_package_file("data/" + data_name))


def load_yaml_data(data_name: str) -> dict[str, Any]:
    return yaml.safe_load(_read_package_file("data/" + data_name))


def load_manifest() -> dict[str, Any]:
    return orjson.loads(_read_package_file("archipelago.json"))


def _parse_encounters(encounter_list: list) -> Sequence[EncounterMon]:
    return [EncounterMon(int(pkmn["level"]), pkmn["pokemon"]) for pkmn in encounter_list]


_friendly_connection_json = load_json_data("friendly_connection_names.json")
FRIENDLY_CONNECTION_NAMES: dict[str, str] = _friendly_connection_json["names"]
# option name -> option value key -> {connection: name}, for connections whose display
# name depends on world options. Resolved per world in _friendly_name_overrides.
FRIENDLY_CONNECTION_NAME_OVERRIDES: dict[str, dict[str, dict[str, str]]] = \
    _friendly_connection_json["option_overrides"]
# Keyed lowercase: PlandoConnections validation is case-insensitive, so resolution must be too.
_CONNECTIONS_BY_FRIENDLY_NAME: dict[str, str] = {v.lower(): k for k, v in FRIENDLY_CONNECTION_NAMES.items()}
_CONNECTIONS_BY_FRIENDLY_NAME.update({name.lower(): conn
                                      for columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.values()
                                      for overrides in columns.values()
                                      for conn, name in overrides.items()})
_CONNECTIONS_BY_FRIENDLY_NAME.update({conn.lower(): conn for conn in FRIENDLY_CONNECTION_NAMES})

ONE_WAY_TARGET_SUFFIX = " (one-way target)"


def friendly_entrance_name(connection_name: str) -> str:
    """Display name for a region connection; falls back to the internal name."""
    if connection_name.endswith(ONE_WAY_TARGET_SUFFIX):
        return friendly_entrance_name(connection_name.removesuffix(ONE_WAY_TARGET_SUFFIX)) + ONE_WAY_TARGET_SUFFIX
    return FRIENDLY_CONNECTION_NAMES.get(connection_name, connection_name)


def internal_entrance_name(name: str) -> str:
    """Canonical connection name for either a friendly or an internal name."""
    if name.endswith(ONE_WAY_TARGET_SUFFIX):
        return internal_entrance_name(name.removesuffix(ONE_WAY_TARGET_SUFFIX)) + ONE_WAY_TARGET_SUFFIX
    return _CONNECTIONS_BY_FRIENDLY_NAME.get(name.lower(), name)


# Friendly names for outdoor maps that have entrance warps, to be used by Fly Destination Plando/Blocklist
OUTDOOR_WARP_MAP_FRIENDLY_NAMES: list[str] = [
    "New Bark Town", "Route 29",
    "Cherrygrove City", "Route 30", "Route 31",
    "Violet City", "Route 32", "Route 36", "Ruins of Alph Outside",
    "Azalea Town", "Route 33",
    "Goldenrod City", "Route 34", "Route 35", # "National Park",
    "Ecruteak City", "Route 38", "Route 39", "Route 42", "Tin Tower Roof",
    "Olivine City", "Olivine Port", "Route 40", "Battle Tower Outside",
    "Cianwood City", "Route 41",
    "Mahogany Town", "Route 43", "Route 44", "Lake of Rage",
    "Blackthorn City", "Route 45", "Route 46",
    "Route 23", "Route 23 Restored", "Route 26", "Route 27",
    "Silver Cave Outside", "Route 28",
    "Pallet Town", "Viridian City", "Route 2", "Route 22",
    "Pewter City", "Route 3", "Mount Moon Square",
    "Cerulean City", "Route 4", "Route 5", "Route 9", "Route 10 North", "Route 25",
    "Vermilion City", "Vermilion Port", "Route 6",
    "Lavender Town", "Route 8", "Route 10 South", "Route 12",
    "Celadon City", "Route 7", "Route 16",
    "Saffron City",
    "Fuchsia City", "Route 15", "Route 17", "Route 18", "Route 19",
    "Cinnabar Island", "Route 20"
]


data: PokemonCrystalData


def _init() -> None:
    location_data = load_json_data("locations.json")
    regions_json = load_json_data("regions.json")
    items_json = load_json_data("items.json")
    data_json = load_json_data("data.json")
    manifest_json = load_manifest()
    rom_address_data = data_json["rom_addresses"]
    ram_address_data = data_json["ram_addresses"]
    sram_address_data = data_json.get("sram_addresses", {})
    event_flag_data = data_json["event_flags"]
    engine_flag_data = data_json["engine_flags"]
    item_codes = data_json["items"]
    item_pockets = data_json["item_pockets"]
    move_data = data_json["moves"]
    trainer_data = data_json["trainers"]
    wild_data = data_json["wilds"]
    fuchsia_data = data_json["misc"]["fuchsia_gym_trainers"]
    saffron_data = data_json["misc"]["saffron_gym_warps"]
    radio_addr_data = data_json["misc"]["radio_channel_addresses"]
    mom_items_data = data_json["misc"]["mom_items"]
    tmhm_data = data_json["tmhm"]
    mart_data = data_json["marts"]
    flag_items = data_json["flag_items"]

    claimed_locations: set[str] = set()

    trainers = {}

    for trainer_name, trainer_attributes in trainer_data.items():
        trainer_type = trainer_attributes["trainer_type"]
        pokemon = []
        for poke in trainer_attributes["pokemon"]:
            if trainer_type == "TRAINERTYPE_NORMAL":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, []))
            elif trainer_type == "TRAINERTYPE_ITEM":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], []))
            elif trainer_type == "TRAINERTYPE_MOVES":
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], None, poke[2:]))
            else:
                pokemon.append(TrainerPokemon(int(poke[0]), poke[1], poke[2], poke[3:]))

        trainers[trainer_name] = TrainerData(
            trainer_name,
            trainer_type,
            pokemon,
            trainer_attributes["name_length"]
        )

    statics = dict[EncounterKey, StaticPokemon]()
    for static_name, static_data in data_json["static"].items():
        static_key = EncounterKey(EncounterType.Static, static_name)
        level_type = static_data["type"]
        if level_type in ("loadwildmon", "givepoke", "gamecorner"):
            level_address = static_data["addresses"][0]
        elif level_type == "custom":
            level_address = static_data["level_address"]
        else:
            level_address = None
        statics[static_key] = StaticPokemon(
            static_name,
            static_data["pokemon"],
            static_data["addresses"],
            static_data["level"],
            static_data["type"],
            level_address
        )

    fly_regions = [
        FlyRegion(1, "New Bark Town", "NEW_BARK", "REGION_NEW_BARK_TOWN", "REGION_NEW_BARK_TOWN", True,
                  exclude_vanilla_start=True),
        FlyRegion(2, "Cherrygrove City", "CHERRYGROVE", "REGION_CHERRYGROVE_CITY:FLY", "REGION_CHERRYGROVE_CITY", True,
                  exclude_vanilla_start=True,
                  unlock_sources=("REGION_CHERRYGROVE_CITY:FLOODED_MINE_ENTRANCE",)),
        FlyRegion(3, "Violet City", "VIOLET", "REGION_VIOLET_CITY", "REGION_VIOLET_CITY", True,
                  exclude_vanilla_start=True),
        FlyRegion(4, "Azalea Town", "AZALEA", "REGION_AZALEA_TOWN:FLY", "REGION_AZALEA_TOWN", True,
                  unlock_sources=("REGION_AZALEA_TOWN:WELL",)),
        FlyRegion(5, "Goldenrod City", "GOLDENROD", "REGION_GOLDENROD_CITY", "REGION_GOLDENROD_CITY", True),
        FlyRegion(6, "Ecruteak City", "ECRUTEAK", "REGION_ECRUTEAK_CITY:FLY", "REGION_ECRUTEAK_CITY", True,
                  unlock_sources=("REGION_ECRUTEAK_CITY:TIN_TOWER_TRAIL",)),
        FlyRegion(7, "Olivine City", "OLIVINE", "REGION_OLIVINE_CITY", "REGION_OLIVINE_CITY", True),
        FlyRegion(8, "Cianwood City", "CIANWOOD", "REGION_CIANWOOD_CITY", "REGION_CIANWOOD_CITY", True),
        FlyRegion(9, "Mahogany Town", "MAHOGANY", "REGION_MAHOGANY_TOWN:FLY", "REGION_MAHOGANY_TOWN", True,
                  unlock_sources=("REGION_MAHOGANY_TOWN:EAST",)),
        FlyRegion(10, "Lake of Rage", "LAKE_OF_RAGE", "REGION_LAKE_OF_RAGE:FLY", "REGION_LAKE_OF_RAGE", True,
                  unlock_sources=("REGION_LAKE_OF_RAGE:HIDDEN_POWER_HOUSE",)),
        FlyRegion(11, "Blackthorn City", "BLACKTHORN", "REGION_BLACKTHORN_CITY:FLY", "REGION_BLACKTHORN_CITY", True,
                  unlock_sources=("REGION_BLACKTHORN_CITY:DRAGONS_DEN_ENTRANCE",)),
        FlyRegion(12, "Silver Cave", "MT_SILVER", "REGION_SILVER_CAVE_OUTSIDE", "REGION_SILVER_CAVE_OUTSIDE", True),

        FlyRegion(13, "Pallet Town", "PALLET", "REGION_PALLET_TOWN", "REGION_PALLET_TOWN", False),
        FlyRegion(14, "Viridian City", "VIRIDIAN", "REGION_VIRIDIAN_CITY", "REGION_VIRIDIAN_CITY", False),
        FlyRegion(15, "Pewter City", "PEWTER", "REGION_PEWTER_CITY", "REGION_PEWTER_CITY", False),
        FlyRegion(16, "Cerulean City", "CERULEAN", "REGION_CERULEAN_CITY", "REGION_CERULEAN_CITY", False),
        FlyRegion(17, "Vermilion City", "VERMILION", "REGION_VERMILION_CITY:FLY", "REGION_VERMILION_CITY", False,
                  unlock_sources=("REGION_VERMILION_CITY:GYM_ENTRANCE",
                                  "REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE", "REGION_ROUTE_11")),
        FlyRegion(18, "Lavender Town", "LAVENDER", "REGION_LAVENDER_TOWN", "REGION_LAVENDER_TOWN", False),
        FlyRegion(19, "Celadon City", "CELADON", "REGION_CELADON_CITY:FLY", "REGION_CELADON_CITY", False,
                  unlock_sources=("REGION_CELADON_CITY:GYM_ENTRANCE",)),
        FlyRegion(20, "Saffron City", "SAFFRON", "REGION_SAFFRON_CITY", "REGION_SAFFRON_CITY", False),
        FlyRegion(21, "Fuchsia City", "FUCHSIA", "REGION_FUCHSIA_CITY:FLY", "REGION_FUCHSIA_CITY", False,
                  unlock_sources=("REGION_FUCHSIA_CITY:CUT",)),
        FlyRegion(22, "Cinnabar Island", "CINNABAR", "REGION_CINNABAR_ISLAND", "REGION_CINNABAR_ISLAND", False),
        FlyRegion(23, "Indigo Plateau", "INDIGO", "REGION_ROUTE_23", "REGION_ROUTE_23", True)
    ]

    items = {}
    for item_constant_name, attributes in items_json.items():

        if attributes["classification"] == "PROGRESSION":
            item_classification = ItemClassification.progression
        elif attributes["classification"] == "USEFUL":
            item_classification = ItemClassification.useful
        elif attributes["classification"] == "FILLER":
            item_classification = ItemClassification.filler
        elif attributes["classification"] == "TRAP":
            item_classification = ItemClassification.trap
        else:
            raise ValueError(f"Unknown classification {attributes['classification']} for item {item_constant_name}")

        if attributes.get("deprioritized", False):
            item_classification |= ItemClassification.deprioritized

        if attributes.get("skip_balancing", False):
            item_classification |= ItemClassification.skip_balancing

        if item_constant_name in flag_items:
            flag_index = flag_items.index(item_constant_name)
            item_id = flag_index + FLAG_ITEM_OFFSET
            item_codes[item_constant_name] = item_id
        else:
            flag_index = None
            item_id = item_codes[item_constant_name]

        pocket = None if flag_index is not None else item_pockets.get(item_constant_name)
        if pocket is None and flag_index is None and "INVALID" not in attributes["tags"]:
            raise ValueError(f"Unknown pocket for item {item_constant_name}")

        items[item_id] = ItemData(
            label=attributes["name"],
            item_id=item_id,
            item_const=item_constant_name,
            price=attributes["price"],
            classification=item_classification,
            tags=frozenset(attributes["tags"]),
            flag_index=flag_index,
            pocket=pocket,
        )

        if "Fly Unlocks" in attributes["tags"]:
            items[item_id | (CANONICAL_ITEM_ID_MASK + 1)] = ItemData(
                label=f"Fly Unlock {flag_index}",
                item_id=item_id,
                item_const=f"FLY_UNLOCK_{flag_index}",
                price=attributes["price"],
                classification=item_classification,
                tags=frozenset(attributes["tags"]),
                flag_index=flag_index,
                pocket=pocket,
            )

    regions = dict[str, RegionData]()
    locations = dict[str, LocationData]()
    locations_to_regions = dict[str, str]()

    for region_name, region_json in regions_json.items():

        region_locations = []

        for location_name in region_json.get("locations", []):
            if location_name in claimed_locations:
                raise AssertionError(f"Location [{location_name}] was claimed by multiple regions")
            location_json: dict[str, Any] = location_data[location_name]
            new_location = LocationData(
                name=location_name,
                label=location_json["label"],
                parent_region=region_name,
                default_item=item_codes[location_json["default_item"]],
                rom_addresses=[rom_address_data[script] for script in location_json["scripts"]],
                flag=event_flag_data[location_json["flag"]],
                tags=frozenset(location_json["tags"] + (
                    ["Johto"] if region_json["johto"] or region_json.get("silver_cave") else ["Kanto"])),
                scripts=location_json["scripts"]
            )
            region_locations.append(location_name)
            locations[location_name] = new_location
            claimed_locations.add(location_name)
            locations_to_regions[location_name] = region_name

        region_locations.sort()

        new_region = RegionData(
            name=region_name,
            johto=region_json["johto"],
            elite_4=region_json.get("elite_4", False),
            silver_cave=region_json.get("silver_cave", False),
            east_west_underground=region_json.get("east_west_underground", False),
            route_23_restored=region_json.get("route_23_restored", False),
            flooded_mine=region_json.get("flooded_mine", False),
            exits=[region_exit for region_exit in region_json.get("exits", [])],
            statics=[EncounterKey(EncounterType.Static, static) for static in region_json.get("statics", [])],
            trainers=[trainers[trainer] for trainer in region_json.get("trainers", [])],
            events=[EventData(event, region_name) for event in region_json.get("events", [])],
            locations=region_locations,
            wild_encounters=RegionWildEncounterData(
                region_json["wild_encounters"].get("grass"),
                region_json["wild_encounters"].get("surfing"),
                region_json["wild_encounters"].get("fishing"),
                region_json["wild_encounters"].get("headbutt"),
                region_json["wild_encounters"].get("rock_smash")
            ) if "wild_encounters" in region_json else None,
            marts=region_json["marts"] if "marts" in region_json else [],
            trades=region_json["trades"] if "trades" in region_json else [],
            signs=region_json["signs"] if "signs" in region_json else [],
        )

        regions[region_name] = new_region

    # items

    pokemon = {}
    for pokemon_name, pokemon_data in data_json["pokemon"].items():
        evolutions = []
        for evo in pokemon_data["evolutions"]:
            evo_type = EvolutionType.from_string(evo[0])
            if len(evo) == 4:
                evolutions.append(EvolutionData(evo_type, int(evo[1]), evo[2], evo[3]))
            elif evo_type is EvolutionType.Level:
                evolutions.append(EvolutionData(evo_type, int(evo[1]), None, evo[2]))
            else:
                evolutions.append(EvolutionData(evo_type, None, evo[1], evo[2]))

        pokemon[pokemon_name] = PokemonData(
            pokemon_data["id"],
            pokemon_data["friendly_name"],
            pokemon_data["base_stats"],
            pokemon_data["types"],
            evolutions,
            [LearnsetData(move[0], move[1]) for move in pokemon_data["learnset"]],
            pokemon_data["tm_hm"],
            pokemon_data["is_base"],
            pokemon_data["bst"],
            pokemon_data["egg_groups"],
            pokemon_data["gender_ratio"],
            GrowthRate.from_string(pokemon_data["growth_rate"]),
            pokemon_data["produces_egg"],
        )

    moves = {
        move_name: MoveData(
            move_name,
            move_attributes["id"],
            move_attributes["type"],
            move_attributes["power"],
            move_attributes["accuracy"],
            move_attributes["pp"],
            move_attributes["is_hm"],
            move_attributes["name"],
            MoveCategory.from_string(move_attributes["category"]),
        ) for move_name, move_attributes in move_data.items()
    }

    types = {
        type_id: TypeData(
            id=type_id,
            rom_id=type_data["id"],
            matchups={
                matchup_id: TypeMatchup.from_string(matchup) for matchup_id, matchup in type_data["matchups"].items()
            }

        ) for type_id, type_data in data_json["types"].items()
    }

    wild = dict[EncounterKey, Sequence[EncounterMon]]()

    for grass_name, grass_data in wild_data["grass"].items():
        if grass_name.endswith("_Swarm"):
            continue
        for tod in GrassTimeOfDay:
            wild[EncounterKey.grass(grass_name, tod)] = _parse_encounters(
                grass_data[tod.name.lower()])

    for water_name, water_data in wild_data["water"].items():
        wild[EncounterKey.water(water_name)] = _parse_encounters(water_data)

    fish_time_slots: dict[tuple[str, FishingRodType], list[tuple[int, int]]] = {}
    fish_rates: dict[tuple[str, FishingRodType], list[int]] = {}
    for fish_name, fish_data in wild_data["fish"].items():
        if fish_name.endswith("_Swarm"):
            continue
        for rod in FishingRodType:
            rod_data = fish_data[rod.name]
            time_slots = sorted(
                (slot["slot_index"], slot["time_group_index"]) for slot in rod_data.get("time_slots", [])
            )
            fish_time_slots[(fish_name, rod)] = time_slots
            fish_rates[(fish_name, rod)] = list(rod_data.get("rates", []))
            if time_slots:
                wild[EncounterKey.fish(fish_name, rod, FishTimeOfDay.Day)] = _parse_encounters(rod_data["Day"])
                # Nite keys own only the time-varying slots; the rest are shared in the ROM with the Day key
                nite_encounters = _parse_encounters(rod_data["Nite"])
                wild[EncounterKey.fish(fish_name, rod, FishTimeOfDay.Nite)] = [
                    nite_encounters[slot_index] for slot_index, _ in time_slots]
            else:
                # No vanilla day/nite difference for this rod -> single un-suffixed key.
                wild[EncounterKey.fish(fish_name, rod)] = _parse_encounters(rod_data["Day"])

    for swarm_region_id, swarm_data in wild_data.get("swarm", {}).items():
        wild[EncounterKey.swarm(swarm_region_id)] = [
            EncounterMon(level=int(swarm_data["level"]), pokemon=swarm_data["pokemon"])
        ]

    for tree_name, tree_data in wild_data["tree"].items():
        if "rare" in tree_data:
            wild[EncounterKey.tree(tree_name, TreeRarity.Common)] = _parse_encounters(tree_data["common"])
            wild[EncounterKey.tree(tree_name, TreeRarity.Rare)] = _parse_encounters(tree_data["rare"])
        else:
            wild[EncounterKey.rock_smash()] = _parse_encounters(tree_data["common"])

    saffron_warps = {warp_name: MiscWarp(warp_data["coords"], warp_data["id"]) for warp_name, warp_data in
                     saffron_data["warps"].items()}

    radio_tower_data = ["Y", "Y", "N", "Y", "N"]

    mom_items = [MiscMomItem(item["index"], item["item"]) for item in mom_items_data]

    misc = MiscData(fuchsia_data, radio_tower_data, MiscSaffronWarps(saffron_warps, saffron_data["pairs"]),
                    radio_addr_data, mom_items)

    tmhm = {tm_name: TMHMData(
        tm_name,
        tm_data["tm_num"],
        tm_data["type"],
        tm_data["is_hm"],
        move_data[tm_name]["id"]
    ) for tm_name, tm_data in tmhm_data.items()}

    mart_categories = {mart: category for category, marts in MART_CATEGORIES.items() for mart in marts}

    marts = {mart_name: MartData(
        mart_data["index"],
        FRIENDLY_MART_NAMES[mart_name],
        mart_categories[mart_name],
        [MartItemData(entry["item"], entry["price"], event_flag_data[entry["flag"]] if "flag" in entry else None,
                      rom_address_data[mart_data["address"]] + (i * 5) + 1)
         for i, entry in enumerate(mart_data["items"])]
    ) for mart_name, mart_data in mart_data.items()}

    music_consts = {music_name: MusicConst(music_data["id"], music_data["loop"]) for music_name, music_data in
                    data_json["music"]["consts"].items()}

    music_maps = {map_name: music_name for map_name, music_name in data_json["music"]["maps"].items()}

    music = MusicData(music_consts,
                      music_maps,
                      data_json["music"]["encounters"],
                      data_json["music"]["scripts"])

    trades = {trade_data["id"]: TradeData(
        trade_data["id"],
        trade_data["index"],
        trade_data["requested_pokemon"],
        trade_data["received_pokemon"],
        trade_data["requested_gender"],
        trade_data["held_item"],
        trade_data["ot_id"],
        trade_data["friendly_name"]
    ) for trade_data in data_json["trade"]}

    starting_towns = [
        StartingTown(25, "Pallet Town", "REGION_PALLET_TOWN", False, restrictive_start=True, pokecenter_region="REGION_VIRIDIAN_CITY"),
        StartingTown(26, "Viridian City", "REGION_VIRIDIAN_CITY", False, restrictive_start=True, pokecenter_region="REGION_VIRIDIAN_CITY"),
        StartingTown(27, "Pewter City", "REGION_PEWTER_CITY", False, restrictive_start=True, pokecenter_region="REGION_PEWTER_CITY"),
        StartingTown(28, "Cerulean City", "REGION_CERULEAN_CITY", False, restrictive_start=True, pokecenter_region="REGION_CERULEAN_CITY"),
        StartingTown(29, "Rock Tunnel", "REGION_ROUTE_9", False, restrictive_start=True, pokecenter_region="REGION_ROUTE_10_NORTH:POKECENTER"),
        StartingTown(30, "Vermilion City", "REGION_VERMILION_CITY", False, restrictive_start=True, pokecenter_region="REGION_VERMILION_CITY"),
        StartingTown(31, "Lavender Town", "REGION_LAVENDER_TOWN", False, restrictive_start=True, pokecenter_region="REGION_LAVENDER_TOWN"),
        StartingTown(32, "Saffron City", "REGION_SAFFRON_CITY", False, pokecenter_region="REGION_SAFFRON_CITY"),
        StartingTown(33, "Celadon City", "REGION_CELADON_CITY", False, restrictive_start=True, pokecenter_region="REGION_CELADON_CITY"),
        StartingTown(34, "Fuchsia City", "REGION_FUCHSIA_CITY", False, restrictive_start=True, pokecenter_region="REGION_FUCHSIA_CITY"),
        # StartingTown(35, "Cinnabar Island", "REGION_CINNABAR_ISLAND", False, restrictive_start=True),

        StartingTown(37, "New Bark Town", "REGION_NEW_BARK_TOWN", True, pokecenter_region="REGION_CHERRYGROVE_CITY"),
        StartingTown(38, "Cherrygrove City", "REGION_CHERRYGROVE_CITY", True, pokecenter_region="REGION_CHERRYGROVE_CITY"),
        StartingTown(39, "Violet City", "REGION_VIOLET_CITY", True, pokecenter_region="REGION_VIOLET_CITY"),
        StartingTown(40, "Union Cave", "REGION_ROUTE_32:SOUTH", True, pokecenter_region="REGION_ROUTE_32:SOUTH"),
        StartingTown(41, "Azalea Town", "REGION_AZALEA_TOWN", True, pokecenter_region="REGION_AZALEA_TOWN"),
        StartingTown(42, "Cianwood City", "REGION_CIANWOOD_CITY", True, restrictive_start=True, pokecenter_region="REGION_CIANWOOD_CITY"),
        StartingTown(43, "Goldenrod City", "REGION_GOLDENROD_CITY", True, pokecenter_region="REGION_GOLDENROD_CITY"),
        StartingTown(44, "Olivine City", "REGION_OLIVINE_CITY", True, pokecenter_region="REGION_OLIVINE_CITY"),
        StartingTown(45, "Ecruteak City", "REGION_ECRUTEAK_CITY", True, pokecenter_region="REGION_ECRUTEAK_CITY"),
        StartingTown(46, "Mahogany Town", "REGION_MAHOGANY_TOWN", True, pokecenter_region="REGION_MAHOGANY_TOWN"),
        StartingTown(47, "Lake of Rage", "REGION_LAKE_OF_RAGE", True, pokecenter_region="REGION_MAHOGANY_TOWN"),
        StartingTown(48, "Blackthorn City", "REGION_BLACKTHORN_CITY", True, pokecenter_region="REGION_BLACKTHORN_CITY"),
    ]

    game_settings = {
        "text_speed": PokemonCrystalGameSetting(0, 0, 2, {"instant": 0, "fast": 1, "mid": 2, "slow": 3}, 2),
        "battle_shift": PokemonCrystalGameSetting(0, 3, 1, {"shift": 1, "set": 0}, 1),
        "battle_animations": PokemonCrystalGameSetting(0, 4, 2,
                                                       {"all": 0, "no_scene": 1, "no_bars": 2, "speedy": 3}, 0),
        "sound": PokemonCrystalGameSetting(0, 6, 1, {"mono": 0, "stereo": 1}, 0),
        "menu_account": PokemonCrystalGameSetting(0, 7, 1, ON_OFF, 1),

        "text_frame": PokemonCrystalGameSetting(1, 0, 4, dict([(f"{x + 1}", x) for x in range(8)]), 0),
        "bike_music": PokemonCrystalGameSetting(1, 4, 1, INVERTED_ON_OFF, 0),
        "surf_music": PokemonCrystalGameSetting(1, 5, 1, INVERTED_ON_OFF, 0),
        "skip_nicknames": PokemonCrystalGameSetting(1, 6, 1, ON_OFF, 0),
        "auto_run": PokemonCrystalGameSetting(1, 7, 1, ON_OFF, 0),

        "scaling_exp": PokemonCrystalGameSetting(2, 0, 1, ON_OFF, 0),
        "fast_egg_hatch": PokemonCrystalGameSetting(2, 1, 1, ON_OFF, 0),
        "fast_egg_make": PokemonCrystalGameSetting(2, 2, 1, ON_OFF, 0),
        "rods_always_work": PokemonCrystalGameSetting(2, 3, 1, ON_OFF, 0),
        "catch_exp": PokemonCrystalGameSetting(2, 4, 1, ON_OFF, 0),
        "poison_flicker": PokemonCrystalGameSetting(2, 5, 1, INVERTED_ON_OFF, 0),
        "low_hp_beep": PokemonCrystalGameSetting(2, 6, 1, INVERTED_ON_OFF, 0),
        "battle_move_stats": PokemonCrystalGameSetting(2, 7, 1, ON_OFF, 0),

        "time_of_day": PokemonCrystalGameSetting(3, 0, 2, {"auto": 0, "morn": 1, "day": 2, "nite": 3}, 0),
        "exp_distribution": PokemonCrystalGameSetting(3, 2, 2, {"gen2": 0, "gen6": 1, "gen8": 2, "no_exp": 3}, 0),
        "turbo_button": PokemonCrystalGameSetting(3, 4, 2, {"none": 0, "a": 1, "b": 2, "a_or_b": 3}, 0),
        "short_fanfares": PokemonCrystalGameSetting(3, 6, 1, ON_OFF, 0),
        "dex_area_beep": PokemonCrystalGameSetting(3, 7, 1, ON_OFF, 0),

        "skip_dex_registration": PokemonCrystalGameSetting(4, 0, 1, ON_OFF, 0),
        "blind_trainers": PokemonCrystalGameSetting(4, 1, 1, ON_OFF, 0),
        "guaranteed_catch": PokemonCrystalGameSetting(4, 2, 1, ON_OFF, 0),
        # byte 4 bit 3 (old ap_item_sound) is now spare; AP item notification moved to byte 6
        "_death_link": PokemonCrystalGameSetting(4, 4, 1, ON_OFF, 0),
        "trainersanity_indication": PokemonCrystalGameSetting(4, 5, 1, ON_OFF, 0),
        "more_uncaught_encounters": PokemonCrystalGameSetting(4, 6, 1, ON_OFF, 0),
        "auto_hms": PokemonCrystalGameSetting(4, 7, 1, ON_OFF, 0),

        "hms_require_teaching": PokemonCrystalGameSetting(5, 0, 1, ON_OFF, 1),
        "local_item_notification": PokemonCrystalGameSetting(5, 1, 2, {"text": 0, "sound": 1, "none": 2}, 0),
        "_trap_link": PokemonCrystalGameSetting(5, 3, 1, ON_OFF, 0),
        "spinners": PokemonCrystalGameSetting(5, 4, 2, {"normal": 0, "rotators": 1, "heck": 2, "hell": 3}, 0),
        "battle_always_run": PokemonCrystalGameSetting(5, 6, 1, ON_OFF, 0),
        "music": PokemonCrystalGameSetting(5, 7, 1, INVERTED_ON_OFF, 0),

        "ap_item_notification": PokemonCrystalGameSetting(6, 0, 2, {"popup_sound": 0, "popup": 1, "sound": 2, "none": 3}, 0),
    }

    phone_scripts = []
    phone_yaml = load_yaml_data("phone_data.yaml")
    for script_name, script_data in phone_yaml.items():
        try:
            phone_scripts.append(
                PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))
        except Exception as ex:
            raise ValueError(f"Error processing phone script '{script_name}': {ex}") from ex

    adhoc_trainersanity = {}

    adhoc_trainers = [f"ITEM_FROM_{trainer}" for trainer in data_json["adhoc_trainersanity"]]

    for loc_id, loc_data in locations.items():
        if loc_id in adhoc_trainers:
            adhoc_trainersanity[loc_data.rom_addresses[0]] = rom_address_data[f"AP_AdhocTrainersanity_{loc_id}"]

    maps = {}

    for map_name, map_data in data_json["maps"].items():
        size = map_data["size"]
        maps[map_name] = MapData(
            map_name,
            MapEnvironment.from_string(map_data["environment"]),
            map_data["phone_service"],
            MapPalette.from_string(map_data["palette"]),
            Landmark.from_string(map_data["landmark"]),
            size[0],
            size[1]
        )

    grass_tiles = {}
    grass_regions = defaultdict(list)

    grass_base_rom_addr = rom_address_data["AP_Setting_GrassTable"]

    for region, tile_data in data_json["grasssanity"].items():
        region_name = region.split(":")[0][7:]  # delete REGION_
        region_name = region_name.lower().replace("_", " ").title()
        if region_name == "Route 23 Restored":
            region_name = "Route 23"
        region_name_regular = f"{region_name} - Grass"
        region_name_long = f"{region_name} - Long Grass"
        tiles = []
        grass_regions[region_name_regular].append(region)
        for tile in tile_data:
            index = tile["index"]
            x = tile["x"]
            y = tile["y"]
            rom_address = grass_base_rom_addr + (index * 5) + 4
            grass_region_name = region_name_regular
            if tile["long"]:
                rom_address += 1  # account for regular grass terminator
                grass_region_name = region_name_long
            tiles.append(
                GrassTile(
                    name=f"{grass_region_name} ({x}, {y})",
                    xcoord=x,
                    ycoord=y,
                    rom_address=rom_address,
                    flag=GRASS_OFFSET + index,
                )
            )

        grass_tiles[region] = tiles

    bug_contest_encounters = [
        BugContestEncounter(
            percentage=encounter_data["percentage"],
            pokemon=encounter_data["pokemon"],
            min_level=encounter_data["min_level"],
            max_level=encounter_data["max_level"],
        ) for encounter_data in data_json["bug_contest"]
    ]

    manifest = ManifestData(
        game=manifest_json["game"],
        world_version=manifest_json["world_version"],
        pokemon_crystal_version=manifest_json.get("pokemon_crystal_version", manifest_json["world_version"]),
        minimum_patch_version=manifest_json["minimum_patch_version"]
    )

    palettes = [
        PaletteData(
            name=palette_data["name"],
            index=palette_data["index"],
            id=palette_data["id"],
            battle_palette=palette_data["battle_palette"]
        ) for palette_data in data_json["palettes"]
    ]

    unown_signs = {
        sign_data["name"]: UnownSignData(
            name=sign_data["name"],
            address=rom_address_data[sign_data["address"]],
            id=sign_data["id"]
        ) for sign_data in data_json["unown_signs"]
    }

    request_pokemon = [
        "LICKITUNG",
        "ODDISH",
        "STARYU",
        "GROWLITHE",
        "PICHU",
        "MARILL",
        "PIKACHU",
        "CLEFAIRY"
    ]

    global data
    entrance_data_json = load_json_data("entrance_data.json")
    entrance_types_json: dict[str, str] = load_json_data("entrance_types.json")
    entrance_connections: dict[str, EntranceConnection] = {}
    for c in entrance_data_json["connections"]:
        conn_name = c["name"]
        if conn_name not in entrance_types_json:
            raise ValueError(
                f"entrance_types.json is missing an entry for connection '{conn_name}'. "
                f"Run the migration script or add it manually."
            )
        exit_warps = tuple(
            EntranceWarp(w["map"], w["index"], w.get("label"), w.get("addr_offset", 2), w.get("warp_id"))
            for w in c["exit_warps"]
        )
        entrance_connections[conn_name] = EntranceConnection(
            name=conn_name,
            exit_region=c["exit_region"],
            entrance_region=c["entrance_region"],
            exit_warps=exit_warps,
            arrival_map=c["arrival_map"],
            arrival_map_const=c.get("arrival_map_const", ""),
            arrival_warp_index=c["arrival_warp_index"],
            category=entrance_types_json[conn_name],
            area=c["area"],
            one_way=c.get("one_way", False),
        )

    map_constants: dict[str, tuple[int, int]] = {
        name: tuple(pair) for name, pair in data_json["map_constants"].items()
    }

    # extracted from vanilla blks; rom.py paints these warp tiles at generation
    PATCHED_WARP_TYPES = {("CherrygroveCity", 6): "CAVE"}

    flypoints: dict[Landmark, list[FlypointWarp]] = defaultdict(list)
    for map_name, map_data in maps.items():
        if data_json["warps"].get(map_name, None) is None: continue
        flypoints[map_data.landmark].extend(FlypointWarp(map_name,
                                                         warp["index"],
                                                         warp["x"],
                                                         warp["y"],
                                                         PATCHED_WARP_TYPES.get((map_name, warp["index"]),
                                                                                warp["warp_type"])
                                                         )
                                            for warp in data_json["warps"][map_name]
                                            if map_data.environment in OUTDOOR_ENVIRONMENTS
                                            )

    spawnpoints: list[SpawnPoint] = [SpawnPoint(*entry) for entry in data_json["spawnpoints"]]

    data = PokemonCrystalData(
        manifest=manifest,
        rom_version=data_json["rom_version"],
        rom_version_11=data_json["rom_version11"],
        ram_addresses=ram_address_data,
        sram_addresses=sram_address_data,
        rom_addresses=rom_address_data,
        event_flags=event_flag_data,
        engine_flags=engine_flag_data,
        mart_flag_offset=data_json["mart_flag_offset"],
        regions=regions,
        locations=locations,
        items=items,
        pocket_sizes=data_json["pocket_sizes"],
        max_item_stack=data_json["max_item_stack"],
        trainers=trainers,
        pokemon=pokemon,
        moves=moves,
        wild=wild,
        fish_time_slots=fish_time_slots,
        fish_rates=fish_rates,
        types=types,
        tmhm=tmhm,
        maps=maps,
        marts=marts,
        misc=misc,
        music=music,
        static=statics,
        trades=trades,
        fly_regions=fly_regions,
        starting_towns=starting_towns,
        game_settings=game_settings,
        phone_scripts=phone_scripts,
        request_pokemon=request_pokemon,
        adhoc_trainersanity=adhoc_trainersanity,
        grass_tiles=grass_tiles,
        grass_regions=grass_regions,
        bug_contest_encounters=bug_contest_encounters,
        palettes=palettes,
        unown_signs=unown_signs,
        entrance_connections=entrance_connections,
        map_constants=map_constants,
        flypoints=flypoints,
        spawnpoints=spawnpoints,
    )


_init()
