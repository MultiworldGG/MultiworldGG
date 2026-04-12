import string

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
            options.CreditReplacement,
            options.RequiredCredits
        ]),
        OptionGroup("Checks", [
            options.ChecksPerMoon,
            options.NumQuotas,
            options.MoneyPerQuotaCheck,
            options.Scrapsanity,
            options.RandomizeCompanyBuilding,
            options.RandomizeScanner,
            options.RandomizeTerminal
        ], True),
        OptionGroup("Starting Info", [
            options.StartingMoon,
            options.StartingStaminaBars,
            options.StartingInventorySlots
        ], True),
        OptionGroup("Logic Config", [
            options.MoonCheckGrade,
            options.SplitMoonGrades,
            options.EasyMoonCheckGrade,
            options.MedMoonCheckGrade,
            options.HighMoonCheckGrade,
            options.ScrapSpawnChance,
            options.MonsterSpawnChance,
            options.MinMoneyCheck,
            options.MaxMoneyCheck,
            options.ModifyScrapSpawns,
            options.ExcludeShotguns,
            options.ExcludeHive,
            options.ExcludeEgg
        ], True),
        OptionGroup("Weights", [
            options.MoneyWeight,
            options.BirthdayGiftWeight,
            options.WeightReducers,
            options.ScrapDupeWeight,
            options.DayIncreaseWeight,
            options.DayDecreaseWeight,
            options.BrackenTrapWeight,
            options.HauntTrapWeight
        ], True)
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
    game = f"Lethal Company{name}"
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

    def create_items(self) -> None:
        # Generate item pool
        itempool: List = []

        for item in self.generated_items:
            names = item.create_item(self)
            for name in names:
                if not name == self.initial_world:
                    itempool.append(name)

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
        create_events(self.multiworld, self.player)

    def fill_slot_data(self):
        calculate_credits(self)

        slot_data = {
            "deathLink": self.options.death_link.value
        }

        for option in dir(self.options):
            if hasattr(getattr(self.options, option), "slot"):
                if getattr(self.options, option).slot:
                    slot_data[getattr(self.options, option).slot_name] = getattr(self.options, option).value

        if self.options.game_mode == 2:
            slot_data["companycreditsgoal"] = self.required_credit_count

        if self.options.modify_scrap_spawns.value == 1:
            slot_data["moon_to_scrap_map"] = self.scrap_map

        return slot_data

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = self.slot_item_data.classification_table.get(name)
        item = LethalCompanyItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    world_region = world.get_region("Company Building", player)
    victory_region = world.get_region("Victory", player)
    victory_event = LethalCompanyLocation(player, "Victory", None, victory_region)
    quota_region = world.get_region("Quotas", player)
    quota_quarter1_event = LethalCompanyLocation(player, "Quota 25%", None, quota_region)
    quota_quarter2_event = LethalCompanyLocation(player, "Quota 50%", None, quota_region)
    quota_quarter3_event = LethalCompanyLocation(player, "Quota 75%", None, quota_region)
    victory_event.place_locked_item(LethalCompanyItem("Victory", ItemClassification.progression, None, player))
    quota_quarter1_event.place_locked_item(LethalCompanyItem("Completed 25% Quota", ItemClassification.progression,
                                                             None, player))
    quota_quarter2_event.place_locked_item(LethalCompanyItem("Completed 50% Quota", ItemClassification.progression,
                                                             None, player))
    quota_quarter3_event.place_locked_item(LethalCompanyItem("Completed 75% Quota", ItemClassification.progression,
                                                             None, player))
    quota_region.locations.append(quota_quarter1_event)
    quota_region.locations.append(quota_quarter2_event)
    quota_region.locations.append(quota_quarter3_event)
    world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, loc=None) -> Region:
    if loc is None:
        loc = {}
    ret = Region(name, player, world)
    for location_name, location_id in loc.items():
        ret.locations.append(LethalCompanyLocation(player, location_name, location_id, ret))
    return ret
