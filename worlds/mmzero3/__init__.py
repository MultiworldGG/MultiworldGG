import math
from typing import List, Dict, Any, ClassVar

from BaseClasses import Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .Items import (MMZero3Item, STORY_LATE, STORY_MID, item_data_table, item_name_groups,
                    item_table, stage_access_names, stage_names, weapon_ability_level,
                    weapon_names)
from .Locations import (MMZero3Location, location_data_table, location_name_groups, location_table,
                        locked_locations, shop_location_names)
from .Options import MMZero3Options, mmzero3_option_groups
from .Regions import region_data_table
from .Rom import MMZero3ProcedurePatch, MMZero3Settings, write_tokens
from . import Data, Palettes
from .Client import MMZero3Client

import pkgutil
import hashlib
import os
from worlds.Files import APProcedurePatch

class MMZero3WebWorld(WebWorld):
    bug_report_page = "https://github.com/brodieberger/ZeroArchipelago/"
    option_groups = mmzero3_option_groups
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Mega Man Zero 3 Randomizer connected to a MultiworldGG Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Stingrays110"]
    )
    tutorials = [setup_en]

class MMZero3World(World):
    """
    Play as Zero, kill the robots and save the day
    """

    game = "Mega Man Zero 3"
    web = MMZero3WebWorld()
    options_dataclass = MMZero3Options
    options: MMZero3Options
    settings_key = "MMZero3_settings"
    settings: ClassVar[MMZero3Settings]

    item_name_to_id = item_table
    location_name_to_id = location_table

    item_name_groups = item_name_groups
    location_name_groups = location_name_groups


    starting_weapons: set

    def generate_early(self) -> None:
        self.roll_shop_prices()
        self.roll_palettes()

        # Inform the Universal Tracker what the starting items are
        passthrough = None
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Mega Man Zero 3" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Mega Man Zero 3"]

        if passthrough:
            self.starting_weapons = set(passthrough["starting_weapons"])
        else:
            self.starting_weapons = set(self.options.starting_weapons.value)

            if not self.starting_weapons:
                self.starting_weapons = {self.random.choice(weapon_names)}

        # If it is your only weapon, add another Shield Boomerang so you can actually attack.
        if self.starting_weapons == {"Shield Boomerang"}:
            self.multiworld.push_precollected(self.create_item("Progressive Shield Boomerang"))

        # Force the first stage access item to be early local
        first_stage_access = self.random.choice(stage_access_names)
        self.multiworld.local_early_items[self.player][first_stage_access] = 1

    def starting_level(self, weapon: str) -> int:
        """How far up its chain a weapon starts. 0 means the player does not own it.

        This only really exists for the progressive item lambda fucntion.
        """
        if weapon not in self.starting_weapons:
            return 0
        if self.starting_weapons == {"Shield Boomerang"}:
            return 2
        return 1

    def create_item(self, name: str) -> MMZero3Item:
        return MMZero3Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[MMZero3Item] = []

        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}

        for name, item in item_data_table.items():
            if item.code and item.can_create(self) and name not in locked_item_names:
                item_pool.extend(self.create_item(name) for _ in range(item.count(self)))

        self.multiworld.itempool += item_pool

        # Count only the free (non-locked) locations that are actually created
        free_location_count = len([
            loc for loc in location_data_table.values()
            if loc.can_create(self) and not loc.locked_item
        ])

        filler_count = free_location_count - len(item_pool)
        if filler_count < 0:
            raise OptionError(
                f"Mega Man Zero 3 ({self.player_name}): {len(item_pool)} items for "
                f"{free_location_count} locations. Turn on extra_life_sanity or itemsanity, "
                f"or stock more shop_slots.")
        for _ in range(filler_count):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, MMZero3Location)
            region.add_exits({target: f"To {target}" for target in region_data_table[region_name].connecting_regions})

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        return "100 Energy Crystals"
    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "required_secret_disks": self.options.required_secret_disks.value,
            "ex_skill_rank": self.options.ex_skill_rank.value,
            "final_stage_rank": self.options.final_stage_rank.value,
            "starting_weapons": sorted(self.starting_weapons),
            "itemsanity": self.options.itemsanity.value,
            "extra_life_sanity": self.options.extra_life_sanity.value,
            "death_link": self.options.death_link.value,
        }

    ELF_PRICE_COSTS = (70, 100, 150, 200, 250, 300, 400, 500, 700)

    def roll_shop_prices(self) -> None:
        self.shop_prices = []
        for _ in range(self.options.shop_slots.value):
            price = self.random.choice(self.ELF_PRICE_COSTS)
            price = price * self.options.shop_price_scale.value // 100
            price = price // 10 * 10        # every vanilla elf cost is a round ten

            if price < 10:
                price = 10
            if price > 9990:
                price = 9990

            self.shop_prices.append(price)

    def add_location_rule(self, loc_name: str, rule) -> None:
        """add_rule, but skips a location disabled by seed's options."""
        if location_data_table[loc_name].can_create(self):
            add_rule(self.multiworld.get_location(loc_name, self.player), rule)

    def roll_palettes(self) -> None:
        """Decide on the palette preset that each stage will be drawn on."""
        self.stage_palettes = {}
        if not self.options.randomized_palettes.value:
            return
        for stage_id in Data.STAGE_PALETTES:
            choices = Palettes.HUES + Palettes.STAGE_THEMES[stage_id]
            self.stage_palettes[stage_id] = self.random.choice(choices)

    def set_rules(self) -> None:
        def has_weapon_at(state, weapon: str, ability: str) -> bool:
            copies_needed = weapon_ability_level(weapon, ability)
            if weapon in self.starting_weapons:
                copies_needed -= 1
            return state.has(f"Progressive {weapon}", self.player, copies_needed)

        # Breaking blocks, moving platforms, and the rod jump.
        def has_rod(state):
            return has_weapon_at(state, "Recoil Rod", "Charged Rod")

        def has_mobility(state):
            return state.has("Double Jump Foot Chip", self.player) or has_rod(state)

        def has_flame(state):
            if not state.has("Flame Body Chip", self.player):
                return False
            return (has_weapon_at(state, "Buster", "Full Charge")
                    or has_weapon_at(state, "Z-Saber", "Charged Slash")
                    or has_weapon_at(state, "Recoil Rod", "Charged Rod")
                    or has_weapon_at(state, "Shield Boomerang", "Charged Throw")
                    or (state.has("EX Skill: Split Heavens", self.player)
                        and has_weapon_at(state, "Z-Saber", "Owns")))

        # Access items.
        for stage_name in stage_names:
            set_rule(
                self.multiworld.get_entrance(f"To {stage_name}", self.player),
                lambda state, item=f"{stage_name} Access": state.has(item, self.player),
            )

        # Cerveau's shop.
        for slot in range(self.options.shop_slots.value):
            set_rule(
                self.multiworld.get_location(shop_location_names[slot], self.player),
                lambda state: state.has_any(stage_access_names, self.player),
            )

        # The base's later mission sets.
        set_rule(self.multiworld.get_entrance("To Resistance Base 2", self.player),
                 lambda state: state.has("Story Progress", self.player, STORY_MID))

        set_rule(self.multiworld.get_entrance("To Resistance Base 3", self.player),
                 lambda state: state.has("Story Progress", self.player, STORY_LATE))

        # The final stage. Needs every access item
        set_rule(
            self.multiworld.get_entrance("To Abandoned Research Laboratory", self.player),
            lambda state: state.has_all(stage_access_names, self.player),
        )

        # Location rules: Recoil Rod required
        for loc_name in [
            "Aegis Volcano Base (4) 114: Push 1st Container",
            "Oceanic Highway Ruins (1) 005: 1st Pit Breakable",
            "Weapons Repair Factory (2) 115: Hit 3rd Hammer",
            "Old Residential (1) 039: 1st Door",
            "Old Residential (3) 112: Floor Breakables",
            "Old Residential Energy (6): Breakable Blocks by Bombers",
            "Forest of Anatre (8) 040: Breakables Below Boss Room",
            "Giant Elevator (2) 041: 1st Passage High Ledges",
            "Giant Elevator (6) 027: 1st Descent Bottom Left Breakable",
            "Aegis Volcano Base E-Crystal (2): Push 1st Container",
            "Aegis Volcano Base E-Crystal (3): Push 1st Container",
            "Oceanic Highway Ruins E-Crystal (1): 1st Pit Breakable",
            "Oceanic Highway Ruins E-Crystal (2): 1st Pit Breakable",
            "Weapons Repair Factory E-Crystal (1): Hit 3rd Hammer",
            "Weapons Repair Factory E-Crystal (2): Hit 3rd Hammer",
            "Forest of Anatre Energy (3): Breakables Below Boss Room",
        ]:
            self.add_location_rule(loc_name, has_rod)

        # Location rules: Mobility required (Double Jump or Recoil Rod)
        for loc_name in [
            "Aegis Volcano Base (3) 026: Platform Above First Room",
            "Aegis Volcano Base (5) 073: Platform After Pushed Container",
            "Old Residential Subtank: Top Left Past Bombers",
            "Forest of Anatre (7) 076: Above 9th Button",
            "Giant Elevator 1-UP: 1st Passage High Ledges",
            "Aegis Volcano Base Energy: Platform Above First Room",
            "Old Residential E-Crystal (13): Top Left Past Bombers",
        ]:
            self.add_location_rule(loc_name, has_mobility)

        # Location rules: Flame Body Chip required
        for loc_name in [
            "Old Residential (4) 074: Left Fork Door",
            "Forest of Anatre (1) 063: Treetops Above Start",
            "Forest of Anatre (2) 002: Ledge Above 1st Door",
            "Old Residential 1-UP (1): Right of Fork",
            "Old Residential 1-UP (2): Left Fork Door",
            "Forest of Anatre 1-UP: In Tree Near Start",
            "Old Residential E-Crystal (1): Stump Door",
            "Old Residential Energy (1): Stump Door",
            "Old Residential E-Crystal (4): Door after Cutscene",
            "Old Residential E-Crystal (5): Door after Cutscene",
            "Old Residential E-Crystal (6): Door after Cutscene",
            "Forest of Anatre Energy (1): Treetops Above Generator Cannon",
        ]:
            self.add_location_rule(loc_name, has_flame)

        # Flame Body Chip + Recoil Rod
        self.add_location_rule("Old Residential (2) 001: Stump Door",
                               lambda state: has_flame(state) and has_rod(state))

        # Mobility OR Splash Jump Foot Chip
        for loc_name in [
            "Frontline Ice Base (1) 066: Top Route Tower",
            "Frontline Ice Base Energy: Top Route Tower",
        ]:
            self.add_location_rule(
                loc_name,
                lambda state: state.has("Disk 005: Splash Jump Foot Chip", self.player) or has_mobility(state))

        # Technically reachable without
        self.add_location_rule("Missile Factory Energy (2): Missile Top Right",
                               lambda state: state.has("Double Jump Foot Chip", self.player))

        # Double Mobility: Double Jump Foot Chip + Recoil Rod
        self.add_location_rule("Giant Elevator (1) 045: 1st Passage High Ledges",
                               lambda state: state.has("Double Jump Foot Chip", self.player) and has_rod(state))

        # Collectable 1-UP spawns in the new room
        self.add_location_rule("Resistance Base 1-UP: In Locked Room by Andrew",
                               lambda state: state.has("Disk 120: New Room Near Andrew", self.player))

        # Completion condition
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        
    def generate_output(self, output_directory: str) -> None:
        patch = MMZero3ProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "basepatch.bsdiff4"))
        write_tokens(self, patch)
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

        #from Utils import visualize_regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
