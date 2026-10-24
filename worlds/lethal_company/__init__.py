import string
import math

from .items import LethalCompanyItem, item_table, generate_items, calculate_credits, get_default_item_map
from .locations import LethalCompanyLocation, generate_locations, locations, get_default_location_map
from .rules import set_rules
from BaseClasses import Item, ItemClassification, Tutorial, MultiWorld, Region
from .options import LCOptions
from worlds.AutoWorld import World, WebWorld
from typing import List, TextIO
from .regions import create_regions
from .logic_generator import GetImportedData
from .imported import data
from Options import OptionGroup
from . import options
from .custom_content import custom_content


class LethalCompanyWeb(WebWorld):
    option_groups = [
        OptionGroup("Goal", [
            options.Goal,
            options.CollectathonScrapGoal,
            options.CollectathonRandomScrap,
            options.CreditReplacement,
            options.RequiredCredits
        ]),
        OptionGroup("Location Options", [
            options.GradeLocationsPerMoon,
            options.NumQuotas,
            options.QuotaCheckpointEvery,
            options.MoneyPerQuotaLocation,
            options.Scrapsanity
        ], True),
        OptionGroup("Item Options", [
            options.RandomizeCompanyBuilding,
            options.RandomizeScanner,
            options.RandomizeTerminal
        ], True),
        OptionGroup("Starting Options", [
            options.StartingMoon,
            options.StartingStaminaBars,
            options.StartingInventorySlots
        ], True),
        OptionGroup("Logic Options", [
            options.GradeLocationRequiredGrade,
            options.SplitMoonGrades,
            options.EasyMoonLocationGrade,
            options.MedMoonLocationGrade,
            options.HardMoonLocationGrade,
            options.ScrapSpawnChance,
            options.MonsterSpawnChance,
            options.MinMoneyPerMoneyItem,
            options.MaxMoneyPerMoneyItem,
            options.ModifyScrapSpawns,
            options.ExcludeShotguns,
            options.ExcludeHive,
            options.ExcludeEgg
        ], True),
        OptionGroup("Trap/Filler Weights", [
            options.MoneyWeight,
            options.BirthdayGiftWeight,
            options.WeightReducers,
            options.ScrapDupeWeight,
            options.DayIncreaseWeight,
            options.DayDecreaseWeight,
            options.BrackenTrapWeight,
            options.HauntTrapWeight
        ], True),
        OptionGroup("Protocols", [
            options.DeathLink,
            options.DeathLinkScrapLoss
        ])
    ]
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Lethal Company integration for MultiworldGG multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["T0r1nn"]
    )]


name = custom_content["name"]


class LethalCompanyWorld(World):
    """
    Lethal Company is an cooperative survival horror video gam released in 2023.
    Payers obtain and sell scrap from abandoned, industrialized exomoons while avoiding traps, environmental hazards, 
    monsters, which are often referred to as "anomalies", "entities", or "creatures", and the hostile fauna. 
    As employees of "The Company", players must sell enough scrap to meet a series of increasing profit quotas until they inevitably fail and the game starts over.
    """
    game = f"Lethal Company{" - " + name if name != "" else ""}"
    options_dataclass = LCOptions
    options: LCOptions
    topology_present = False

    item_name_to_id = get_default_item_map()
    location_name_to_id = get_default_location_map()

    item_name_groups = {
        "Moons": {moon for moon in data["moons"]},
        "Items": {item for item in data["store"]},
        "Vehicles": {vehicle for vehicle in data["vehicles"]}
    }

    location_name_groups = {
        "Moons": {location for location in locations if location in {moon for moon in data["moons"]}},
        "Bestiary": {location for location in locations if "Bestiary" in location},
        "Scrap": {location for location in locations if "Scrap" in location},
        "Quota": {location for location in locations if "Quota" in location},
        "Logs": {location for location in locations if "Log" in location}
    }

    data_version = 7
    required_client_version = (0, 6, 2)
    web = LethalCompanyWeb()
    initial_world: string
    scrap_map = {}
    required_collectathon_scrap: List[str] = []
    required_credit_count: int = 0
    imported_data = {}
    moons = []
    generated_items = []
    slot_item_data = None
    log_names = []
    bestiary_names = []
    scrap_names = []
    spoiler_text = ""
    location_count = 0

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.generated_items, self.slot_item_data = generate_items(data)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(self.spoiler_text)

    def generate_early(self) -> None:

        self.imported_data = GetImportedData()

        self.location_count = len(generate_locations(self))

        self.moons = self.slot_item_data.moons

        environment_pool = self.moons.copy()

        unlock = None
        starting_moon_option = self.options.starting_moon.value
        for moon in self.moons:
            if str(moon).lower().find(starting_moon_option.lower()) >= 0:
                unlock = moon
        if unlock is None:
            unlock = self.multiworld.random.choices(environment_pool, k=1)[0]

        if (self.options.starting_stamina_bars.value == 0
                and (self.options.randomize_terminal.value == 1
                     or self.options.randomize_company_building.value == 1)
                and self.options.randomize_scanner.value == 1
                and self.multiworld.players == 1):
            while (unlock == "Offense" or unlock == "Titan" or unlock == "Artifice" or unlock == "Adamance"
                   or unlock == "Embrion"):
                unlock = self.multiworld.random.choices(environment_pool, k=1)

        self.multiworld.push_precollected(self.create_item(unlock))
        self.initial_world = unlock

        for _ in range(self.options.starting_inventory_slots.value):
            self.multiworld.push_precollected(self.create_item("Inventory Slot"))
        for _ in range(self.options.starting_stamina_bars.value):
            self.multiworld.push_precollected(self.create_item("Stamina Bar"))

    def create_items(self) -> None:
        # Generate item pool
        itempool: List = []

        for item in self.generated_items:
            names = item.create_item(self)
            for name in names:
                if not name == self.initial_world:
                    itempool.append(name)
        
        if self.options.game_mode == 2:
            num_credits = math.ceil((self.location_count - len(itempool)) * (self.options.credit_replacement.value/100.0))
            self.required_credit_count = round(num_credits * (self.options.required_credits.value/100.0))
            for _ in range(num_credits):
                itempool.append("Company Credit")

        # Fill remaining items with randomly generated junk
        while len(itempool) < self.location_count:
            itempool.append(self.get_filler_item_name())

        # Convert itempool into real items
        itempool = list(map(lambda item_name: self.create_item(item_name), itempool))
        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        set_rules(self)

    def get_filler_item_name(self) -> str:
        weights = [data for data in self.slot_item_data.filler_items.values()]
        filler = self.multiworld.random.choices([filler for filler in self.slot_item_data.filler_items.keys()], weights,
                                                k=1)[0]
        return filler

    def create_regions(self) -> None:
        create_regions(self.options, self)
        create_events(self.multiworld, self.player, self.options)

    def fill_slot_data(self):

        slot_data = {
            "worldversion": self.world_version.as_simple_string(),
            "deathLink": self.options.death_link.value,
            "deathLinkScrapLossPercent": self.options.death_link_percent_scrap_lost.value
        }

        for option in dir(self.options):
            if hasattr(getattr(self.options, option), "slot"):
                if getattr(self.options, option).slot:
                    slot_data[getattr(self.options, option).slot_name] = getattr(self.options, option).value

        if self.options.game_mode == 2:
            slot_data["companycreditsgoal"] = self.required_credit_count
        elif self.options.game_mode == 1:
            slot_data["collectathonrequiredscrap"] = self.required_collectathon_scrap

        if self.options.modify_scrap_spawns.value == 1:
            slot_data["moon_to_scrap_map"] = self.scrap_map

        return slot_data

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = self.slot_item_data.classification_table.get(name)
        item = LethalCompanyItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int, options: LCOptions) -> None:
    world_region = world.get_region("Company Building", player)
    victory_region = world.get_region("Victory", player)
    quota_region = world.get_region("Quotas", player)

    victory_event = LethalCompanyLocation(player, "Victory", None, victory_region)
    victory_event.place_locked_item(LethalCompanyItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)

    checkpoint_every = options.quota_checkpoint_every.value
    num_quotas = options.num_quotas.value
    checkpoint_index = 1
    while checkpoint_index * checkpoint_every < num_quotas:
        event = LethalCompanyLocation(player, f"Quota checkpoint {checkpoint_index}", None, quota_region)
        event.place_locked_item(LethalCompanyItem(
            f"Completed quota checkpoint {checkpoint_index}",
            ItemClassification.progression,
            None,
            player
        ))
        quota_region.locations.append(event)
        checkpoint_index += 1


def create_region(world: MultiWorld, player: int, name: str, loc=None) -> Region:
    if loc is None:
        loc = {}
    ret = Region(name, player, world)
    for location_name, location_id in loc.items():
        ret.locations.append(LethalCompanyLocation(player, location_name, location_id, ret))
    return ret
