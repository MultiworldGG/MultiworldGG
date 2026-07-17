import logging
import os
import yaml

from typing import ClassVar, Any, Optional, Type, TextIO
from Options import Option
from BaseClasses import Item, Location, LocationProgressType
from Options import Accessibility, OptionError
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union
from .data.Items import *
from .Options import *
from .WebWorld import OracleOfAgesWeb
from .generation.PatchWriter import ooa_create_appp_patch
from .data.Constants import *
from .data.Locations import LOCATIONS_DATA
from .data.Items import ITEMS_DATA
from .data.Entrances import *
from .data.Regions import *
from .common.Util import build_location_name_to_id_dict, build_item_name_to_id_dict
from .Client import OracleOfAgesClient  # Unused, but required to register with BizHawkClient
from .Settings import OOASettings
from .WebWorld import *

class OracleOfAgesWorld(World):
    """
    The Legend of Zelda: Oracles of Ages is one of the rare Capcom entries to the series.
    Nayru, the oracle of ages, has been possessed by Veran, and she is now making a mess in Labrynna
    Gather the Essences of Times, exorcice Nayru and defeat Veran to save the timeline of Labrynna
    """
    game = "The Legend of Zelda - Oracle of Ages"
    options_dataclass = OracleOfAgesOptions
    options: OracleOfAgesOptions
    required_client_version = (0, 5, 1)
    web = OracleOfAgesWeb()
    topology_present = True

    location_name_to_id = build_location_name_to_id_dict(LOCATIONS_DATA)
    item_name_to_id = build_item_name_to_id_dict(ITEMS_DATA)
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    pre_fill_items: List[Item]
    pre_fill_seeds: Dict[str, Item]
    dungeon_items: List[Item]
    randomized_entrances: Dict[str, str] = {}
    shop_prices: Dict[str, int]

    settings: ClassVar[OOASettings]
    settings_key = "tloz_ooa_options"

    remaining_progressive_gasha_seeds = 0

    ages = True
    seasons = False
    romhack = False

    tracker_world: ClassVar = {
        "external_pack_key": "ut_pack_path",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": [
            "locations/dungeons.json",
            "locations/overworld_past.json",
            "locations/overworld_present.json",
        ],
        "poptracker_name_mapping": dict[str, int]
    }


    @classmethod
    def version(cls) -> str:
        return cls.world_version.as_simple_string()

    def __init__(self, multiworld, player):
        self.tracker_world["poptracker_name_mapping"] = {}
        for location_name, location_data in LOCATIONS_DATA.items():
            split = location_name.split(": ")
            poptrackerName = split[-1] + "/"
            self.tracker_world["poptracker_name_mapping"][poptrackerName] = self.location_name_to_id[location_name]
            #print(f"{poptrackerName} ({location_name}) => {self.location_name_to_id[location_name]}")

        super().__init__(multiworld, player)

        self.pre_fill_items = []
        self.dungeon_items = []
        self.pre_fill_seeds = {}
        self.shop_prices = SHOP_PRICES_DIVIDERS.copy()
   
   
    # -------------------------------------------------------------------------------------   
    # REMINDER OF AP WORLD GENERATION PROCESS. This function are called in order: 
    # -------------------------------------------------------------------------------------   
    #stage_assert_generate(cls, multiworld: MultiWorld) 
    #   a class method called at the start of generation to check for the existence of prerequisite files, usually a ROM for games which require one.
    #generate_early(self) 
    #   called per player before any items or locations are created. You can set properties on your world here. Already has access to player options and RNG. This is the earliest step where the world should start setting up for the current multiworld, as the multiworld itself is still setting up before this point. You cannot modify local_items, or non_local_items after this step.
    #create_regions(self) 
    #   called to place player's regions and their locations into the MultiWorld's regions list. If it's hard to separate, this can be done during generate_early or create_items as well.
    #create_items(self) 
    #   called to place player's items into the MultiWorld's itempool. By the end of this step all regions, locations and items have to be in the MultiWorld's regions and itempool. You cannot add or remove items, locations, or regions after this step. Locations cannot be moved to different regions after this step. This includes event items and locations.
    #set_rules(self) 
    #   called to set access and item rules on locations and entrances.
    #connect_entrances(self) 
    #   by the end of this step, all entrances must exist and be connected to their source and target regions. Entrance randomization should be done here.
    #generate_basic(self) 
    #   player-specific randomization that does not affect logic can be done here.
    #pre_fill(self), fill_hook(self) and post_fill(self) 
    #   called to modify item placement before, during, and after the regular fill process; all finishing before generate_output. Any items that need to be placed during pre_fill should not exist in the itempool, and if there are any items that need to be filled this way, but need to be in state while you fill other items, they can be returned from get_pre_fill_items.
    #generate_output(self, output_directory: str) 
    #   creates the output files if there is output to be generated. When this is called, self.multiworld.get_locations(self.player) has all locations for the player, with attribute item pointing to the item. location.item.player can be used to see if it's a local item.
    #fill_slot_data(self) and modify_multidata(self, multidata: MultiData)
    #    can be used to modify the data that will be used by the server to host the MultiWorld.
    
        
    # ===================================================================================
    #
    # ===================================================================================
    def generate_early(self):
        from .generation.GenerateEarly import ooa_generate_early
        ooa_generate_early(self)
        
    # ===================================================================================
    #
    # ===================================================================================
    def create_regions(self):
        from .generation.CreationRegions import ooa_create_region
        ooa_create_region(self)

    # ===================================================================================
    #
    # ===================================================================================
    def create_items(self):
        from .generation.CreateItems import ooa_create_items
        ooa_create_items(self)

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def create_item(self, item: str) -> Item :
        from .common.generation.CreateItems import create_item
        return create_item(self, item)

    # ===================================================================================
    #
    # ===================================================================================
    def set_rules(self):
        from .generation.Logic import create_connections, apply_self_locking_rules
        create_connections(self)
        apply_self_locking_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)
        
        #multiworld = self.multiworld
        #allstate = multiworld.get_all_state(False)
        #locations = multiworld.get_locations()
        #reachable = multiworld.get_reachable_locations(allstate)
        #unreachable = [location for location in locations if location not in reachable]
        #print(unreachable)
        #print(allstate.prog_items)

        

    # ===================================================================================
    #
    # ===================================================================================
    def get_filler_item_name(self) -> str:
        from .generation.CreateItems import ooa_get_filler_item_name
        return ooa_get_filler_item_name(self)

    # ===================================================================================
    #
    # ===================================================================================
    def pre_fill(self) -> None:
        from .generation.PreFill import pre_fill
        pre_fill(self)

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def get_pre_fill_items(self):
        return self.pre_fill_items
    
    # ===================================================================================
    #
    # ===================================================================================
    def generate_output(self, output_directory: str):
        patch = ooa_create_appp_patch(self)
        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")
        patch.write(rom_path)
        return

    # -----------------------------------------------------------------------------------
    #
    # -----------------------------------------------------------------------------------
    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"Apworld version : {self.version()}\n")
        if self.options.shuffle_dungeons != "vanilla":
            spoiler_handle.write(f"Shuffled Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.randomized_entrances.items():
                spoiler_handle.write(f"\t- outside {entrance} --> inside {dungeon}\n")


    # ===================================================================================
    #
    # ===================================================================================
    def fill_slot_data(self) -> dict:
        # Put options that are useful to the tracker inside slot data
        #print(self.randomized_entrances)
        slot_data = {
            "version": f"{self.version()}",
            "options": self.options.as_dict(
                *[option_name for option_name in OracleOfAgesOptions.type_hints
                  if hasattr(OracleOfAgesOptions.type_hints[option_name], "include_in_slot_data")]),
            "randomized_entrances": self.randomized_entrances,
            "shop_costs": self.shop_prices,
        }

        return slot_data
    

    
    # ===================================================================================
    #
    # =================================================================================== 
    def interpret_slot_data(self, slot_data: Optional[dict[str, Any]]) -> Any:
        if slot_data is not None:
            return slot_data

        if not hasattr(self.multiworld, "re_gen_passthrough") or self.game not in self.multiworld.re_gen_passthrough:
            return False

        slot_data = self.multiworld.re_gen_passthrough[self.game]

        for option in [option_name for option_name in OracleOfAgesOptions.type_hints
                        if hasattr(OracleOfAgesOptions.type_hints[option_name], "include_in_slot_data")]:
            option_class: Type[Option] = OracleOfAgesOptions.type_hints[option]
            self.options.__setattr__(option, option_class.from_any(slot_data["options"][option]))

        self.randomized_entrances = slot_data["randomized_entrances"]
        #print(self.randomized_entrances)
        self.shop_prices = slot_data["shop_costs"]

        return True
    
    # ===================================================================================
    #
    # =================================================================================== 
    def determine_warp_to_start_variables(self):
        # Mashy wasn't sure if he liked the new warp to start location on his first video on playing my 1.0.0 beta hotfix. 
        # Adding this to not force the new warp to start location on anyone that is still used to the old one.
        if self.options.warp_to_start_location == OracleOfAgesWarpToStartLocation.option_near_timeportal:
            return {
                "room": 0x39,
                "pos": 0x21
            }
        else:
            return {
                # The syntax is like this:
                # "room" represents a byte number for the screen that link will go to when warp to start is activated.
                # "pos" represents a byte number for a position link will be in when warp to start is active.
                # "group" represents a byte number for a screen group that link will be in once warp to start is activated.
                # "dest_transittion" is a number that will changes the screen after the warp
                # "src_transittion" is a number that will changes the screen before the warp
            }
