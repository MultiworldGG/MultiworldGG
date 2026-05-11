from collections.abc import Mapping
from collections import defaultdict
from typing import Any, Dict, ClassVar


from Options import PerGameCommonOptions, OptionError
from worlds.AutoWorld import World
from . import items, locations, options, regions, rules, web_world
from BaseClasses import MultiWorld
from .items import car_name_to_internal_id, ITEM_DEFS
from .components import SHARSettings
from .options import SimpsonsHitNRunOptions
from .SHARContainer import gen
from .web_world import SimpsonsHitNRunWebWorld

class SimpsonsHitNRunWorld(World):
    """A 2003 Action Adventure game similar to the GTA series starring the Simpsons"""

    game = "Simpsons Hit and Run"
    author: str = "Caesius"
    options_dataclass = options.SimpsonsHitNRunOptions
    options: options.SimpsonsHitNRunOptions
    settings: ClassVar[SHARSettings]

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    location_name_groups = locations.location_name_groups
    item_name_groups = items.item_name_groups

    car_name_to_internal_id = items.car_name_to_internal_id

    origin_region_name = "Hub"
    web = SimpsonsHitNRunWebWorld()

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    ut_can_gen_without_yaml = True

    apworld_version: str
    missionlockdict: Dict[str, str]
    card_table: list[locations.Card]
    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.apworld_version = "0.5.4"
        self.missionlockdict = {}
        self.card_table = []
        self.prog_cars = []

    def generate_early(self) -> None:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                print("Getting UT slot data.")
                passthrough = self.multiworld.re_gen_passthrough[self.game]
                for key in vars(self.options):
                    if key in passthrough:
                        option = getattr(self.options, key)
                        if hasattr(option, "value"):
                            value = passthrough[key]
                            option.value = value

                self.missionlockdict = passthrough["missionlockdic"]
                self.prog_cars = list(passthrough["progcars"])

                locations.fill_card_table_by_id(self, passthrough["card_locations"])


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str, make_prog: bool = False) -> items.SimpsonsHitNRunItem:
        return items.create_item_with_correct_classification(self, name, make_prog)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {}

        slot_data["version"] = self.apworld_version
        common_options = set(PerGameCommonOptions.type_hints.keys())
        for option_key, _ in self.options_dataclass.type_hints.items():
            if option_key in common_options:
                continue
            slot_data[option_key] = getattr(self.options, option_key).value

        slot_data["card_locations"] = [ card.id for card in self.card_table ]
        slot_data["missionlockdic"] = self.missionlockdict
        slot_data["progcars"] = self.prog_cars
        slot_data["VerifyID"] = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"
        slot_data["ingamehints"] = self.get_ingame_hints() if self.options.Extra_Hint_Policy else "No hints"
        # Generate costs for shops
        min = self.options.Min_Shop_Price
        max = self.options.Max_Shop_Price

        if min > max:
            print(f"Simpsons: Min shop price {min} is greater than max shop price {max}. Setting min and max to {max}.")
            min = max

        scale = self.options.Shop_Scale_Modifier

        slot_data["costs"] = [
            self.random.randint(
                min * (1 if level == 1 else (level * scale)),
                max * (1 if level == 1 else (level * scale))
            )
            for level in range(1, 8)
            for _ in range(6)
        ]

        return slot_data

    def generate_output(self, output_directory: str):
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}_SHAR"

        blacklisted_ids = {
            car_name_to_internal_id[name]
            for name in self.options.Traffic_Blacklist
            if name in car_name_to_internal_id
        }

        available_traffic = [
            v for v in car_name_to_internal_id.values()
            if v not in blacklisted_ids
        ]

        LEVEL_LOCKED_TRAFFIC = {
            "Mini School Bus", "Glass Truck", "Minivan", "Pizza Van", "Taxi", "Sedan B", "Fish Van",
            "Garbage Truck", "Nuclear Waste Truck", "Pickup", "Sports Car A", "Compact Car", "SUV",
            "Hallo Hearse", "Coffin Car", "Ghost Ship", "Witch Broom"
        }

        level_blacklists = defaultdict(set)

        for name, item in ITEM_DEFS.items():
            if not item.is_car:
                continue
            #if name not in LEVEL_LOCKED_TRAFFIC:
            #    continue

            for level in item.level:
                level_blacklists[level].add(item.internal_id)

        final_traffic = []
        for level in range(1, 8):
            pool = [car for car in available_traffic if car not in level_blacklists[level]]

            if len(pool) < 5:
                print(f"Not enough traffic cars for level {level}. Shuffled traffic will be treated as False.")
                continue

            final_traffic.extend(self.random.sample(pool, 5))

        traffic_table = final_traffic if len(final_traffic) == 35 else ["NO TRAFFIC"]

        gen(
            output_directory,
            filename,
            f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}",
            f"AP-{self.multiworld.seed_name}-P{self.player}",
            self.card_table,
            traffic_table,
            {mission: car_name_to_internal_id[car] for mission, car in self.missionlockdict.items()},
            self.player
        )

    def get_ingame_hints(self):
        igh = {}

        for item in self.prog_cars:
            try:
                loc = self.multiworld.find_item(item, self.player)
            except StopIteration:
                continue

            igh[items.ITEM_NAME_TO_ID[item]] = (loc.address, loc.player)

        for _, item in self.missionlockdict.items():
            if item == "NO MISSIONLOCKS":
                continue

            try:
                loc = self.multiworld.find_item(item, self.player)
            except StopIteration:
                continue

            igh[items.ITEM_NAME_TO_ID[item]] = (loc.address, loc.player)

        return igh

    def write_spoiler(self, spoiler_handle):
        if self.options.Mission_Locks:
            spoiler_handle.write("\nMission Locks:\n")
            for i, (m, c) in enumerate(sorted(self.missionlockdict.items(), key=lambda item: (int(item[0][2]), int(item[0][4]))), start=1):
                spoiler_handle.write(f"{i}: {m} requires {c}\n")
