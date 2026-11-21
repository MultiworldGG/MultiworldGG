"""
Archipelago init file for Super Mario Sunshine
"""
import math
from dataclasses import fields
import os, logging
from typing import Dict, Any, ClassVar

import Options
from BaseClasses import ItemClassification, MultiWorld, Tutorial, Item, Location
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths

from .items import ALL_ITEMS_TABLE, REGULAR_PROGRESSION_ITEMS, ALL_PROGRESSION_ITEMS, TICKET_ITEMS, JUNK_ITEMS, SmsItem
from .options import *
from .world_logic_constants import *
from .regions import create_regions, ALL_REGIONS
from .regions import get_location_name_to_id
from .sms_rules import create_sms_region_and_entrance_rules
from .constants import WORLD_VERSION, WORLD_NAME
from .sms_settings import SuperMarioSunshineSettings

logger = logging.getLogger()


def run_client(*args):
    from .SMSClient import main
    launch_subprocess(main, name="SMS Client", args=args)

icon_paths["sms_ico"] = f"ap:{__name__}/assets/sms_ap_logo.png"
components.append(
    Component("Super Mario Sunshine Client", func=run_client, component_type=Type.CLIENT,
        icon="sms_ico", file_identifier=SuffixIdentifier(".apsms")))

class SmsWebWorld(WebWorld):
    theme = "ocean"
    option_groups = [
        Options.OptionGroup("SMS Basic", [
            options.LevelAccess,
            options.Difficulty,
            options.AllShinesSelectable,
            options.StartingNozzle,
            options.EnableCoinShines,
            options.NozzleBoxes,
            options.BlueCoinSanity,
            options.BlueCoinMaximum,
            options.TradeShineMaximum,
        ])
    ]

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG Super Mario Sunshine software on your computer. This guide covers"
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Joshark"]
    )

    tutorials = [setup]

class SmsWorld(World):
    """
    The second Super Mario game to feature 3D gameplay. Coupled with F.L.U.D.D. (a talking water tank that can be used
    as a jetpack), Mario must clean the graffiti off of Delfino Isle and return light to the sky.
    """
    game = "Super Mario Sunshine"
    web = SmsWebWorld()

    options_dataclass = SmsOptions
    options: SmsOptions

    item_name_to_id = ALL_ITEMS_TABLE
    location_name_to_id = get_location_name_to_id()

    settings: ClassVar[SuperMarioSunshineSettings]
    required_shines: int = 0
    blue_coins_required: int = 0
    large_shine_count: bool = False  # Used in rules to know if corona mountain should block tickets in their region
    # otherwise generation would fail significantly more in swap.

    # Randomly picked ticket based on ticket mode being true
    ticket_chosen: str

    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.ticket_chosen = ""

    def generate_early(self):
        if self.options.starting_nozzle.value == 0:
            self.multiworld.push_precollected(self.create_item("Spray Nozzle"))
        elif self.options.starting_nozzle.value == 1:
            self.multiworld.push_precollected(self.create_item("Hover Nozzle"))
        elif self.options.starting_nozzle.value == 2:
            start_inv: list[str] = [s_item.name for s_item in self.multiworld.precollected_items[self.player]]
            early_nozzles: bool = any([nozzle_item for nozzle_item in REGULAR_PROGRESSION_ITEMS.keys() if nozzle_item
                in (list(self.multiworld.early_items[self.player].keys()) + start_inv)])
            if not early_nozzles:
                chosen_nozzle: str = str(self.random.choice(list(REGULAR_PROGRESSION_ITEMS.keys())))
                self.multiworld.early_items[self.player].update({chosen_nozzle: 1})

        if hasattr(self.multiworld, "re_gen_passthrough"):
            slot_data = self.multiworld.re_gen_passthrough[self.game]
            for key, value in slot_data.items():
                if key == "seed":
                    continue

                # If the slot data is an option value directly
                if hasattr(self.options, key):
                    getattr(self.options, key).value = value

                # if the world has the attribute itself, add the value directly to the world
                elif hasattr(self, key):
                    setattr(self, key, value)

            if self.options.level_access.value == 1 and self.ticket_chosen:
                self.multiworld.push_precollected(self.create_item(self.ticket_chosen))

            return

        if self.options.level_access.value == 1:
            self.ticket_chosen: str = str(self.random.choice(list(TICKET_ITEMS.keys())))
            self.multiworld.push_precollected(self.create_item(self.ticket_chosen))

        # If blue coins are turned on in any way, set the max trade amount to be the max blue count required.
        if self.options.blue_coin_sanity.value == 1:
            trade_blue_coins_req: int = int(self.options.trade_shine_maximum.value * 10)
            max_blue_coins_needed: int = int(trade_blue_coins_req * MAXIMUM_BLUE_COIN_PERCENTAGE)
            trade_shines_req: int = int(self.options.blue_coin_maximum.value / 10)

            # Since the player can set a blue coin amount well over the max coins needed, this can cause a lot of
            # extra progression items that are not required. Since every progression item will need to be checked
            # against accessibility, we remove the extra amounts to be more reasonable (20% extra currently).
            if self.options.blue_coin_maximum.value > max_blue_coins_needed:
                percentage_used: int = int((MAXIMUM_BLUE_COIN_PERCENTAGE - 1) * 100)
                logger.warning(f"SMS: Player's Yaml {self.player_name} had more blue coins required than trade shines "
                    f"max  + {percentage_used}%. Adjusting their count down to: {max_blue_coins_needed}")
                self.options.blue_coin_maximum.value = min(max_blue_coins_needed, self.options.blue_coin_maximum.range_end)

            elif self.options.trade_shine_maximum.value > trade_shines_req:
                logger.warning(f"SMS: Player's Yaml {self.player_name} had more trade shines required than blue coins "
                    f"in the item pool. Adjusting theirs down to: {trade_shines_req}")
                self.options.trade_shine_maximum.value = trade_shines_req

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        # Adds the minimum amount required of shines for Corona Mountain access
        possible_shine_locations: int = len([reg_loc for reg_loc in self.multiworld.get_unfilled_locations(self.player)
            if hasattr(reg_loc, "corona") and not reg_loc.corona])

        start_inv: list[str] = [start_item.name for start_item in self.multiworld.precollected_items[self.player]]

        # Removes any progression item not in the starting items
        pool = [self.create_item(prog_name) for prog_name in REGULAR_PROGRESSION_ITEMS.keys() if not prog_name in start_inv]

        if self.options.level_access.value == 1:
            pool += [self.create_item(tick_name) for tick_name in TICKET_ITEMS.keys() if tick_name not in start_inv]

        if self.options.blue_coin_sanity.value == 1:
            for _ in range(0, self.options.blue_coin_maximum.value):
                pool.append((self.create_item("Blue Coin")))

        self.blue_coins_required = self.options.blue_coin_maximum.value if self.options.blue_coin_sanity.value > 0 else 0

        # Add Shine Sprites
        remaining_locs: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        if self.options.total_shines.value > remaining_locs:
            logger.warning(f"SMS: Player's Yaml {self.player_name} had total shine count higher than locations "
                           f"available to them ({self.options.total_shines.value}). "
                           f"Adjusting their total shine count down to {remaining_locs}."
                           )
            self.options.total_shines.value = remaining_locs

        # Count how many non corona locations are available for shines sprites to be used in progression
        valid_shine_locations: int = possible_shine_locations - len(pool)
        self.required_shines = int(self.options.total_shines.value * self.options.required_shines_percentage * 0.01)

        max_required_percentage: float = 90 if valid_shine_locations > 125 else 85 if valid_shine_locations > 110 else 80
        max_location_count: int = int(valid_shine_locations * max_required_percentage * 0.01)

        # Lower the amount of shines required if our required shine count is too high
        # Lower the total shine count again to maintain the required shines percentage set by the player
        if self.required_shines > max_location_count:
            new_total_shines = int(math.ceil(max_location_count * 100 / self.options.required_shines_percentage))
            logger.warning(f"SMS: Player's Yaml {self.player_name} had required shine count higher than the safe limit "
                           f"of item pool percentage ({self.required_shines} shines - Limit: {max_location_count}). "
                           f"Adjusting their required shine count down to {max_location_count} and total shine count down to {new_total_shines}..."
                           )
            self.options.total_shines.value = new_total_shines
            self.required_shines = max_location_count

        # Check if this world's item pool has a large amount of shine sprites, used for item rules later on.
        if self.required_shines > int(math.ceil(valid_shine_locations * MAX_PROGRESSION_FLAG)):
            self.large_shine_count = True

        for i in range(0, self.options.total_shines.value):
            if i < self.required_shines:
                pool.append(self.create_item("Shine Sprite"))
            else:
                pool.append(self.create_item("Bonus Shine Sprite", ItemClassification.useful))

        # Fill remaining locations with filler.
        remaining_locs: int = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)

        for i in range(0, remaining_locs):
            pool.append(self.create_item(self.random.choice(list(JUNK_ITEMS.keys()))))

        self.multiworld.itempool += pool

    def create_item(self, name: str, item_class_override: ItemClassification | None = None):
        if not name in ALL_ITEMS_TABLE:
            raise Exception(f"Invalid SMS item name: {name}")

        if item_class_override is None:
            if name in ALL_PROGRESSION_ITEMS:
                if name == "Shine Sprite" or name == "Blue Coin":
                    classification = ItemClassification.progression_deprioritized_skip_balancing
                else:
                    classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler
        else:
            classification = item_class_override

        return SmsItem(name, classification, ALL_ITEMS_TABLE[name], self.player)

    def set_rules(self):
        create_sms_region_and_entrance_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool: list[Item], usefulitempool: list[Item],
        filleritempool: list[Item], fill_locations: list[Location]) -> None:

        # Credit to @Mysteryem for this hook and the sort_fuc.
        game_players = multiworld.get_game_players(cls.game)
        # Get all player IDs that require either corona mountain shines to complete their goal or have blue coins
        sms_excessive_prog_items = {player for player in game_players if
            multiworld.worlds[player].required_shines > 0 or multiworld.worlds[player].blue_coins_required > 0}
        # Get the player IDs of those that are using minimal accessibility.
        sms_minimal_players = {player for player in game_players
            if multiworld.worlds[player].options.accessibility == "minimal"}

        def sort_func(item: Item):
            # Credit once again for @Mysteryem for this function AND very nice description
            if item.player in sms_excessive_prog_items and item.name in ["Shine Sprite", "Blue Coin"]:
                if item.player in sms_minimal_players:
                    # For minimal players, place goal macguffins first. This helps prevent fill from dumping logically
                    # relevant items into unreachable locations and reducing the number of reachable locations to fewer
                    # than the number of items remaining to be placed.
                    #
                    # Placing only the non-required goal macguffins first or slightly more than the number of
                    # non-required goal macguffins first was also tried, but placing all goal macguffins first seems to
                    # give fill the best chance of succeeding.
                    #
                    # All shine sprites and blue coins are given the *deprioritized* classification for minimal players,
                    # which avoids them being placed on priority locations, which would otherwise occur due to them
                    # being sorted to be placed first. They also skip progression balancing in larger multiworlds.
                    return 1
                else:
                    # For non-minimal players, place goal macguffins last. The helps prevent fill from filling most/all
                    # reachable locations with the goal macguffins that are only required for the goal.
                    return -1
            else:
                # Python sorting is stable, so this will leave everything else in its original order.
                return 0

        progitempool.sort(key=sort_func)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: dict = {}

        # This gets all the names of the options from both the world's option class and the inherited class as sets
        # Since this world's options inherit from PerGameCommonOptions, there will be duplicates.
        child_local_fields = set({f.name for f in fields(SmsOptions)})
        parent_fields = set({f.name for f in fields(PerGameCommonOptions)})

        # Subtract the elements to find the options only unique to this world, then sort them to avoid any
        #   deterministic issues.
        only_in_child = sorted(list(child_local_fields - parent_fields))

        # Output the value of each based on the option type.
        for child_option in only_in_child:
            slot_data[child_option] = getattr(self.options, child_option).value

        slot_data["required_shines"] = self.required_shines
        slot_data["death_link"] = self.options.death_link.value
        slot_data["seed"] = str(self.multiworld.seed_name)
        slot_data["ticket_chosen"] = self.ticket_chosen
        return slot_data

    def generate_output(self, output_directory: str):
        from .iso_helper.sms_rom import SMSPlayerContainer # circular import nonsense
        output_data = {
            "Seed": str(self.multiworld.seed_name),
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {},
            "Version": WORLD_VERSION
        }

        for field in fields(self.options):
            if "plando" in field.name.lower():
                continue
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        output_data["required_shines"] = self.required_shines

        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
            f"{SMSPlayerContainer.patch_file_ending}")
        sms_container = SMSPlayerContainer(output_data, patch_path, self.multiworld.player_name[self.player], self.player)
        sms_container.write()