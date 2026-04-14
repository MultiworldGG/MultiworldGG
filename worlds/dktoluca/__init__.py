import os
import math
import settings
import threading
import pkgutil

from BaseClasses import MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from rule_builder.rules import Rule

from .items import DKC3Item, item_table, misc_table, item_groups
from .locations import setup_locations, all_locations, location_groups
from .regions import create_regions, connect_regions
from .enums import Items, Locations, Regions
from .options import DKC3Options, Logic, StartingKong, dkc3_option_groups
from .levels import generate_level_list, level_map
from .rules import DKC3StrictRules, DKC3LooseRules, DKC3ExpertRules
from .rom import patch_rom, DKC3ProcedurePatch, HASH_US
from .client import DKC3SNIClient
from .constants import *
from . import tracker

from typing import Dict, Set, List, ClassVar

class DKC3Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Donkey Kong Country 3 US v1.0 ROM"""
        description = "Donkey Kong Country 3 (USA) ROM File"
        copy_to = "Donkey Kong Country 3 - Dixie Kong's Double Trouble! (USA).sfc"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class DKC3Web(WebWorld):
    theme = "grass"
    display_name = "Donkey Kong Country 3 (Toluca)"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Donkey Kong Country 3 with MultiworldGG",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )

    tutorials = [setup_en]

    option_groups = dkc3_option_groups


class DKC3World(tracker.UTMxin, World):
    """
    Donkey Kong Country 3 is an action platforming game for the SNES. K. Rool is BACK once again, retrieve Banana Birds to open up Kaos Kore or find Knautilus in order to rescue Donkey and Diddy!
    """
    game = GAME_NAME
    web = DKC3Web()

    settings: ClassVar[DKC3Settings]
    
    options_dataclass = DKC3Options
    options: DKC3Options
    
    required_client_version = (0, 6, 7)
    
    using_ut: bool
    ut_can_gen_without_yaml = True
    glitches_item_name = Items.glitched

    item_name_to_id = {name.value: data.code for name, data in item_table.items()}
    location_name_to_id = {name.value: code for name, code in all_locations.items()}
    item_name_groups = item_groups
    location_name_groups = location_groups
    origin_region_name = Regions.northern_kremisphere_south
    rule_macros: dict[str, Rule.Resolved]
    hint_blacklist = frozenset({
        Locations.defeated_belcha.value,
        Locations.defeated_arich.value,
        Locations.defeated_squirt.value,
        Locations.defeated_kaos.value,
        Locations.defeated_bleak.value,
        Locations.defeated_barbos.value,
    })

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.rule_macros = {}
        super().__init__(multiworld, player)


    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self, location_table)
        
        connect_regions(self)
       

    def set_rules(self):
        logic = self.options.logic
        if logic == Logic.option_loose:
            DKC3LooseRules(self).set_dkc3_rules()
        elif logic == Logic.option_strict:
            DKC3StrictRules(self).set_dkc3_rules()
        elif logic == Logic.option_expert:
            DKC3ExpertRules(self).set_dkc3_rules()
        else:
            raise ValueError(f"Somehow you have a logic option that's currently invalid."
                             f" {logic} for {self.multiworld.get_player_name(self.player)}")
        
        # Universal Tracker: If we're using UT, scan the rules again to build "glitched logic" during the regen
        if self.is_ut:
            if logic == Logic.option_strict:
                DKC3LooseRules(self).set_dkc3_glitched_rules(DKC3StrictRules(self).location_rules)
            elif logic == Logic.option_loose:
                DKC3ExpertRules(self).set_dkc3_glitched_rules(DKC3LooseRules(self).location_rules)
                
        return
        from Utils import visualize_regions
        from BaseClasses import CollectionState
        state = CollectionState(self.multiworld, allow_partial_entrances=True)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region(self.origin_region_name), "my_world.puml", show_entrance_names=True,
                        regions_to_highlight=state.reachable_regions[self.player])
    
 
    def create_items(self) -> None:
        itempool: List[DKC3Item] = []

        self.total_required_locations = len(setup_locations(self)) - 6

        # Set starting kong
        if self.options.starting_kong == StartingKong.option_dixie:
            self.multiworld.push_precollected(self.create_item(Items.dixie))
            itempool += [self.create_item(Items.kiddy)]
        elif self.options.starting_kong == StartingKong.option_kiddy:
            self.multiworld.push_precollected(self.create_item(Items.kiddy))
            itempool += [self.create_item(Items.dixie)]
        elif self.options.starting_kong == StartingKong.option_both:
            self.multiworld.push_precollected(self.create_item(Items.dixie))
            self.multiworld.push_precollected(self.create_item(Items.kiddy))

        self.multiworld.push_precollected(self.create_item(Items.lake_orangatanga))
        for world_ in sorted(item_groups["Worlds"]):
            if world_ in self.multiworld.precollected_items[self.player]:
                continue
            else:
                itempool.append(self.create_item(world_))

        # Kaos Kore is special
        if not self.options.required_birds.value:
            itempool.append(self.create_item(Items.kaos_kore))
                
        shuffle_abilities = sorted(self.options.shuffle_abilities.value)
        for item in sorted(item_groups["Abilities"]):
            if item in self.multiworld.precollected_items[self.player]:
                continue
            elif item in shuffle_abilities:
                itempool += [self.create_item(item)]
            else:
                self.multiworld.push_precollected(self.create_item(item))

        shuffle_animals = sorted(self.options.shuffle_animals.value)
        for item in sorted(item_groups["Animals"]):
            if item in shuffle_animals:
                itempool += [self.create_item(item)]
            else:
                self.multiworld.push_precollected(self.create_item(item))
                
        shuffle_objects = sorted(self.options.shuffle_objects.value)
        for item in sorted(item_groups["Barrels"]):
            if item in shuffle_objects:
                itempool += [self.create_item(item)]
            else:
                self.multiworld.push_precollected(self.create_item(item))

        itempool += [self.create_item(Items.vehicle) for _ in range(3)]
        itempool += [self.create_item(Items.bonus_coin) for _ in range(5)]
        itempool += [self.create_item(Items.cog) for _ in range(5)]

        if self.options.energy_link:
            itempool += [self.create_item(Items.extractinator) for _ in range(3)]

        itempool += [self.create_item(Items.radar)]

        # Add junk items into the pool
        junk_count = self.total_required_locations - len(itempool)
        junk_weights = []
        junk_weights += ([Items.dk_barrel] * 60)
        junk_weights += ([Items.bear_coin] * 10)
        junk_weights += ([Items.balloon] * 30)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        boss_locations = [
            Locations.defeated_belcha,
            Locations.defeated_arich,
            Locations.defeated_squirt,
            Locations.defeated_kaos,
            Locations.defeated_bleak,
            Locations.defeated_barbos,
            #Locations.defeated_krool_castle,
            #Locations.defeated_krool_knautilus,
        ]
        for location in boss_locations:
            self.multiworld.get_location(str(location), self.player).place_locked_item(self.create_item(Items.banana_bird))

        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification=False) -> DKC3Item:
        data = item_table[str(name)]

        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        
        created_item = DKC3Item(str(name), classification, data.code, self.player)

        return created_item


    def interpret_slot_data(self, slot_data):
        return slot_data
    
    
    def fill_slot_data(self):
        slot_data = {}
        slot_data["level_connections"] = self.level_connections
        slot_data["boss_connections"] = self.boss_connections
        slot_data["logic"] = self.options.logic.value
        slot_data["goal"] = self.options.goal.value
        slot_data["starting_kong"] = self.options.starting_kong.value
        slot_data["kong_checks"] = self.options.kong_checks.value
        slot_data["dk_coin_checks"] = self.options.dk_coin_checks.value
        slot_data["balloon_checks"] = self.options.balloon_checks.value
        slot_data["banana_checks"] = self.options.banana_checks.value
        slot_data["coin_checks"] = self.options.coin_checks.value
        slot_data["bird_checks"] = self.options.bird_checks.value
        slot_data["required_birds"] = self.options.required_birds.value
        slot_data["required_lake_levels"] = self.options.required_lake_levels.value
        slot_data["required_forest_levels"] = self.options.required_forest_levels.value
        slot_data["required_cove_levels"] = self.options.required_cove_levels.value
        slot_data["required_mekanos_levels"] = self.options.required_mekanos_levels.value
        slot_data["required_k3_levels"] = self.options.required_k3_levels.value
        slot_data["required_ridge_levels"] = self.options.required_ridge_levels.value
        slot_data["required_kore_levels"] = self.options.required_kore_levels.value
        slot_data["required_krematoa_levels"] = self.options.required_krematoa_levels.value
        slot_data["energy_link"] = self.options.energy_link.value

        return slot_data


    def generate_early(self):
        # Skip shuffling levels
        #if self.options.shuffle_levels:
        #    self.options.shuffle_levels.value = False
        # Place cogs anywhere for now
        if self.options.cog_placement:
            self.options.cog_placement.value = 0


        # Shuffle levels
        self.level_connections: Dict[str, str] = dict()
        self.boss_connections: Dict[str, str] = dict()
        self.rom_connections: Dict[str, str] = dict()
        self.lost_world_levels: Set[str] = set()
        generate_level_list(self)

        super().generate_early()


    def get_filler_item_name(self) -> str:
        return self.random.choice(list(misc_table.keys()))
    

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        er_hint_data = {}
        for level_spot, map_name in level_map.items():
            if level_spot not in self.level_connections.keys():
                continue
            level_name = self.level_connections[level_spot.value]
            level_region = self.get_region(level_name)
            for location in level_region.locations:
                if location.address is None:
                    continue
                er_hint_data[location.address] = map_name.value
                
        hint_data[self.player] = er_hint_data


    def generate_output(self, output_directory: str):
        try:
            patch = DKC3ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("dkc3_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/dkc3_basepatch.bsdiff4"))
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
