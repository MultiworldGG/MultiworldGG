import os
from typing import Dict, Set
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from BaseClasses import Region, MultiWorld, Item, Location, LocationProgressType, ItemClassification
from worlds.AutoWorld import World, WebWorld
from Utils import visualize_regions
import yaml
import logging
import base64

from .Options import PathOfExileOptions
from . import Items
from . import Locations
from . import Regions as poeRegions
from . import Rules as poeRules
from . import Options
from . import Logic
from .Version import POE_VERSION

logger = logging.getLogger("poe")
logger.setLevel(logging.INFO)

# ----- Configure the POE client ----- #


def launch_client():
    from . import Client
    launch_subprocess(Client.launch, name="poeClient", )

components.append(Component("Path of Exile Client",
                            func=launch_client,
                            component_type=Type.CLIENT,
                            icon="poe"))

icon_paths["poe"] = f"ap:{__name__}/icons/poeicon.png"

# ----- PathOfExile Web World ----- #
from BaseClasses import Tutorial
class PathOfExileWebWorld(WebWorld):
    """
    Web interface for the Path of Exile world.
    This class can be extended to include specific web functionalities.
    """
    theme = "stone"
    bug_report_page = "https://github.com/stubobis1/Archipelago/issues" # if anyone else wants to help maintain this, please do so
    setup_en = Tutorial(
        tutorial_name="Path of Exile Setup Guide",
        description="A guide to setting up MultiworldGG Path of Exile.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["StuBob"]
    )
    tutorials = [setup_en]

    option_groups = Options.poe_options_groups
    options_presets = Options.poe_presets

# ----- PathOfExile World ----- #


class PathOfExileWorld(World):
    """
    Path of Exile is a free-to-play online action RPG set in a dark, gritty world where you explore, fight monsters,
    and collect powerful loot. The game is known for its deep character customization, with an enormous passive skill
    tree, thousands of items, and a huge endgame full of challenging bosses, and a wide variety of skill gems that define abilities.
    """
    _debug = False
    game = "Path of Exile"
    author: str = "StuBob"
    web = PathOfExileWebWorld()
    options_dataclass = PathOfExileOptions
    origin_region_name = "Menu"

    MAX_GUCCI_GEAR_UPGRADES = 19 # fishing rods don't count.
    MAX_GEAR_UPGRADES       = 50
    MAX_FLASK_SLOTS         = 10
    MAX_LINK_UPGRADES       = 22
    MAX_SKILL_GEMS          = 50 # you will get more, but this is the max required for "logic"
    MAX_SUPPORT_GEMS        = 50 # you will get more, but this is the max required for "logic"

# Instance variables, but made in __init__ so they are per-instance
#    items_to_place = {}
#    items_procollected = {}
#    locations_to_place = {}
#    total_items_to_place_count = 0
#
#    goal_act = 0

    location_name_to_id = ({ loc["name"]: id for id, loc in Locations.full_locations.items() } 
                        | { loc["name"]: loc["id"] for loc in Locations.bosses.values() })

    item_name_to_id = ({ item["name"]: item["id"] for item in Items.item_table.values() }
                       | { item["name"]: item["id"] for item in Locations.bosses.values() })



    item_name_groups: Dict[str, Set[str]] = Items.get_item_name_groups()

    def __init__(self, *args, **kwargs):

        self.items_to_place = {}
        self.items_procollected = {}
        self.locations_to_place = {}
        self.total_items_to_place_count = 0
        self.goal_act = 0
        self.bosses_for_goal: list[str] = []

        self.placed_total_gear_upgrades = 0
        self.placed_total_flask_slots   = 0
        self.placed_total_link_upgrades = 0
        self.placed_total_skill_gems    = 0
        self.placed_total_support_gems  = 0

        super().__init__(*args, **kwargs)

        # ``Items.item_table`` is a module level dictionary whose values are
        # mutable ``dict`` objects.  The original implementation only created a
        # shallow copy of this mapping which meant that any modification to the
        # nested dictionaries (for example changing an item's classification
        # from progression to filler) would also mutate the global item table.
        #
        # By performing a deep copy we ensure every world gets its own private
        # copy of the item table and mutations no longer leak between runs.
        # self.items_to_place = Items.item_table.copy()
        import copy
        self.items_to_place = copy.deepcopy(Items.item_table)


    def remove_and_create_items_by_itemdict(self, item: Items.ItemDict) -> list[Items.PathOfExileItem]:
        item_id = item["id"]
        item_to_place = self.items_to_place.pop(item_id)  # Remove from items to place
        item_objs = []
        count = item.get("count", 1)
        for i in range(count):
            item_obj = Items.PathOfExileItem(item_to_place["name"], item.get("classification", ItemClassification.filler), item_id, self.player)
            item_objs.append(item_obj)
        return item_objs

    # This is only used for plando and start inventory, where we want to create an item by name,
    # but also remove it from the items to place, so it doesn't get placed again later.
    # This will remove a single instance of the item.
    def remove_and_create_item_by_name(self, item_name: str) -> Item:
        item_id = self.item_name_to_id[item_name]
        item_to_place = self.items_to_place[item_id]
        item_count = item_to_place.get("count", 1)
        if item_count <= 1:
            self.items_to_place.pop(item_id)  # Remove from items to place when last copy is taken
        else:
            item_to_place["count"] = item_count - 1
        item_obj = Items.PathOfExileItem(item_to_place["name"], ItemClassification.progression, item_id, self.player)
        return item_obj

    def precollect(self, item_obj):
        self.items_procollected[item_obj.code] = item_obj
        self.multiworld.push_precollected(item_obj)
    
    def generate_early(self):
        Logic.generate_items_logic(self)

    def create_regions(self):
        """Create the regions for the Path of Exile world.
        This method initializes the regions based on the acts defined in Regions.py.
        """
        options: PathOfExileOptions = self.options
        acts_to_play = [act for act in poeRegions.acts if act["act"] <= self.goal_act]
        poeRegions.create_and_populate_regions(world = self,
                                               multiworld=self.multiworld,
                                               player= self.player,
                                               locations=self.locations_to_place,
                                               act_regions=acts_to_play)
        #poeRegions.create_and_populate_regions(self, self.multiworld, self.player, locations_to_place, poeRegions.acts)

        self.multiworld.completion_condition[self.player] = lambda state: (poeRules.completion_condition(self, state))


        logger.debug(f"[poe.CreateRegion]: total items to place: {self.total_items_to_place_count}")
        logger.debug(f"[poe.CreateRegion]: total locs in world.: {len(self.locations_to_place)}")

    def create_item(self, item_name: str) -> Items.PathOfExileItem:
        # this is called when AP wants to create an item by name (for plando, start inventory, item links) or when you call it from your own code

        # get the item from the item table, by name
        id = self.item_name_to_id.get(item_name)
        item = Items.item_table.get(id)
        if item is None:
            if "defeat" in item_name:
                #its a boss
                item = Locations.bosses.get(item_name.replace("defeat ", ""))
            else:
                raise Exception(f"I don't know how to create the item {item}")
        classification = item.get("classification", ItemClassification.progression)  # progression I guess?
        return Items.PathOfExileItem(item['name'], classification, item['id'], self.player)

    def create_items(self):
        #itempool = self.multiworld.itempool
        #logger.debug(f"[DEBUG]: in create_items {len(itempool)} ---- ")options: PathOfExileOptions = self.options
        # iterate over a copy to be safe while modifying the dictionary
        for item in list(self.items_to_place.values()):
            list_of_items = self.remove_and_create_items_by_itemdict(item)
            for item in list_of_items:
                self.multiworld.itempool.append(item)
        logger.debug(f"[POE]: items left to place:{len(self.items_to_place)} /{self.total_items_to_place_count}.\nCreated {len(self.locations_to_place)} locations.")



    def fill_slot_data(self):
        options: PathOfExileOptions = self.options
        game_options = {
            "gucciHobo": options.gucci_hobo_mode.value,
            "passivePointsAsItems": options.add_passive_skill_points_to_item_pool.value,
            "LevelingUpAsLocations": options.add_leveling_up_to_location_pool.value,
            "ProgressiveGear": options.progressive_gear.value,
            "goal": options.goal.value,
            "starting_character": Options.option_starting_character_to_class_name(options.starting_character.value),
            "bosses_for_goal": self.bosses_for_goal,
            "deathlink": options.death_link.value,
        }
        client_options = {
            "lootFilterSounds": options.loot_filter_sounds.value,
            "lootFilterDisplay": options.loot_filter_display.value,
            "ttsSpeed" : options.tts_speed.value,
            "ttsEnabled": options.enable_tts.value,
        }
        return {
            "game_options": game_options,
            "client_options": client_options,
            "poe-uuid": base64.urlsafe_b64encode(self.random.randbytes(8)).strip(b'=').decode('utf-8'), # used for generation id
            "generated_version": POE_VERSION,
        }

        
    def generate_output(self, output_directory: str):
        if self._debug:
            logger.debug(f"Generating output for {self.game} in {output_directory}")
            from BaseClasses import CollectionState
            local_state = CollectionState(self.multiworld)  # collects all precollected items already
            for item in self.multiworld.itempool:
                if item.player == self.player:
                    local_state.collect(item, prevent_sweep=True)
            local_state.sweep_for_advancements(locations=self.multiworld.get_locations(self.player))
            visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), f"PathOfExile-Player{self.player}.puml",
                            show_entrance_names=True,
                            regions_to_highlight=local_state.reachable_regions[self.player])