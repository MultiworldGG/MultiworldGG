# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

import json
import logging
import math
import os
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TextIO, cast

from BaseClasses import Item, Location, Region, Tutorial
from BaseClasses import ItemClassification as IClass
from BaseClasses import LocationProgressType as LPType
from Fill import fast_fill
from Options import OptionError

from worlds.AutoWorld import WebWorld, World

from .items import Episode, LocalItem, LocalItemData
from .locations import LevelLocationData, LevelRegion
from .logic import DamageTables, set_level_rules
from .options import TyrianOptions, tyrian_option_groups
from .twiddles import Twiddle, generate_twiddles

if TYPE_CHECKING:
    from BaseClasses import MultiWorld


class TyrianItem(Item):
    game = "Tyrian"


class TyrianLocation(Location):
    game = "Tyrian"

    shop_price: int | None  # None if not a shop, price in credits if it is

    def __init__(self, player: int, name: str, address: int | None, parent: Region):
        super().__init__(player, name, address, parent)
        self.shop_price = None


class TyrianWebWorld(WebWorld):
    game = "Tyrian"
    option_groups = tyrian_option_groups
    theme = "partyTime"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to playing Tyrian with MultiworldGG.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Kaito Sinclaire"]
        ),
        Tutorial(
            "Excluded and Commonly Missed Locations",
            "A list of locations that are commonly missed and excluded on lower logic difficulties, and descriptions of how to obtain them.",  # noqa: E501
            "English",
            "locations_en.md",
            "locations/en",
            ["Kaito Sinclaire"]
        ),
    ]


class TyrianWorld(World):
    """
    Tyrian is a PC SHMUP originally released in 1995, and then re-released as Tyrian 2000 in 1999. Follow space pilot
    Trent Hawkins in the year 20,031 as he flies through the galaxy to defend it from the evil corporation, Microsol.
    This randomizer supports both versions of the game.
    """
    game = "Tyrian"
    web = TyrianWebWorld()
    options_dataclass = TyrianOptions
    options: TyrianOptions  # type: ignore

    base_id = 20031000
    item_name_to_id = LocalItemData.get_item_name_to_id(base_id)
    item_name_groups = LocalItemData.get_item_groups()
    location_name_to_id = LevelLocationData.get_location_name_to_id(base_id)
    location_name_groups = LevelLocationData.get_location_groups()

    # Raise this to force outdated clients to update.
    aptyrian_net_version = 7

    # --------------------------------------------------------------------------------------------

    goal_episodes: set[int]  # Require these episodes for goal (1, 2, 3, 4, 5)
    play_episodes: set[int]  # Add levels from these episodes (1, 2, 3, 4, 5)

    default_start_level: str  # Level we start on, gets precollected automatically
    all_levels: list[str]  # List of all levels available in seed
    local_itempool: list[str]  # String-based item pool for us, becomes multiworld item pool after create_items

    single_special_weapon: str | None  # For output to spoiler log only
    twiddles: list[Twiddle]  # Twiddle/SF Code inputs and their results.

    weapon_costs: dict[str, int]  # Costs of each weapon's upgrades (see LocalItemData.default_upgrade_costs)
    total_money_needed: int  # Sum total of shop prices and max upgrades, used to calculate filler items

    damage_tables: DamageTables  # Used for rule generation

    # ================================================================================================================
    # Item / Location Helpers
    # ================================================================================================================

    def create_item(self, name: str) -> TyrianItem:
        pool_data = LocalItemData.get(name)
        return TyrianItem(name, pool_data.item_class, self.item_name_to_id[name], self.player)

    def create_level_location(self, name: str, region: Region) -> TyrianLocation:
        loc = TyrianLocation(self.player, name, self.location_name_to_id[name], region)

        region.locations.append(loc)
        return loc

    def create_shop_location(self, name: str, region: Region, region_data: LevelRegion) -> TyrianLocation:
        loc = TyrianLocation(self.player, name, self.location_name_to_id[name], region)

        loc.shop_price = 0  # Give a default int value for shops
        region_data.set_random_shop_price(self, loc)
        self.total_money_needed += loc.shop_price

        region.locations.append(loc)
        return loc

    def create_event(self, name: str, region: Region) -> TyrianLocation:
        loc = TyrianLocation(self.player, name[0:9], None, region)
        loc.place_locked_item(TyrianItem(name, IClass.progression, None, self.player))

        region.locations.append(loc)
        return loc

    # ================================================================================================================
    # Item Pool Methods
    # ================================================================================================================

    def get_dict_contents_as_items(self, target_dict: Mapping[str, LocalItem]) -> list[str]:
        item_list = []

        for (name, item) in target_dict.items():
            if item.count > 0:
                item_list.extend([name] * item.count)

        return item_list

    def get_junk_items(self, total_checks: int, total_money: int, allow_superbombs: bool = True) -> list[str]:
        valid_money_amounts = [int(name.removesuffix(" Credits"))
                               for name in LocalItemData.other_items if name.endswith(" Credits")]

        junk_list = []

        while total_checks > 1:
            # Target credit total has been overshot
            if total_money <= 0:
                junk_list.extend(["SuperBomb" if allow_superbombs else "50 Credits"] * total_checks)
                return junk_list

            # We want to allow a wide range of money values early, but then tighten up our focus as we start running
            # low on items remaining. This way we get a good variety of credit values while not straying too far
            # from the target value.
            average = total_money / total_checks
            avg_divisor = total_checks / 1.5 if total_checks > 3 else 2
            possible_choices = [i for i in valid_money_amounts if i > average / avg_divisor and i < average * 5]

            # If the low end of the scale is _really_ low, include a SuperBomb as a choice.
            if allow_superbombs and average / avg_divisor < 20:
                possible_choices.append(0)

            # In case our focus is a little _too_ tight and we don't actually have any money values close enough to
            # the average, just pick the next highest one above the average. That'll help ensure we're always over
            # the target value, and never under it.
            if len(possible_choices) == 0:
                item_choice = next(i for i in valid_money_amounts if i >= average)
            else:
                item_choice = self.random.choice(possible_choices)

            total_money -= item_choice
            total_checks -= 1
            junk_list.append(f"{item_choice} Credits" if item_choice != 0 else "SuperBomb")

        # No point being random here. Just pick the first credit value that puts us over the target value.
        if total_checks == 1:
            item_choice = next(i for i in valid_money_amounts if i >= total_money)
            junk_list.append(f"{item_choice} Credits")

        return junk_list

    # ================================================================================================================
    # Option Parsing Helpers
    # ================================================================================================================

    def get_weapon_costs(self) -> dict[str, int]:
        if self.options.base_weapon_cost.current_key == "original":
            return {key: value.original for (key, value) in LocalItemData.default_upgrade_costs.items()}
        elif self.options.base_weapon_cost.current_key == "balanced":
            return {key: value.balanced for (key, value) in LocalItemData.default_upgrade_costs.items()}
        elif self.options.base_weapon_cost.current_key == "randomized":
            return {key: self.random.randrange(400, 1801, 50)
                    for key in LocalItemData.default_upgrade_costs.keys()}
        else:
            return {key: int(self.options.base_weapon_cost.current_key)
                    for key in LocalItemData.default_upgrade_costs.keys()}

    def get_starting_weapon_name(self) -> str:
        if not self.options.random_starting_weapon:
            return "Pulse-Cannon"

        if self.options.logic_difficulty == "no_logic":
            # Anything is permissible in no_logic, regardless of circumstances
            possible_choices = [item for item in self.local_itempool if item in LocalItemData.front_ports]
            return self.random.choice(possible_choices)

        starting_generator = 1
        starting_power_level = 1
        base_energy = 0

        # Get the amount of energy and power level we'll start the seed with
        for item in self.multiworld.precollected_items[self.player]:
            if item.name == "Advanced MR-12":
                base_energy = max(base_energy, self.damage_tables.local_power_provided[2])
            elif item.name == "Gencore Custom MR-12":
                base_energy = max(base_energy, self.damage_tables.local_power_provided[3])
            elif item.name == "Standard MicroFusion":
                base_energy = max(base_energy, self.damage_tables.local_power_provided[4])
            elif item.name == "Advanced MicroFusion":
                base_energy = max(base_energy, self.damage_tables.local_power_provided[5])
            elif item.name == "Gravitron Pulse-Wave":
                base_energy = max(base_energy, self.damage_tables.local_power_provided[6])
            elif item.name == "Progressive Generator":
                starting_generator += 1
            elif item.name == "Maximum Power Up":
                starting_power_level += 1
        if base_energy == 0:
            base_energy = self.damage_tables.local_power_provided[starting_generator]

        # If the weapon at any power level has energy usage below our starting generator's power, we can use it
        def can_use_from_start(weapon_name: str) -> bool:
            nonlocal base_energy, starting_power_level

            # Forbid the Orange Juicer from power level 1 starts because power 1 only shoots straight right
            if starting_power_level == 1 and weapon_name == "The Orange Juicer":
                return False

            lowest_power = min(DamageTables.generator_power_required[weapon_name][0:starting_power_level])
            return lowest_power <= base_energy

        possible_choices = [item for item in self.local_itempool
                            if item in LocalItemData.front_ports and can_use_from_start(item)]

        # List is empty? Pick totally randomly among everything available in the seed
        if len(possible_choices) == 0:
            possible_choices = [item for item in self.local_itempool if item in LocalItemData.front_ports]

        return self.random.choice(possible_choices)

    def get_filler_item_name(self) -> str:
        filler_items = (["50 Credits", "75 Credits", "100 Credits", "150 Credits", "200 Credits", "300 Credits",
                         "375 Credits", "500 Credits", "750 Credits"] * 2) + ["1000 Credits", "SuperBomb"]
        return self.random.choice(filler_items)

    # ================================================================================================================
    # Slot Data / File Output
    # ================================================================================================================

    # ---------- Settings -----------------------------------------------------
    # Game settings, user choices the game needs to know about.
    # Present: Always.
    def output_settings(self) -> dict[str, Any]:
        settings: dict[str, Any] = {
            "RequireT2K": bool(self.options.enable_tyrian_2000_support),
            "Episodes": sum(1 << (i - 1) for i in self.play_episodes),
            "Goal": sum(1 << (i - 1) for i in self.goal_episodes),
            "Difficulty": int(self.options.difficulty),
            "LogicDifficulty": int(self.options.logic_difficulty),  # For trackers
        }

        # The following settings are only added if their values are truthy or non-zero
        # The client should handle their absence just fine (defaulting to false or 0)
        if self.options.data_cube_hunt:
            settings["DataCubesNeeded"] = int(self.options.data_cubes_required)
        if self.options.contact_bypasses_shields:
            settings["HardContact"] = True
        if self.options.allow_excess_armor:
            settings["ExcessArmor"] = True
        if self.options.force_game_speed != "off":
            settings["GameSpeed"] = int(self.options.force_game_speed)

        if self.options.shop_mode != "none":
            settings["ShopMode"] = int(self.options.shop_mode)
        if self.options.specials == "as_items":
            settings["SpecialMenu"] = True
        if self.options.christmas_mode:
            settings["Christmas"] = True
        if self.options.death_link:
            settings["DeathLink"] = True

        return settings

    # ---------- ExcludedLocations --------------------------------------------
    # Which locations are excluded. Used to show them differently in the client.
    # Present: Always.
    def output_excluded_locations(self) -> list[int]:
        return [location.address - self.base_id for location in self.multiworld.get_locations(self.player)
                if location.address is not None and location.progress_type == LPType.EXCLUDED]

    # ---------- StartState (obfuscated) --------------------------------------
    # Tell the game what we start with.
    # Present: Always. (Optional in theory, but in practice there will always at least be the starting level.)
    def output_start_state(self) -> dict[str, Any]:
        start_state: dict[str, Any] = {}

        def increase_state(option: str) -> None:
            nonlocal start_state
            start_state[option] = start_state.get(option, 0) + 1

        def set_state(option: str, value: int) -> None:
            nonlocal start_state
            start_state[option] = max(start_state.get(option, 0), value)

        def append_state(option: str, value: str) -> None:
            nonlocal start_state
            if option not in start_state:
                start_state[option] = []
            # May as well give the game the ID number it's already expecting if it saves 5+ bytes to do so
            start_state[option].append(self.item_name_to_id[value] - self.base_id)

        def add_credits(value: str) -> None:
            nonlocal start_state
            credit_count = int(value.removesuffix(" Credits"))
            start_state["Credits"] = start_state.get("Credits", 0) + credit_count

        if self.options.starting_money > 0:
            start_state["Credits"] = self.options.starting_money.value

        for item in self.multiworld.precollected_items[self.player]:
            if item.name in LocalItemData.levels:            append_state("Items", item.name)
            elif item.name in LocalItemData.front_ports:     append_state("Items", item.name)
            elif item.name in LocalItemData.rear_ports:      append_state("Items", item.name)
            elif item.name in LocalItemData.special_weapons: append_state("Items", item.name)
            elif item.name in LocalItemData.sidekicks:       append_state("Items", item.name)
            elif item.name in LocalItemData.bonus_games:     append_state("Items", item.name)
            elif item.name == "Data Cube":                   increase_state("DataCubes")
            elif item.name == "Armor Up":                    increase_state("Armor")
            elif item.name == "Maximum Power Up":            increase_state("Power")
            elif item.name == "Shield Up":                   increase_state("Shield")
            elif item.name == "Progressive Generator":       increase_state("Generator")
            elif item.name == "Advanced MR-12":              set_state("Generator", 1)
            elif item.name == "Gencore Custom MR-12":        set_state("Generator", 2)
            elif item.name == "Standard MicroFusion":        set_state("Generator", 3)
            elif item.name == "Advanced MicroFusion":        set_state("Generator", 4)
            elif item.name == "Gravitron Pulse-Wave":        set_state("Generator", 5)
            elif item.name == "Solar Shields":               start_state["SolarShield"] = True
            elif item.name == "SuperBomb":                   pass  # Only useful if obtained in level, ignore
            elif item.name.endswith(" Credits"):             add_credits(item.name)
            else:
                raise Exception(f"Unknown item '{item.name}' in precollected items")

        return start_state

    # ---------- WeaponCost (obfuscated) --------------------------------------
    # Base cost of each weapon's upgrades
    # Present: Always.
    def output_weapon_cost(self) -> dict[int, int]:
        return {self.item_name_to_id[key] - self.base_id: value for (key, value) in self.weapon_costs.items()}

    # ---------- TwiddleData (obfuscated) -------------------------------------
    # Twiddle inputs, costs, etc.
    # Present: If the option "Twiddles" is not set to "off".
    def output_twiddles(self) -> list[dict[str, Any]]:
        return [twiddle.to_json() for twiddle in self.twiddles]

    # ---------- ProgressionData (obfuscated) ---------------------------------
    # Which locations contain progression items for any player.
    # Present: Only in slot_data (remote games).
    def output_progression_data(self) -> list[int]:
        return [location.address - self.base_id for location in self.multiworld.get_locations(self.player)
                if location.address is not None and location.item is not None
                and getattr(location, "shop_price", None) is None  # Ignore shop items (they're scouted in game)
                and location.item.advancement]

    # ---------- LocationMax --------------------------------------------------
    # Total number of locations available.
    # Present: Only in slot_data (remote games).
    def output_location_count(self) -> int:
        return len([loc for loc in self.multiworld.get_locations(self.player) if loc.address is not None])

    # ---------- LocationData (obfuscated) ------------------------------------
    # The contents of every single location present in the player's game. Single player only.
    # Present: Only in local/offline .aptyrian files.
    def output_all_locations(self) -> dict[int, str]:
        assert self.multiworld.players == 1

        def get_location_item(location: Location) -> str:
            assert location.item is not None and location.item.code is not None
            return f"{'!' if location.item.advancement else ''}{location.item.code - self.base_id}"

        return {location.address - self.base_id: get_location_item(location)
                for location in self.multiworld.get_locations(self.player)
                if location.address is not None and location.item is not None}

    # ---------- ShopData (obfuscated) ----------------------------------------
    # The price of every shop present in the player's world.
    # Present: If the option "Shop Mode" is not set to "none".
    def output_shop_data(self) -> dict[int, int]:
        def correct_shop_price(location: TyrianLocation) -> int:
            assert location.shop_price is not None  # Tautological

            # If the shop has credits, and the cost is more than you'd gain, reduce the cost.
            # Don't do this in hidden mode, though, since the player shouldn't have any idea what each item is.
            if self.options.shop_mode != "hidden" and location.item is not None \
                  and location.item.player == self.player and location.item.name.endswith(" Credits"):
                credit_amount = int(location.item.name.removesuffix(" Credits"))
                adjusted_shop_price = location.shop_price % credit_amount
                return adjusted_shop_price if adjusted_shop_price != 0 else credit_amount
            return location.shop_price

        return {location.address - self.base_id: correct_shop_price(cast(TyrianLocation, location))
                for location in self.multiworld.get_locations(self.player)
                if location.address is not None  # Ignore events
                and getattr(location, "shop_price", None) is not None}

    # --------------------------------------------------------------------------------------------

    def obfuscate_object(self, input_obj: Any) -> str:
        # Every character the small font can display.
        input_chars = " ABCDEFGHIJKLMNOPQRSTUVWXYZ!?.,;:'\"abcdefghijklmnopqrstuvwxyz#$%*(){}[]1234567890/|\\-+="
        # Three characters are replaced by obfuscation: Single quotes, double quotes, and backslashes.
        # They are replaced by left and right brackets, and a tilde.
        obfus_chars = "0GTi29}#{K+d O1VYr]en:zP~yAI5(,ZL/)|?.sb4l<MFU3tD6$>wp[f*q%C=o8Emgj;xuXakhW!SNHc-Q7RBJv"
        # The sole point of this is to be relatively fast and simple to encode and decode, while keeping information
        # from being visible easily from just looking at the JSON file.
        offset = 54

        input_str = json.dumps(input_obj, separators=(",", ":"))

        def obfuscate_char(in_chr: str) -> str:
            nonlocal offset
            try:
                idx = input_chars.index(in_chr) + offset
                offset += (ord(in_chr) & 0xF) + 1
            except ValueError:
                idx = input_chars.index("?") + offset
                offset += (ord("?") & 0xF) + 1

            if idx >= 87:
                idx -= 87
            if offset >= 87:
                offset -= 87
            return obfus_chars[idx]

        return "".join(obfuscate_char(i) for i in input_str)

    # --------------------------------------------------------------------------------------------

    def get_slot_data(self, local_mode: bool = False) -> dict[str, Any]:
        # local_mode: If true, return a JSON file meant to be downloaded, for offline play
        slot_data = {
            "NetVersion": self.aptyrian_net_version,
            "Settings": self.output_settings(),
            "ExcludedLocations": self.output_excluded_locations(),
            "StartState": self.obfuscate_object(self.output_start_state()),
            "WeaponCost": self.obfuscate_object(self.output_weapon_cost()),
        }

        if local_mode:  # Local mode: Output all location contents
            slot_data["Seed"] = self.multiworld.seed_name  # Needed for savegames
            slot_data["LocationData"] = self.obfuscate_object(self.output_all_locations())
        else:  # Remote mode: Just output a list of location IDs that contain progression
            slot_data["ProgressionData"] = self.obfuscate_object(self.output_progression_data())
            slot_data["LocationMax"] = self.output_location_count()

        if self.options.twiddles:
            slot_data["TwiddleData"] = self.output_twiddles()
        if self.options.shop_mode != "none":
            slot_data["ShopData"] = self.obfuscate_object(self.output_shop_data())

        return slot_data

    # ================================================================================================================
    # Main Generation Steps
    # ================================================================================================================

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        # Import code that affects other worlds; must happen after all worlds are loaded
        # See crossgame/__init__.py for more info
        from .crossgame import alttp  # noqa: F401

    def generate_early(self) -> None:
        if not self.options.enable_tyrian_2000_support:
            self.options.episode_5.value = 0

        self.goal_episodes = set()
        if self.options.episode_1 == 2: self.goal_episodes.add(Episode.Escape)
        if self.options.episode_2 == 2: self.goal_episodes.add(Episode.Treachery)
        if self.options.episode_3 == 2: self.goal_episodes.add(Episode.MissionSuicide)
        if self.options.episode_4 == 2: self.goal_episodes.add(Episode.AnEndToFate)
        if self.options.episode_5 == 2: self.goal_episodes.add(Episode.HazudraFodder)

        self.play_episodes = set()
        if self.options.episode_1 != 0: self.play_episodes.add(Episode.Escape)
        if self.options.episode_2 != 0: self.play_episodes.add(Episode.Treachery)
        if self.options.episode_3 != 0: self.play_episodes.add(Episode.MissionSuicide)
        if self.options.episode_4 != 0: self.play_episodes.add(Episode.AnEndToFate)
        if self.options.episode_5 != 0: self.play_episodes.add(Episode.HazudraFodder)

        # Default to at least playing episode 1
        if len(self.play_episodes) == 0:
            logging.warning(f"No episodes were enabled in {self.multiworld.get_player_name(self.player)}'s "
                            f"Tyrian world. Defaulting to Episode 1 (Escape).")
            self.play_episodes = {Episode.Escape}
            self.goal_episodes = {Episode.Escape}

        # If no goals, make all selected episodes goals by default
        if len(self.goal_episodes) == 0:
            logging.warning(f"No episodes were marked as goals in {self.multiworld.get_player_name(self.player)}'s "
                            f"Tyrian world. Defaulting to all playable episodes.")
            self.goal_episodes = self.play_episodes

        if Episode.Escape in self.play_episodes:           self.default_start_level = "TYRIAN (Episode 1)"
        elif Episode.Treachery in self.play_episodes:      self.default_start_level = "TORM (Episode 2)"
        elif Episode.MissionSuicide in self.play_episodes: self.default_start_level = "GAUNTLET (Episode 3)"
        elif Episode.AnEndToFate in self.play_episodes:    self.default_start_level = "SURFACE (Episode 4)"
        else:                                              self.default_start_level = "ASTEROIDS (Episode 5)"

        self.weapon_costs = self.get_weapon_costs()
        self.total_money_needed = max(self.weapon_costs.values()) * 220

        self.damage_tables = DamageTables(self.options.logic_difficulty.value)

        # May as well generate twiddles now, if the options are set.
        if self.options.twiddles:
            self.twiddles = generate_twiddles(self, False)
        else:
            self.twiddles = []

        self.single_special_weapon = None
        self.all_levels = []
        self.local_itempool = []

        # ----------------------------------------------------------------------------------------
        # Clean up some option values.

        # Data Cube Hunt related options
        if self.options.data_cubes_total.value == 0:
            # Set total to (required * total_percentage) if in percentage mode
            new_cube_total = int(self.options.data_cubes_required * (self.options.data_cubes_total_percent / 100))
            self.options.data_cubes_total.value = new_cube_total
        elif self.options.data_cubes_total.value < self.options.data_cubes_required.value:
            # Raise total to at least match required
            self.options.data_cubes_total.value = self.options.data_cubes_required.value

        # Turn start_inventory non-progressive generators into progressive ones, and vice versa, depending on options.
        # We do this so we can try to ensure consistent behavior among the client, starting item output, and logic.
        if self.options.progressive_items:
            # Initialization of this dict will remove all non-progressive generators from start_inventory for us.
            # We still want to get rid of lower level ones even if we don't acknowledge them later on.
            nonprogressive_generators = {
                5: self.options.start_inventory.value.pop("Gravitron Pulse-Wave", 0),
                4: self.options.start_inventory.value.pop("Advanced MicroFusion", 0),
                3: self.options.start_inventory.value.pop("Standard MicroFusion", 0),
                2: self.options.start_inventory.value.pop("Gencore Custom MR-12", 0),
                1: self.options.start_inventory.value.pop("Advanced MR-12", 0),
            }

            # Now give enough Progressive Generators to reach the highest level we saw.
            for to_give, num_precollected in nonprogressive_generators.items():
                if num_precollected > 0:
                    # This will overwrite any Progressive Generators already in start_inventory, but I think that's a
                    # fair assumption to make when you throw a non-progressive generator in here in the first place.
                    self.options.start_inventory.value["Progressive Generator"] = to_give
                    break
        else:
            # Get rid of all progressive generators from start_inventory.
            progressive_count = self.options.start_inventory.value.pop("Progressive Generator", 0)
            progressive_count = min(progressive_count, 5)  # Cap at Gravitron Pulse-Wave

            # Take the count of progressive generators we popped out, and convert them to a single non-progressive one.
            if progressive_count > 0:
                generator = ["Advanced MR-12", "Gencore Custom MR-12", "Standard MicroFusion",
                             "Advanced MicroFusion", "Gravitron Pulse-Wave"][progressive_count - 1]
                self.options.start_inventory.value[generator] = 1

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_hub_region = Region("Play Next Level", self.player, self.multiworld)
        self.multiworld.regions.append(main_hub_region)
        menu_region.connect(main_hub_region)

        # ==============
        # === Levels ===
        # ==============

        # Before we start, track levels the player wants removed.
        removed_levels = []
        for removed_item in self.options.remove_from_item_pool.keys():
            if removed_item not in LocalItemData.levels:
                continue
            removed_levels.append(removed_item)

        def recursive_create_subregions(locations: dict[str, Any], parent_region: Region) -> None:
            for name, value in locations.items():
                # Create a new subregion, recurse to add subregions/locations to it
                if type(value) is dict:
                    new_subregion = Region(f"{name} (subregion)", self.player, self.multiworld)
                    parent_region.connect(new_subregion, name)
                    self.multiworld.regions.append(new_subregion)
                    recursive_create_subregions(value, new_subregion)

                # Create a shop subregion, that we'll fill in later.
                elif type(value) is tuple:
                    # Create a shop subregion that will be filled in later
                    shop_region = Region(name, self.player, self.multiworld)
                    parent_region.connect(shop_region, f"{name} @ Shop Open")
                    self.multiworld.regions.append(shop_region)

                # Create a new location attached to this region.
                else:
                    self.create_level_location(name, parent_region)

        for (name, region_info) in LevelLocationData.level_regions.items():
            if region_info.episode not in self.play_episodes:
                continue
            if name in removed_levels:
                continue

            self.all_levels.append(name)
            self.local_itempool.append(name)

            # Create the region for the level and connect it to the hub
            level_start_region = Region(f"{name} @ Start", self.player, self.multiworld)
            main_hub_region.connect(level_start_region, f"{name} @ Start")
            self.multiworld.regions.append(level_start_region)

            # Create all locations and subregions now
            recursive_create_subregions(region_info.locations, parent_region=level_start_region)

        # =============
        # === Shops ===
        # =============

        # If we have shops enabled, then let's figure out how to divvy up their locations!
        if self.options.shop_mode != "none":
            # One of the "always_x" choices, add each level shop exactly x times
            if self.options.shop_item_count <= -1:
                times_to_add = abs(self.options.shop_item_count.value)
                items_per_shop = dict.fromkeys(self.all_levels, times_to_add)

            # Not enough items for one in every shop
            elif self.options.shop_item_count < len(self.all_levels):
                items_per_shop = dict.fromkeys(self.all_levels, 0)
                for level in self.random.sample(self.all_levels, self.options.shop_item_count.value):
                    items_per_shop[level] = 1

            # More than enough items to go around
            else:
                # Silently correct too many items to just cap at the max
                total_item_count: int = min(self.options.shop_item_count.value, len(self.all_levels) * 5)

                # First guarantee every shop has at least one
                items_per_shop = dict.fromkeys(self.all_levels, 1)
                total_item_count -= len(self.all_levels)

                # Then get a random sample of a list where every level is present four times
                # This gives us between 1 to 5 items in every level
                for level in self.random.sample(self.all_levels * 4, total_item_count):
                    items_per_shop[level] += 1

            # ------------------------------------------------------------------------------------

            for level in self.all_levels:
                # Just get the shop region we made earlier
                shop_region = self.multiworld.get_region(f"Shop - {level}", self.player)
                region_data = LevelLocationData.level_regions[level]

                for i in range(items_per_shop[level]):
                    shop_loc_name = f"Shop - {level} - Item {i + 1}"
                    self.create_shop_location(shop_loc_name, shop_region, region_data)

        # ==============
        # === Events ===
        # ==============

        all_events = []
        episode_num = 0
        for (event_name, level_name) in LevelLocationData.events.items():
            episode_num += 1
            if episode_num not in self.goal_episodes:
                continue

            if level_name in removed_levels:
                raise OptionError(f"Cannot remove '{level_name}' from the item pool"
                                  f" because it's required to complete the goal."
                                  f"\nIf you want to do this, change the Episode {episode_num} option"
                                  f" to 'on' instead of 'goal'.")

            all_events.append(event_name)
            self.create_event(event_name, menu_region)

        # Victory condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(all_events, self.player)

    def create_items(self) -> None:

        def pop_from_pool(item_name: str) -> str | None:
            if item_name in self.local_itempool:  # Regular item
                self.local_itempool.remove(item_name)
                return item_name
            return None

        # ----------------------------------------------------------------------------------------
        # Add base items to the pool.

        LocalItemData.set_tyrian_2000_items(bool(self.options.enable_tyrian_2000_support))

        # Level items are added into the pool in create_regions.
        self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.front_ports))
        self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.rear_ports))
        self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.sidekicks))
        self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.other_items))

        if self.options.specials == "as_items":
            self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.special_weapons))

        if self.options.progressive_items:
            self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.progressive_items))
        else:
            self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.nonprogressive_items))

        if self.options.add_bonus_games:
            self.local_itempool.extend(self.get_dict_contents_as_items(LocalItemData.bonus_games))
        else:
            all_bonus_games = self.get_dict_contents_as_items(LocalItemData.bonus_games)
            for bonus_game in all_bonus_games:
                self.multiworld.push_precollected(self.create_item(bonus_game))

        if self.options.data_cube_hunt:
            # Earlier code will ensure this is set to a final value already.
            self.local_itempool.extend(["Data Cube"] * self.options.data_cubes_total.value)

            # Remove goal levels from the itempool.
            [pop_from_pool(name) for (name, details) in LocalItemData.levels.items()
                  if details.goal_level and details.episode in self.goal_episodes]

        # ----------------------------------------------------------------------------------------
        # Handle pre-collected items, remove requests, other options.

        precollected_level_exists = False
        precollected_weapon_exists = False

        # Remove precollected (starting inventory) items from the pool.
        for precollect in self.multiworld.precollected_items[self.player]:
            name = pop_from_pool(precollect.name)
            if name in LocalItemData.levels:  # Allow starting level override (dangerous logic-wise, but whatever)
                precollected_level_exists = True
            elif name in LocalItemData.front_ports:  # Allow default weapon override
                precollected_weapon_exists = True

        # Remove items we've been requested to remove from the pool.
        for (removed_item, remove_count) in self.options.remove_from_item_pool.items():
            for i in range(remove_count):
                pop_from_pool(removed_item)

        # If requested, pull max power upgrades from the pool and give them to the player.
        for i in range(1, self.options.starting_max_power):
            max_power_item = pop_from_pool("Maximum Power Up")
            if max_power_item is not None:
                self.multiworld.push_precollected(self.create_item(max_power_item))

        if not precollected_level_exists:
            # Precollect the default starting level and pop it from the item pool.
            start_level = pop_from_pool(self.default_start_level)
            if start_level is not None:
                self.multiworld.push_precollected(self.create_item(start_level))
            else:
                raise OptionError(f"Cannot remove default starting level from the item pool."
                                  f" (tried to remove '{self.default_start_level}')"
                                  f"\nIf you want to do this, add another level to start_inventory.")

        if not precollected_weapon_exists:
            # Pick a starting weapon and pull it from the pool.
            start_weapon_name = self.get_starting_weapon_name()
            start_weapon = pop_from_pool(start_weapon_name)
            if start_weapon is not None:
                self.multiworld.push_precollected(self.create_item(start_weapon))
            else:
                raise OptionError(f"Cannot remove default starting weapon from the item pool."
                                  f" (tried to remove '{start_weapon_name}')"
                                  f"\nIf you want to do this, add another front weapon to start_inventory"
                                  f" or use a random starting weapon.")

        if self.options.specials == "on":  # Get a random special, no others
            possible_specials = self.get_dict_contents_as_items(LocalItemData.special_weapons)
            self.single_special_weapon = self.random.choice(possible_specials)
            assert self.single_special_weapon is not None  # Tautological (but clues mypy in that None isn't possible)
            self.multiworld.push_precollected(self.create_item(self.single_special_weapon))

        # Mark some levels as local only, based on Local Level %
        if self.options.local_level_percent != 0:
            levels_in_pool = [level for level in self.local_itempool if level in LocalItemData.levels]
            requested_local_levels = int(len(levels_in_pool) * (self.options.local_level_percent / 100))

            levels_made_local = self.random.sample(levels_in_pool, requested_local_levels)
            self.options.local_items.value.update(levels_made_local)

            # If over 50% of the levels are marked to be local, also mark one of those local levels early.
            if self.options.local_level_percent >= 50 and requested_local_levels > 0:
                early_level = self.random.choice(levels_made_local)
                self.multiworld.early_items[self.player][early_level] = 1

        # ----------------------------------------------------------------------------------------
        # Automatically fill the pool with junk Credits items, enough to reach total_money_needed.

        # Returns remaining amount of space in itempool after tossing requested number of items
        def toss_from_itempool(num_to_toss: int) -> int:
            tossable_items = [name for name in self.local_itempool if LocalItemData.get(name).tossable]

            # Any data cubes that are more than the total required are tossable, too.
            if self.options.data_cube_hunt:
                tossable_cube_count = (self.options.data_cubes_total.value - self.options.data_cubes_required.value)
                if tossable_cube_count > 0:
                    tossable_items.extend(["Data Cube"] * tossable_cube_count)

            if num_to_toss > len(tossable_items):
                raise OptionError(f"Cannot trim enough items from the item pool in "
                                  f"{self.multiworld.get_player_name(self.player)}'s Tyrian world;"
                                  f" need to remove {num_to_toss}, but only {len(tossable_items)} can be removed."
                                  f" Please adjust your settings to add more locations.")

            [pop_from_pool(i) for i in self.random.sample(tossable_items, num_to_toss)]
            logging.warning(f"Trimming {num_to_toss} item{'' if num_to_toss == 1 else 's'} "
                            f"from {self.multiworld.get_player_name(self.player)}'s Tyrian world.")

            return len(self.multiworld.get_unfilled_locations(self.player)) - len(self.local_itempool)

        # Subtract what we start with, and then scale as requested.
        # Catch negative money needed (because we start with more than we need) and set to zero.
        self.total_money_needed -= self.options.starting_money.value
        self.total_money_needed = max(0, int(self.total_money_needed * (self.options.money_pool_scale / 100)))

        # Shops-only mode junk fill
        if self.options.shop_mode == "shops_only":
            # Warn on currently unsupported option combinations (that we still allow generation of, for the daring)
            if self.options.logic_difficulty != "no_logic" and self.options.logic_difficulty != "master":
                if self.multiworld.players == 1:
                    raise OptionError(f"Cowardly refusing to generate a solo 'shops_only' game for "
                                      f"{self.multiworld.get_player_name(self.player)} "
                                      f"due to improper logic difficulty settings. "
                                      f"A logic difficulty of 'master' or 'no logic' is required.")
                logging.warning(f"{self.multiworld.get_player_name(self.player)}:"
                                f" Shop mode 'shops_only' is not designed for these logic settings."
                                f" You may experience an empty sphere 1, or failed generations in solo play.")

            # We're going to take all locations that are not shop locations, and pre-fill all of them with
            # junk Credits items. This gives shops a wide variety of items, while still giving a way to earn money.
            in_level_locations = [location for location in self.multiworld.get_unfilled_locations(self.player)
                  if getattr(location, "shop_price", None) is None]
            junk_items = [cast(Item, self.create_item(item)) for item in
                  self.get_junk_items(len(in_level_locations), self.total_money_needed, allow_superbombs=False)]

            fast_fill(self.multiworld, junk_items, in_level_locations)
            for location in in_level_locations:
                location.locked = True

            shop_locs_size = len(self.multiworld.get_unfilled_locations(self.player))
            item_pool_size = len(self.local_itempool)
            # If the itempool is too small for the shop location pool, add some random filler to make up for it.
            if item_pool_size < shop_locs_size:
                need_to_add = shop_locs_size - item_pool_size
                self.local_itempool.extend([self.get_filler_item_name() for i in range(need_to_add)])
            # If it's too big, however, trim down items to fit.
            elif item_pool_size > shop_locs_size:
                need_to_toss = item_pool_size - shop_locs_size
                toss_from_itempool(need_to_toss)

        # Traditional junk fill
        else:
            # Size of itempool versus number of locations. May be negative (!), will be fixed shortly if it is.
            rest_item_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.local_itempool)

            # Don't spam the seed with SuperBombs; lower limit to 200 credits per base item in the junk pool.
            self.total_money_needed = max(200 * rest_item_count, self.total_money_needed)

            # We want to at least have SOME variety of credit items in the pool regardless of settings.
            # We also don't want to leave ourselves with a situation where, say,
            # we can only place one junk item so it MUST be 1,000,000 credits.

            # So, if rest_item_count doesn't allow for us to stay under an average of 50,000 credits per junk item,
            # (or if rest_item_count is negative in the first place), we'll toss stuff from the pool to make space.
            minimum_needed_item_count = math.ceil(self.total_money_needed / 50000)
            if rest_item_count < minimum_needed_item_count:
                need_to_toss = minimum_needed_item_count - rest_item_count
                rest_item_count = toss_from_itempool(need_to_toss)

            self.local_itempool.extend(self.get_junk_items(rest_item_count, self.total_money_needed))

        # ----------------------------------------------------------------------------------------

        # We're finally done, dump everything we've got into the itempool
        self.multiworld.itempool.extend(self.create_item(item) for item in self.local_itempool)

    def set_rules(self) -> None:
        # Pass off rule generation to logic.py
        set_level_rules(self)

        # ==============================
        # === Automatic (base) rules ===
        # ==============================

        def create_level_unlock_rule(level_name: str) -> None:
            entrance = self.multiworld.get_entrance(f"{level_name} @ Start", self.player)
            entrance.access_rule = lambda state: state.has(level_name, self.player)

        def create_data_cube_unlock_rule(level_name: str) -> None:
            entrance = self.multiworld.get_entrance(f"{level_name} @ Start", self.player)
            entrance.access_rule = lambda state: state.has("Data Cube", self.player,
                  self.options.data_cubes_required.value)

        if self.options.data_cube_hunt:
            for level in self.all_levels:
                level_details = LocalItemData.levels[level]
                if level_details.goal_level and level_details.episode in self.goal_episodes:
                    create_data_cube_unlock_rule(level)
                else:
                    create_level_unlock_rule(level)
        else:
            for level in self.all_levels:
                create_level_unlock_rule(level)

        # ------------------------------

        def create_episode_complete_rule(event_name: str, location_name: str) -> None:
            event = self.multiworld.find_item(event_name, self.player)
            event.access_rule = lambda state: state.can_reach(location_name, "Entrance", self.player)

        for (event_name, level_name) in LevelLocationData.events.items():
            region_data = LevelLocationData.level_regions[level_name]
            if (region_data.episode not in self.goal_episodes):
                continue

            create_episode_complete_rule(event_name, f"{level_name} @ Destroy Boss")

            # If only one episode is goal, exclude anything in the shop behind the goal level.
            if len(self.goal_episodes) == 1:
                shop_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                  if loc.name.startswith(f"Shop - {level_name} - ")]

                for location in shop_locations:
                    location.progress_type = LPType.EXCLUDED

    def generate_output(self, output_directory: str) -> None:
        if self.multiworld.players != 1:
            return

        # For solo seeds, output a file that can be loaded to play the seed offline.
        local_play_filename = f"{self.multiworld.get_out_file_name_base(self.player)}.aptyrian"
        with open(os.path.join(output_directory, local_play_filename), "w") as f:
            json.dump(self.get_slot_data(local_mode=True), f)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\n\nSpecial Weapon ({self.multiworld.player_name[self.player]}):\n")
        spoiler_handle.write(f"{self.single_special_weapon}\n")

        spoiler_handle.write(f"\n\nTwiddles ({self.multiworld.player_name[self.player]}):\n")
        if len(self.twiddles) == 0:
            spoiler_handle.write("None\n")
        else:
            for twiddle in self.twiddles:
                spoiler_handle.write(twiddle.spoiler_str())

    def fill_slot_data(self) -> dict[str, Any]:
        return self.get_slot_data(local_mode=False)
