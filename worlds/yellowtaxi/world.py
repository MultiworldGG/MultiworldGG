import logging
import math
import typing
from collections.abc import Mapping
from typing import Any, ClassVar, Dict, List, Set, Optional

from BaseClasses import MultiWorld, Region, Entrance
from Options import Option, OptionError
from Utils import messagebox#, visualize_regions, Version
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, Type, components

from . import data_loader, level_shuffler, items, regions, locations, rules, web_world
from . import options as taxi_options
from . import settings as taxi_settings
from .items import TRAPS


class YellowTaxiWorld(World):
    #TODO: Better description
    """
    Yellow Taxi Goes Vroom is a trippy arcade platformer ready to take you on a crazy adventure!
    """
    game = "Yellow Taxi Goes Vroom"

    web = web_world.YellowTaxiWebWorld()

    options_dataclass = taxi_options.YellowTaxiOptions
    options: taxi_options.YellowTaxiOptions
    settings_key = "yellowtaxi_options"
    settings: ClassVar[taxi_settings.YellowTaxiSettings]

    location_name_to_id = data_loader.all_locations
    location_name_groups = data_loader.all_location_groups
    item_name_to_id = items.ITEM_NAME_TO_ID
    item_name_groups = {
        "Move": { "Progressive Jump", "Progressive Boost" },
        "Move (Hub)": { "Progressive Jump (Hub)", "Progressive Boost (Hub)" },
        "Move (Morio's Lab)": { "Progressive Jump (Hub)", "Progressive Boost (Hub)" },
        "Move (Granny's Island)": { "Progressive Jump (Hub)", "Progressive Boost (Hub)" },
        "Move (Morio's Home)": { "Progressive Jump (Morio's Home)", "Progressive Boost (Morio's Home)" },
        "Move (Bombeach)": { "Progressive Jump (Bombeach)", "Progressive Boost (Bombeach)" },
        "Move (Arcade Panik)": { "Progressive Jump (Arcade Panik)", "Progressive Boost (Arcade Panik)" },
        "Move (Pizza Time)": { "Progressive Jump (Pizza Time)", "Progressive Boost (Pizza Time)" },
        "Move (Tosla's Offices)": { "Progressive Jump (Tosla's Offices)", "Progressive Boost (Tosla's Offices)" },
        "Move (Maurizio's City)": { "Progressive Jump (Maurizio's City)", "Progressive Boost (Maurizio's City)" },
        "Move (Crash Test Industries)": { "Jump (Crash Test Industries)", "Boost (Crash Test Industries)" },
        #"Move (Morio's Mind)": { "Progressive Jump (Morio's Mind)", "Progressive Boost (Morio's Mind)" },
        #"Move (Ruined Observatory)": { "Progressive Jump (Ruined Observatory)", "Progressive Boost (Ruined Observatory)" },
        #"Move (Tosla HQ)": { "Progressive Jump (Tosla HQ)", "Progressive Boost (Tosla HQ)" },
        #"Move (Moon)": { "Progressive Jump (The Moon)", "Progressive Boost (The Moon)" },
        #"Move (The Moon)": { "Progressive Jump (The Moon)", "Progressive Boost (The Moon)" },
        "Move (Gym Gears)": { "Progressive Jump (Gym Gears)", "Progressive Boost (Gym Gears)" },
        "Move (Fecal Matters)": { "Progressive Jump (Fecal Matters)", "Progressive Boost (Fecal Matters)" },
        "Move (Flushed Away)": { "Progressive Jump (Flushed Away)", "Progressive Boost (Flushed Away)" },
        "Move (Mosk's Rocket)": { "Progressive Jump (Mosk's Rocket)", "Progressive Boost (Mosk's Rocket)" },
        "Move (Rocket)": { "Progressive Jump (Mosk's Rocket)", "Progressive Boost (Mosk's Rocket)" },
        "Move (Time Trials)": { "Progressive Jump (Time Trials)", "Progressive Boost (Time Trials)" },
        "Move (Baby Steps!)": { "Progressive Jump (Time Trials)", "Progressive Boost (Time Trials)" },
        "Move (Getting Gud!)": { "Progressive Jump (Time Trials)", "Progressive Boost (Time Trials)" },
        "Move (Pro Tricks!)": { "Progressive Jump (Time Trials)", "Progressive Boost (Time Trials)" },
        "Golden Spring": { "Golden Spring Blueprints" },
        "Golden Propeller": { "Golden Propeller Blueprints" },
        "FGU": { "Full Game Unlock" },
        "Trap": TRAPS,
        "Traps": TRAPS,
    }

    # Universal Tracker stuff
    glitches_item_name = "Additional Expert Logic Level"
    ut_can_gen_without_yaml = True
    found_entrances_datastorage_key: list[str] = ["Slot:{player}:PortalSave"]

    # Shamelessly taken from Tunic's implementation
    def attempt_launch_ut(*args: str) -> None:
        try:
            from worlds.tracker import launch_client

            launch_client(*args)
        except ImportError as e:
            logging.getLogger(__name__).error(e)
            messagebox(
                "Cannot Load UT",
                "There was an error loading Universal Tracker. Please ensure it is installed and up to date.",
            )

    components.append(
        Component(
            "Universal Tracker for Yellow Taxi Goes Vroom",
            func=attempt_launch_ut,
            game_name="Yellow Taxi Goes Vroom",
            component_type=Type.HIDDEN,
            supports_uri=True,
        )
    )

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data

    # Keeping default Menu region, actual starting location can vary so this is simpler
    origin_region_name = "Menu"

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.num_gears : int = 0
        self.num_bunnies : int = 0
        self.num_portals : int = 0
        self.num_filler : int = 0
        self.included_hats: Set[str] = set()
        self.hat_location_count : int = 0
        self.level_order : List[str] = []
        self.excluded_regions : List[str] = []
        self.included_levels : List[str] = []
        self.special_levels : List[str] = []
        self.lab_start : bool = False
        self.early_gela_toni : bool = False
        self.early_pizza_wheels : bool = False
        self.early_pizza_king : bool = False
        self.early_rat : bool = False
        self.early_doggo : bool = False
        self.early_sewer_island : bool = False
        self.early_backflip : bool = False
        self.early_psycho_taxi : bool = False
        self.early_orange_switch : bool = False
        self.early_golden_spring : bool = False
        self.early_golden_propeller : bool = False
        self.early_morios_password : bool = False
        self.early_rocket : bool = False
        self.exclude_spike_bunny : bool = False
        self.exclude_top_bunny : bool = False
        self.final_portal_cost : int = 0
        self.goal_levels : List[str] = ["Bombeach"]
        # These are used to simplify logic and region inclusion rules
        # Sometimes not shuffling these results in them not existing, if the related level isn't in the game
        self.has_golden_spring_access : bool = False
        self.has_golden_propeller_access : bool = False
        self.has_orange_switch_access : bool = False
        self.has_password_access : bool = False
        self.has_rocket_access : bool = False
        # Pizza Wheels or Golden Spring can give spike traversal
        self.has_spike_traversal : bool = False

        self.using_ut : bool = False
        # UT only
        if getattr(self.multiworld, "generation_is_fake", False):
            self.using_ut = True
            self.defer_entrances : bool = getattr(self.multiworld, "enforce_deferred_connections", "default") != "off"
            self.disconnected_entrances : dict[int, tuple[Entrance, Region]] = {}
            self.ut_true_num_gears : int = 0
            self.ut_true_goal_cost : int = 0
            self.ut_sort_region_dict : dict[str, int] = {}

    def generate_early(self) -> None:
        # UT YAML-less
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            major_version : int = 0
            minor_version : int = 0
            build_version : int = 0
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_data.items():
                if key == "level_order":
                    for level in value:
                        for levelName, levelId in data_loader.level_ids.items():
                            if level == levelId:
                                self.level_order += [levelName]
                                break
                    continue

                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
                elif key == "total_gears":
                    self.ut_true_num_gears = value
                elif key == "goal_portal_cost":
                    self.ut_true_goal_cost = value
                elif key.startswith("early_") or key.startswith("exclude_"):
                    attr : Optional[Any] = getattr(self, key, None)
                    if attr is not None:
                        setattr(self, key, value)
                elif key == "major_version":
                    major_version = value
                elif key == "minor_version":
                    minor_version = value
                elif key == "build_version":
                    build_version = value

            if major_version != self.world_version.major or minor_version != self.world_version.minor:
                raise OptionError("APWorld version (v" +
                                  f"{self.world_version.major}.{self.world_version.minor}.{self.world_version.build}" +
                                  ") is not the same version used at generation (v" +
                                  f"{major_version}.{minor_version}.{build_version})!")

        self.num_gears = 0
        self.num_bunnies = 0
        self.included_hats = set()
        self.hat_location_count = 0
        self.excluded_regions = []
        self.included_levels = []

        match self.options.goal:
            case 0:
                self.goal_levels = ["Bombeach"]
            case 1:
                self.goal_levels =  ["Tosla's Offices"]
            case 2:
                self.goal_levels = ["Maurizio's City"]
            case 3:
                self.goal_levels = ["Tosla HQ", "Moon"]

        goal_portal_index : int = -1

        if not self.using_ut:
            self.level_order = level_shuffler.get_level_order(self.options, self.random, self.goal_levels[0])
            #self.log_level_order()

        self.included_levels = ["Hub"]
        self.special_levels = [""]

        for level in self.level_order:
            if level == "Excluded":
                continue
            if level in self.goal_levels and self.options.remove_goal_portal_locations:
                continue
            self.included_levels += [level]

        if self.options.hatsanity == 1: # Special "level" for shared hats
            self.special_levels += ["Hatsanity"]

        self.has_golden_spring_access = ((self.options.shuffle_golden_spring ==
                                         self.options.shuffle_golden_spring.option_true) or
                                         "Tosla's Offices" in self.included_levels)
        self.has_spike_traversal = (self.has_golden_spring_access or
                                    self.options.pizza_wheels == self.options.pizza_wheels.option_progression)
        self.has_orange_switch_access = ((self.options.shuffle_orange_switch.value ==
                                          self.options.shuffle_orange_switch.option_true) or
                                         "Crash Test Industries" in self.included_levels)
        self.has_password_access = ((self.options.shuffle_morios_password.value ==
                                     self.options.shuffle_morios_password.option_true) or
                                    "Morio's Mind" in self.included_levels or
                                    (self.options.include_out_of_bounds.value ==
                                     self.options.include_out_of_bounds.option_full
                                     and self.options.expert_level >= 1)
                                    )
        self.has_golden_propeller_access = ((self.options.shuffle_golden_propeller.value ==
                                             self.options.shuffle_golden_propeller.option_true) or
                                            "Ruined Observatory" in self.included_levels)
        self.has_rocket_access = (self.options.rocket_unlock_condition.value !=
                                  self.options.rocket_unlock_condition.option_exclude)

        # Exclude unreachable hub areas
        if not self.has_rocket_access and not (self.options.expert_level >= 3):
            self.excluded_regions += [
                "Granny's Island - Coins on Top of Rocket",
                "Granny's Island - Gear on Top of Rocket",
            ]

        # Gela-Toni normally only appears after Bomboss is defeated
        if "Bombeach" not in self.included_levels:
            if self.options.shuffle_gela_toni:
                if not self.using_ut:
                    self.early_gela_toni = True
            else:
                self.excluded_regions += ["Ice Cream Truck - Lower Path", "Ice Cream Truck - Upper Path"]
        # Pizza King appears in Pizza Time. If level is inaccessible, either exclude his hub portion or set early
        if "Pizza Time" not in self.included_levels:
            if self.options.shuffle_pizza_king:
                if not self.using_ut:
                    self.early_pizza_king = True
            else:
                self.excluded_regions += ["Pizza Oven - Entrance", "Pizza Oven - Pillar"]
            if (self.options.pizza_wheels != self.options.pizza_wheels.option_off and
                    not self.using_ut):
                self.early_pizza_wheels = True
        if not self.has_orange_switch_access:
            if self.options.expert_level < 3:
                # Technically this is totally accessible, but is certain death
                self.excluded_regions += ["Pizza Time - Orange Block Bridge"]
            if self.options.expert_level < 1 or (not self.has_golden_propeller_access and
                                                 self.options.expert_level < 3):
                self.excluded_regions += ["Granny's Island - Crash Again Island",
                                          "Granny's Island - Crash Again Roof",
                                          "Crash Again - Starting Area",
                                          "Crash Again - End"]
                if (self.options.flushed_away_unlock_condition.value <
                        self.options.flushed_away_unlock_condition.option_exclude):
                    if not self.using_ut:
                        self.early_sewer_island = True
                else:
                    self.excluded_regions += ["Granny's Island - Sewer Island",
                                              "Granny's Island - Sewer Island Upper"]
        elif (not self.options.shuffle_orange_switch and self.level_order[13] == "Crash Test Industries"
              and (self.options.expert_level <= 0 or not self.has_golden_propeller_access) and not self.using_ut):
            # Sewer island would lock itself unless this is done
            self.early_sewer_island = True
        if not self.has_spike_traversal:
            self.excluded_regions += ["Lab Memories - First Step",
                                      "Lab Memories - High Ground"]
            if self.options.expert_level < 2:
                self.excluded_regions += ["Morio's Lab - Fourth Floor Spiky Cliffs"]
            if self.options.expert_level < 3:
                self.excluded_regions += ["Morio's Lab - Fourth Floor Spiky Bunny Alcove"]
        if not self.has_password_access:
            if self.options.expert_level <= 0 or (self.options.include_out_of_bounds !=
                                                  self.options.include_out_of_bounds.option_full
                                                  and self.options.expert_level < 3):
                self.excluded_regions += ["Morio's Lab - Fifth Floor Ruined Observatory Area",
                                          "Morio's Lab - Fifth Floor Golden Propeller",
                                          "Morio's Lab - Ledge Above Ruined Observatory Portal",
                                          "Morio's Lab - Ledge Below Tosla HQ Portal",
                                          "Morio's Lab - Fifth Floor Low Pillars",
                                          "Morio's Lab - Fifth Floor High Pillars",
                                          "Morio's Lab - Final Floor",
                                          "Morio's Lab - Final Floor Pipes",
                                          "Morio's Lab - Final Floor Bunny Shortcut Upper",
                                          "Morio's Lab - Final Floor Bunny Shortcut Lower",
                                          "Morio's Lab - Final Floor Catwalk"]
                if self.options.expert_level <= 0:
                    # Assume that expert 0 will not be using the shortcut pipe (plus it's useless until entrance rando)
                    # Additionally, expert 0 will never have GP inside lab
                    self.excluded_regions += [
                        "Morio's Lab - Second Floor Falling From Shortcut Pipe",
                        "Morio's Lab - Second Floor Access to Shortcut Pipe",
                        "Morio's Lab - Fifth Floor Inside Shortcut Pipe",
                        "Morio's Lab - Middle Floors 3 Golden Propellers",
                        "Morio's Lab - Middle Floors 2 Golden Propellers",
                        "Morio's Lab - Ground Floor Golden Propeller",
                    ]
        if not "Tosla's Offices" in self.included_levels and "Tosla's Offices" in self.goal_levels:
            # Remove employees-only completely since the hat will not be progression in this case
            # Makes generator less mad
            self.excluded_regions += [
                "Tosla Offices (Employees Only) - Starting Area",
                "Tosla Offices (Employees Only) - Higher Ground",
            ]
        if not self.has_golden_propeller_access and self.options.expert_level < 1:
            self.excluded_regions += [
                "Conveyor Belts - Platform Above Starting Area"
            ]

        # Make sure early items are set as needed
        if not self.using_ut:
            if not "Pizza Time" in self.included_levels and (self.options.shuffle_rat or self.options.cheesesanity):
                self.early_rat = True
            if self.options.shuffle_flip_o_will != 0 and "Morio's Lab - Final Floor" in self.excluded_regions:
                self.early_backflip = True
            if (self.options.psycho_taxi_unlock_condition.value ==
                    self.options.psycho_taxi_unlock_condition.option_shuffle_cartridge
                    and not "Arcade Panik" in self.included_levels):
                self.early_psycho_taxi = True
            if self.options.shuffle_orange_switch and not "Crash Test Industries" in self.included_levels:
                self.early_orange_switch = True
            if self.options.shuffle_golden_spring and not "Tosla's Offices" in self.included_levels:
                self.early_golden_spring = True
            if self.options.shuffle_golden_propeller and not "Ruined Observatory" in self.included_levels:
                self.early_golden_propeller = True
            if self.options.shuffle_morios_password and not "Morio's Mind" in self.included_levels:
                self.early_morios_password = True
            if self.options.rocket_unlock_condition.value == self.options.rocket_unlock_condition.option_shuffle_rocket:
                self.early_rocket = True

            if "Morio's Lab - Fourth Floor Spiky Bunny Alcove" in self.excluded_regions:
                self.exclude_spike_bunny = True
            if "Morio's Lab - Final Floor Bunny Shortcut Upper" in self.excluded_regions:
                self.exclude_top_bunny = True

            if self.options.coinsanity and self.multiworld.players > 1:
                if self.settings.multiworld_coinsanity_percentage_cap < self.options.coinsanity_percent:
                    self.options.coinsanity_percent.value = self.settings.multiworld_coinsanity_percentage_cap
                    logging.warning(
                        f"{self.player_name}: Your options have been modified to avoid disrupting the multiworld.\n"
                        f"Coinsanity Percent has been lowered to {self.options.coinsanity_percent.value}. "
                        "You can increase this by setting 'multiworld_coinsanity_percentage_cap' in the seed "
                        "generator's host.yaml to a higher value and generating locally.")
                if self.settings.multiworld_coinsanity_percentage_non_filler_cap < self.options.coinsanity_non_filler_cap:
                    self.options.coinsanity_non_filler_cap.value = (
                        self.settings.multiworld_coinsanity_percentage_non_filler_cap)
                    logging.warning(
                        f"{self.player_name}: Your options have been modified to avoid disrupting the multiworld.\n"
                        "Coinsanity Non-Filler Cap Percentage has been lowered to "
                        f"{self.options.coinsanity_non_filler_cap.value}. "
                        "You can increase this by setting 'multiworld_coinsanity_percentage_non_filler_cap' in the "
                        "seed generator's host.yaml to a higher value and generating locally.")
            if self.options.coinsanity_percent.value == 0:
                self.options.coinsanity.value = False

            goal_portal_threshold : int = (50 + 5 * (len(self.included_levels) - 1))
            if (not self.options.remove_goal_portal_locations and self.multiworld.players == 1 and self.options.goal < 1
                    and self.options.goal_portal_gear_percentage > goal_portal_threshold):
                self.options.goal_portal_gear_percentage.value = goal_portal_threshold
                logging.warning(
                    f"{self.player_name}: Your options have been modified to avoid generation failures.\n"
                    f"Goal Portal Gear percentage has been capped to {goal_portal_threshold}%.")

            if self.multiworld.players == 1 and self.options.ring_link:
                self.options.ring_link.value = False
                logging.warning(
                    f"{self.player_name}: Your options have been modified.\n"
                    "RingLink has no effect on a single-player game "
                    "and has been disabled to reduce unnecessary network pings.")

            if self.multiworld.players == 1 and self.options.trap_link:
                self.options.trap_link.value = False
                logging.warning(
                    f"{self.player_name}: Your options have been modified.\n"
                    "TrapLink has no effect on a single-player game "
                    "and has been disabled to reduce unnecessary network pings.")

        if not self.options.open_grannys_island and self.options.locked_morios_lab:
            self.lab_start = True

        if self.options.early_move:
            move : str = ""
            if self.options.shuffle_flip_o_will.value == self.options.shuffle_flip_o_will.option_global:
                move = self.random.choice(["Progressive Jump", "Progressive Boost"])
            if self.options.shuffle_flip_o_will.value == self.options.shuffle_flip_o_will.option_per_level:
                move = self.random.choice(["Progressive Jump (Hub)", "Progressive Boost (Hub)"])

            if move != "":
                self.multiworld.local_early_items[self.player][move] = 1

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_locations(self)
        locations.fix_location_deficit(self)
        if self.using_ut:
            self.final_portal_cost = self.ut_true_goal_cost
        else:
            self.final_portal_cost = math.floor((self.num_gears *
                                                 self.options.goal_portal_gear_percentage) / 100)

    def set_rules(self) -> None:
        rules.set_all_rules(self)
        #visualize_regions(self.get_region("Menu"), "regions_test.puml", show_entrance_names=True, linetype_ortho=False)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.YellowTaxiItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def reconnect_found_entrances(self, key: str, value: Any) -> None:
        if not value:
            return
        else:
            for i in range(0, len(data_loader.original_level_order)):
                if (value >> i) & 1 == 1 and i in self.disconnected_entrances.keys():
                    self.disconnected_entrances[i][0].connect(self.disconnected_entrances[i][1])

    def log_level_order(self) -> None:
        logger = logging.getLogger()
        logger.info(f"\nLevel Order ({self.player_name}):")
        for i in range(0, len(self.level_order)):
            logger.info(f"  {data_loader.original_level_order[i]} -> {self.level_order[i]}")

    def fill_slot_data(self) -> Mapping[str, Any]:
        # Get relevant options needed for client
        slot_data : Dict[str, Any] = self.options.as_dict(
            "death_link",
            "death_link_amnesty",
            "ring_link",
            "trap_link",
            "goal",
            "open_grannys_island",
            "locked_morios_lab",
            "locked_morios_wardrobe",
            "locked_time_trials",
            "shuffle_gela_toni",
            "shuffle_pizza_king",
            "shuffle_orange_switch",
            "shuffle_morios_password",
            "shuffle_full_game",
            "demo_portal_mode",
            "shuffle_rat",
            "gym_gears_unlock_condition",
            "fecal_matters_unlock_condition",
            "flushed_away_unlock_condition",
            "rocket_unlock_condition",
            "psycho_taxi_unlock_condition",
            "bunnysanity",
            "hatsanity",
            "cheesesanity",
            "shuffle_flip_o_will",
            "allow_top_down_jumps",
            "shuffle_spin_attack",
            "shuffle_glide",
            "shuffle_golden_spring",
            "shuffle_golden_propeller",
            "pizza_wheels",
            "extra_demo_collectables",
            "purchase_rebate_percent",
            "remove_goal_portal_locations",
            "funny_faces",
            "easy_alien_mosk",
            "quick_pickups",
            "shop_hints",
            "taxi_skin",
            # Only used by UT
            "expert_level",
            "include_out_of_bounds",
            toggles_as_bools=True
        )

        slot_data["major_version"] = self.world_version.major
        slot_data["minor_version"] = self.world_version.minor
        slot_data["build_version"] = self.world_version.build

        # Set counts that client needs to know
        slot_data["goal_portal_cost"] = self.final_portal_cost
        slot_data["total_gears"] = self.num_gears
        slot_data["total_bunnies"] = self.num_bunnies

        # Set early item states, in order to make it easier to track clientside without needing to match logic
        slot_data["early_gela_toni"] = self.early_gela_toni
        slot_data["early_pizza_king"] = self.early_pizza_king
        slot_data["early_pizza_wheels"] = self.early_pizza_wheels
        slot_data["early_rat"] = self.early_rat
        #dict["early_doggo"] = self.early_doggo
        slot_data["early_backflip"] = self.early_backflip
        slot_data["early_psycho_taxi"] = self.early_psycho_taxi
        slot_data["early_orange_switch"] = self.early_orange_switch
        slot_data["early_golden_spring"] = self.early_golden_spring
        slot_data["early_golden_propeller"] = self.early_golden_propeller
        slot_data["early_morios_password"] = self.early_morios_password
        slot_data["early_rocket"] = self.early_rocket
        slot_data["early_sewer_island"] = self.early_sewer_island

        # Set excluded bunnies
        slot_data["exclude_top_bunny"] = self.exclude_top_bunny
        slot_data["exclude_spike_bunny"] = self.exclude_spike_bunny

        # Start location
        slot_data["lab_start"] = self.lab_start

        if self.options.trap_link_uses_whitelist:
            slot_data["trap_link_whitelist"] = sorted(self.options.enabled_traps.value)

        numerical_level_order : List[int] = []

        for level in self.level_order:
            numerical_level_order.append(data_loader.level_ids[level])

        slot_data["level_order"] = numerical_level_order

        return slot_data

    def custom_ut_sort(self, region_label: str, location_label: str) -> str | int:
        return self.ut_sort_region_dict.get(region_label, 9999999)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        er_hint_data = {}
        for reg_name in data_loader.regions_json_data.keys():
            try:
                region : Region = self.multiworld.get_region(reg_name, self.player)
            except KeyError:
                continue

            region_data : Dict[str, Any] = data_loader.regions_json_data[reg_name]

            if region_data["level"] not in self.level_order:
                continue

            level_index : int = self.level_order.index(region_data["level"])
            if level_index == data_loader.original_level_order.index(region_data["level"]):
                continue

            level_entrance : str = data_loader.original_level_order[level_index]

            if level_entrance in data_loader.original_portal_level_order:
                level_entrance += " Portal"
            elif level_entrance == "Psycho Taxi":
                level_entrance += " Arcade Machine"
            elif level_entrance.endswith("!"):
                level_entrance += " TV"
            else:
                level_entrance += " Entrance"

            for location in region.get_locations():
                if location.address is None:
                    continue
                er_hint_data[location.address] = level_entrance

        hint_data[self.player] = er_hint_data

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        spoiler_handle.write("\nEntrances:\n")
        for i in range(0, len(self.level_order)):
            if self.level_order[i] != "Excluded":
                spoiler_handle.write(f"\n{data_loader.original_level_order[i]} -> {self.level_order[i]}")
