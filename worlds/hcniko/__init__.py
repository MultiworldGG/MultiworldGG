from typing import List, Dict, TextIO, Any

from BaseClasses import MultiWorld
from BaseClasses import Region, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import item_data_table, HereComesNikoItem, item_table, item_name_groups
from .Locations import location_data_table, HereComesNikoLocation, locked_locations, location_table, \
    location_name_groups
from .Options import *
from .Regions import region_data_table
from .Rules import *


class HereComesNikoWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to setting up & playing Here Comes Niko! in MultiworldGG.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["nieli"]
    )

    tutorials = [setup_en]
    option_groups = hcniko_option_groups


class HereComesNikoWorld(World):
    """A cozy little game, about frogs and being a good friend"""

    game = "Here Comes Niko!"
    web = HereComesNikoWebWorld()
    options: HereComesNikoOptions
    options_dataclass = HereComesNikoOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    using_ut: bool
    passthrough: Dict[str, Any]
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.selected_ticket = None
        self.kiosk_cost: Dict[str, int] = {
            "Kiosk Home": 0,
            "Kiosk Hairball City": 0,
            "Kiosk Turbine Town": 0,
            "Kiosk Salmon Creek Forest": 0,
            "Kiosk Public Pool": 0,
            "Kiosk Bathhouse": 0,
            "Elevator": 0
        }

        self.cassette_cost: Dict[str, int] = {
            "Hairball City - Mitch": 0,
            "Hairball City - Mai": 0,
            "Turbine Town - Mitch": 0,
            "Turbine Town - Mai": 0,
            "Salmon Creek Forest - Mai": 0,
            "Salmon Creek Forest - Mitch": 0,
            "Public Pool - Mitch": 0,
            "Public Pool - Mai": 0,
            "Bathhouse - Mitch": 0,
            "Bathhouse - Mai": 0,
            "Tadpole HQ - Mai": 0,
            "Tadpole HQ - Mitch": 0,
            "Gary's Garden - Mai": 0,
            "Gary's Garden - Mitch": 0,
        }
        self.extra_cassettes = 0
        self.custom_goal_required = 0

    def generate_early(self):
        adjust_options(self)
        # if self.options.shuffle_kiosk_reward == 0:
        #     self.options.tickets_on_kiosk.value = 0
        # Random starting Ticket
        tickets = [
            "Hairball City Ticket",
            "Turbine Town Ticket",
            "Salmon Creek Forest Ticket",
            "Public Pool Ticket",
            "Bathhouse Ticket",
            "Tadpole HQ Ticket"
        ]
        if self.options.start_with_ticket.value:
            self.selected_ticket = self.random.choice(tickets)
            self.multiworld.push_precollected(self.create_item(self.selected_ticket))
        else:
            # Place one of the tickets early so there are no fill errors
            early_ticket = self.random.choice(tickets)
            self.multiworld.early_items[self.player][early_ticket] = 1

        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Here Comes Niko!" in self.multiworld.re_gen_passthrough:
                self.using_ut = True
                self.passthrough = self.multiworld.re_gen_passthrough["Here Comes Niko!"]
                self.options.start_with_ticket.value = self.passthrough["start_with_ticket"]
                self.options.shuffle_garys_garden.value = self.passthrough["shuffle_garden"]
                self.options.level_based_keys.value = self.passthrough["key_level"]
                self.options.bonk_permit.value = self.passthrough["bonk_permit"]
                self.options.bug_catching.value = self.passthrough["bug_net"]
                self.options.soda_cans.value = self.passthrough["soda_cans"]
                self.options.parasols.value = self.passthrough["parasols"]
                self.options.swimming.value = self.passthrough["swimming"]
                self.options.textbox.value = self.passthrough["textbox"]
                self.options.ac_repair.value = self.passthrough["ac_repair"]
                self.options.applebasket.value = self.passthrough["applebasket"]
                self.options.precisejumps.value = self.passthrough["precisejumps"]
                self.options.fishsanity.value = self.passthrough["fishsanity"]
                self.options.seedsanity.value = self.passthrough["seedsanity"]
                self.options.flowersanity.value = self.passthrough["flowersanity"]
                self.options.bonesanity.value = self.passthrough["bonesanity"]
                self.options.applesanity.value = self.passthrough["applessanity"]
                self.options.bugsanity.value = self.passthrough["bugsanity"]
                self.options.chatsanity.value = self.passthrough["chatsanity"]
                self.options.thoughtsanity.value = self.passthrough["thoughtsanity"]
                self.options.access_garys_garden.value = self.passthrough["garden_access"]
                self.options.snail_shop.value = self.passthrough["snailshop"]
                self.options.shuffle_kiosk_reward.value = self.passthrough["shuffle_kiosk_reward"]
                self.options.cassette_logic.value = self.passthrough["cassette_logic"]
                self.options.enable_achievements.value = self.passthrough["achievements"]
                self.options.shuffle_handsome_frog.value = self.passthrough["handsome_frog"]
                self.options.goal_completion.value = self.passthrough["goal_completion"]
            else:
                self.using_ut = False
        else:
            self.using_ut = False

    def create_item(self, name: str) -> HereComesNikoItem:
        return HereComesNikoItem(name, item_data_table[name].type, item_data_table[name].id, self.player)

    def create_items(self) -> None:
        mw = self.multiworld

        item_pool: List[HereComesNikoItem] = []

        for name, item in item_data_table.items():
            if not item.id or not item.can_create(self.options):
                continue
            if item.type in {ItemClassification.filler, ItemClassification.trap}:
                continue
            if name == "Speed Boost":
                continue
            for _ in range(item.num_exist):
                item_pool.append(self.create_item(name))

        if not self.options.shuffle_garys_garden.value:
            for _ in range(3):
                item_pool.remove(self.create_item("Coin"))
            if self.options.cassette_logic.value != 0:
                for _ in range(10):
                    item_pool.remove(self.create_item("Cassette"))

        if self.options.goal_completion.value == 1:
            coins_needed = 76
        elif self.options.goal_completion.value == 2:
            coins_needed = self.custom_goal_required
        else:
            coins_needed = self.kiosk_cost["Elevator"]
        coin_count = 0
        for item in item_pool:
            if item.name == "Coin":
                coin_count += 1
                if coin_count <= coins_needed:
                    item.classification = ItemClassification.progression_deprioritized
        if self.options.start_with_ticket.value:
            item_pool = [item for item in item_pool if item.name != self.selected_ticket]

        # Add extra cassettes to the item pool
        if self.options.extra_cassettes.value > 0 and self.options.cassette_logic.value != 0:
            total_locations = len(self.multiworld.get_unfilled_locations(self.player))
            remaining_spots = total_locations - len(item_pool)
            extra_cassettes_amount = self.options.extra_cassettes.value
            extra_cassettes_to_add = min(extra_cassettes_amount, remaining_spots)
            for _ in range(extra_cassettes_to_add):
                item_pool.append(self.create_item("Cassette"))
            self.extra_cassettes = extra_cassettes_to_add

        # Determine available locations before adding Speed Boosts
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        remaining_spots = total_locations - len(item_pool)
        speed_boost_amount = self.options.speed_boost_amount.value
        speed_boosts_to_add = min(speed_boost_amount, remaining_spots)
        for _ in range(speed_boosts_to_add):
            item_pool.append(self.create_item("Speed Boost"))
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        item_pool += self.create_junk_items(total_locations - len(item_pool))
        #item_pool += [self.create_filler() for _ in range(total_locations - len(item_pool))]
        mw.itempool += item_pool

    def create_regions(self) -> None:
        player = self.player
        mw = self.multiworld

        # Create regions
        for region_name in region_data_table.keys():
            region = Region(region_name, player, mw)
            mw.regions.append(region)

        # Create locations
        for region_name, region_data in region_data_table.items():
            region = mw.get_region(region_name, player)
            region.add_locations({
                location_name: location_data.id for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.options)
            },  HereComesNikoLocation)
            region.add_exits(region_data.connecting_regions)

        # Place locked locations
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.options):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            mw.get_location(location_name, player).place_locked_item(locked_item)

        if not self.options.shuffle_kiosk_reward.value:
            kiosk_locations = {
                "Home - Kiosk": "Hairball City Ticket",
                "Hairball City - Kiosk": "Turbine Town Ticket",
                "Turbine Town - Kiosk": "Salmon Creek Forest Ticket",
                "Salmon Creek Forest - Kiosk": "Public Pool Ticket",
                "Public Pool - Kiosk": "Bathhouse Ticket",
                "Bathhouse - Kiosk": "Tadpole HQ Ticket"
            }
            selected_ticket = getattr(self, 'selected_ticket', None)
            for location, ticket in kiosk_locations.items():
                # Skip placing this ticket if it matches the selected_ticket
                if selected_ticket and ticket == selected_ticket:
                    continue  # Skip this iteration to prevent placing the selected ticket
                mw.get_location(location, player).place_locked_item(self.create_item(ticket))

    def get_filler_item_name(self) -> str:
        filler_items = [item for item, data in item_data_table.items() if data.type == ItemClassification.filler]
        return self.random.choice(filler_items)

    def create_junk_items(self, count: int) -> List[HereComesNikoItem]:
        trap_chance = self.options.trapchance.value
        junk_items: List[HereComesNikoItem] = []
        filler_items: List[str] = [name for name, item in item_data_table.items() if item.type == ItemClassification.filler]
        trap_list: Dict[str, int] = {}

        for name, item in item_data_table.items():
            if trap_chance > 0 and item.type == ItemClassification.trap:
                option_map = {
                    "Freeze Trap": self.options.freeze_trapweight.value,
                    "Iron Boots Trap": self.options.ironboots_trapweight.value,
                    "Whoops! Trap": self.options.whoops_trapweight.value,
                    "My Turn! Trap": self.options.myturn_trapweight.value,
                    "Gravity Trap": self.options.gravity_trapweight.value,
                    "Home Trap": self.options.home_trapweight.value,
                    "W I D E Trap": self.options.wide_trapweight.value,
                    "Phone Trap": self.options.phone_trapweight.value,
                    "Tiny Trap": self.options.tiny_trapweight.value,
                    "Jumping Jacks Trap": self.options.jumpingjacks_trapweight.value,
                    "Camera Stuck Trap": self.options.camerastuck_trapweight.value,
                    "Inverted Camera Trap": self.options.invertedcamera_trapweight.value,
                    "There Goes Niko Trap": self.options.theregoesniko_trapweight.value,
                }
                if name in option_map:
                    trap_list[name] = option_map[name]

        for i in range(count):
            if trap_chance > 0 and self.random.randint(1, 100) <= trap_chance:
                junk_items.append(self.create_item(
                    self.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
            else:
                junk_items.append(self.create_item(
                    self.random.choice(filler_items)))
        return junk_items

    def set_rules(self) -> None:
        player = self.player
        mw = self.multiworld

        # Complete condition
        mw.completion_condition[player] = lambda state: state.has("Victory", player)

        region_rules = get_region_rules(player, self)
        for entrance_name, rule in region_rules.items():
            entrance = mw.get_entrance(entrance_name, player)
            entrance.access_rule = rule

        location_rules = get_location_rules(player, self)
        for location in mw.get_locations(player):
            name = location.name
            if name in location_rules and location_data_table[name].can_create(self.options):
                location.access_rule = location_rules[name]

        # assign randomized costs
        if self.using_ut:
            self.kiosk_cost["Kiosk Home"] = self.passthrough["kioskhome"]
            self.kiosk_cost["Kiosk Hairball City"] = self.passthrough["kioskhc"]
            self.kiosk_cost["Kiosk Turbine Town"] = self.passthrough["kiosktt"]
            self.kiosk_cost["Kiosk Salmon Creek Forest"] = self.passthrough["kiosksfc"]
            self.kiosk_cost["Kiosk Public Pool"] = self.passthrough["kioskpp"]
            self.kiosk_cost["Kiosk Bathhouse"] = self.passthrough["kioskbath"]
            self.kiosk_cost["Elevator"] = self.passthrough["kioskhq"]
            if self.options.goal_completion.value == 2:
                self.custom_goal_required = self.passthrough["custom_goal"]
            if self.options.cassette_logic.value == 0:
                self.cassette_cost["Hairball City - Mitch"] = self.passthrough["chc1"]
                self.cassette_cost["Hairball City - Mai"] = self.passthrough["chc2"]
                self.cassette_cost["Turbine Town - Mitch"] = self.passthrough["ctt1"]
                self.cassette_cost["Turbine Town - Mai"] = self.passthrough["ctt2"]
                self.cassette_cost["Salmon Creek Forest - Mitch"] = self.passthrough["csfc1"]
                self.cassette_cost["Salmon Creek Forest - Mai"] = self.passthrough["csfc2"]
                self.cassette_cost["Public Pool - Mitch"] = self.passthrough["cpp1"]
                self.cassette_cost["Public Pool - Mai"] = self.passthrough["cpp2"]
                self.cassette_cost["Bathhouse - Mitch"] = self.passthrough["cbath1"]
                self.cassette_cost["Bathhouse - Mai"] = self.passthrough["cbath2"]
                self.cassette_cost["Tadpole HQ - Mitch"] = self.passthrough["chq1"]
                self.cassette_cost["Tadpole HQ - Mai"] = self.passthrough["chq2"]
                self.cassette_cost["Gary's Garden - Mitch"] = self.passthrough["cgg1"]
                self.cassette_cost["Gary's Garden - Mai"] = self.passthrough["cgg2"]
            else:
                self.cassette_cost["Hairball City - Mitch"] = self.passthrough["chc1"] * 5
                self.cassette_cost["Hairball City - Mai"] = self.passthrough["chc2"] * 5
                self.cassette_cost["Turbine Town - Mitch"] = self.passthrough["ctt1"] * 5
                self.cassette_cost["Turbine Town - Mai"] = self.passthrough["ctt2"] * 5
                self.cassette_cost["Salmon Creek Forest - Mitch"] = self.passthrough["csfc1"] * 5
                self.cassette_cost["Salmon Creek Forest - Mai"] = self.passthrough["csfc2"] * 5
                self.cassette_cost["Public Pool - Mitch"] = self.passthrough["cpp1"] * 5
                self.cassette_cost["Public Pool - Mai"] = self.passthrough["cpp2"] * 5
                self.cassette_cost["Bathhouse - Mitch"] = self.passthrough["cbath1"] * 5
                self.cassette_cost["Bathhouse - Mai"] = self.passthrough["cbath2"] * 5
                self.cassette_cost["Tadpole HQ - Mitch"] = self.passthrough["chq1"] * 5
                self.cassette_cost["Tadpole HQ - Mai"] = self.passthrough["chq2"] * 5
                self.cassette_cost["Gary's Garden - Mitch"] = self.passthrough["cgg1"] * 5
                self.cassette_cost["Gary's Garden - Mai"] = self.passthrough["cgg2"] * 5

    def scout_swim_course(self) -> Any:
        if not self.options.swimming.value:
            return None
        loc = self.multiworld.find_item("Swim Course", self.player)
        return [{"player": loc.player, "location": loc.address}]

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if self.options.start_with_ticket.value:
            spoiler_handle.write(f"Starting Ticket: {self.selected_ticket}\n")
        for i in self.kiosk_cost:
            spoiler_handle.write("%s Cost: %i\n" %(i, self.kiosk_cost[i]))
        for i in self.cassette_cost:
            if self.options.cassette_logic == 0:
                real_cassette_cost = self.cassette_cost[i]
            else:
                real_cassette_cost = self.cassette_cost[i] * 5
            spoiler_handle.write(f"%s Cassette Cost: %i\n" %(i, real_cassette_cost))
        spoiler_handle.write(f"Extra added Cassettes: {self.extra_cassettes}\n")
        if self.options.goal_completion.value == 2:
            spoiler_handle.write(f"Required Coins for custom goal: {self.custom_goal_required}\n")

    def fill_slot_data(self) -> Dict[str, Any]:
        return  {
            "kioskhome": self.kiosk_cost["Kiosk Home"],
            "kioskhc": self.kiosk_cost["Kiosk Hairball City"],
            "kiosktt": self.kiosk_cost["Kiosk Turbine Town"],
            "kiosksfc": self.kiosk_cost["Kiosk Salmon Creek Forest"],
            "kioskpp": self.kiosk_cost["Kiosk Public Pool"],
            "kioskbath": self.kiosk_cost["Kiosk Bathhouse"],
            "kioskhq": self.kiosk_cost["Elevator"],
            "chc1": self.cassette_cost["Hairball City - Mitch"],
            "chc2": self.cassette_cost["Hairball City - Mai"],
            "ctt1": self.cassette_cost["Turbine Town - Mitch"],
            "ctt2": self.cassette_cost["Turbine Town - Mai"],
            "csfc1": self.cassette_cost["Salmon Creek Forest - Mitch"],
            "csfc2": self.cassette_cost["Salmon Creek Forest - Mai"],
            "cpp1": self.cassette_cost["Public Pool - Mitch"],
            "cpp2": self.cassette_cost["Public Pool - Mai"],
            "cbath1": self.cassette_cost["Bathhouse - Mitch"],
            "cbath2": self.cassette_cost["Bathhouse - Mai"],
            "chq1": self.cassette_cost["Tadpole HQ - Mitch"],
            "chq2": self.cassette_cost["Tadpole HQ - Mai"],
            "cgg1": self.cassette_cost["Gary's Garden - Mitch"],
            "cgg2": self.cassette_cost["Gary's Garden - Mai"],
            "shuffle_garden": self.options.shuffle_garys_garden.value,
            "fishsanity": self.options.fishsanity.value,
            "seedsanity": self.options.seedsanity.value,
            "flowersanity": self.options.flowersanity.value,
            "applessanity": self.options.applesanity.value,
            "bugsanity": self.options.bugsanity.value,
            "chatsanity": self.options.chatsanity.value,
            "thoughtsanity": self.options.thoughtsanity.value,
            "garden_access": self.options.access_garys_garden.value,
            "snailshop": self.options.snail_shop.value,
            "shuffle_kiosk_reward": self.options.shuffle_kiosk_reward.value,
            "start_with_ticket": self.options.start_with_ticket.value,
            "handsome_frog": self.options.shuffle_handsome_frog.value,
            "achievements": self.options.enable_achievements.value,
            "goal_completion": self.options.goal_completion.value,
            "cassette_logic": self.options.cassette_logic.value,
            "key_level": self.options.level_based_keys.value,
            "bonk_permit": self.options.bonk_permit.value,
            "bug_net": self.options.bug_catching.value,
            "soda_cans": self.options.soda_cans.value,
            "parasols": self.options.parasols.value,
            "swimming": self.options.swimming.value,
            "textbox": self.options.textbox.value,
            "ac_repair": self.options.ac_repair.value,
            "applebasket": self.options.applebasket.value,
            "precisejumps": self.options.precisejumps.value,
            "bonesanity": self.options.bonesanity.value,
            "death_link": self.options.death_link.value,
            "death_link_amnesty": self.options.death_link_amnesty.value,
            "trap_link": self.options.trap_link.value,
            "trapchance": self.options.trapchance.value,
            "freeze_trapweight": self.options.freeze_trapweight.value,
            "ironboots_trapweight": self.options.ironboots_trapweight.value,
            "whoops_trapweight": self.options.whoops_trapweight.value,
            "myturn_trapweight": self.options.myturn_trapweight.value,
            "gravity_trapweight": self.options.gravity_trapweight.value,
            "home_trapweight": self.options.home_trapweight.value,
            "wide_trapweight": self.options.wide_trapweight.value,
            "phone_trapweight": self.options.phone_trapweight.value,
            "tiny_trapweight": self.options.tiny_trapweight.value,
            "jumpingjacks_trapweight": self.options.jumpingjacks_trapweight.value,
            "camerastuck_trapweight": self.options.camerastuck_trapweight.value,
            "invertedcamera_trapweight": self.options.invertedcamera_trapweight.value,
            "theregoesniko_trapweight": self.options.theregoesniko_trapweight.value,
            "custom_goal": self.custom_goal_required,
            "hint_swim": self.scout_swim_course(),
        }

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data