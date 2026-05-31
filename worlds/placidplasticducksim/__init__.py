from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial
from .Locations import *
from .Rules import *
from .Options import *
from .Items import *
from .Regions import *
from .Settings import *
from typing import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]
class PPDSWebWorld(WebWorld):
    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Placid Plastic Duck Simulator in MultiworldGG.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["SW_CreeperKing"]
    )

    tutorials = [setup_en]

class PlacidPlasticDuckSimulator(World):
	"""
	A game about funny ducks in a pool
	"""
	game = "Placid Plastic Duck Simulator"
	web = PPDSWebWorld()
	options_dataclass = PlacidPlasticDuckSimulatorOptions
	options: PlacidPlasticDuckSimulatorOptions
	settings: ClassVar[PlacidPlasticDuckSimulatorSettings]
	topology_present = True
	ut_can_gen_without_yaml = True
	gen_puml = False
	location_name_to_id = {value: location_dict.index(value) + 1 for value in location_dict}
	item_name_to_id = {value: raw_items.index(value) + 1 for value in raw_items}
	item_name_groups = {
		"column": ["Progressive Column Unlock"]
	}

	def __init__(self, multiworld: "MultiWorld", player: int):
		super().__init__(multiworld, player)
		self.location_count = 0

	def generate_early(self):
		options = self.options
		if hasattr(self.multiworld, "re_gen_passthrough"):
			if "Placid Plastic Duck Simulator" not in self.multiworld.re_gen_passthrough: return
			passthrough = self.multiworld.re_gen_passthrough["Placid Plastic Duck Simulator"]
			if "ducks_please" in passthrough:
				options.ducks_please = DucksPlease(passthrough["ducks_please"])
			
			if "duck_addiction" in passthrough:
				options.duck_addiction = DuckAddiction(passthrough["duck_addiction"])
			
			if "so_many_ducks" in passthrough:
				options.so_many_ducks = SoManyDucks(passthrough["so_many_ducks"])
			
			if "ducks_galore" in passthrough:
				options.ducks_galore = DucksGalore(passthrough["ducks_galore"])
			
			if "ducklings" in passthrough:
				options.ducklings = Ducklings(passthrough["ducklings"])
			
		check_options(self)

	def create_regions(self):
		gen_create_regions(self)

	def create_item(self, name: str):
		return Item(name, item_table[name], self.item_name_to_id[name], self.player)

	def create_items(self):
		gen_create_items(self)

	def set_rules(self):
		player = self.player
		options = self.options
		self.multiworld.completion_condition[self.player] = lambda state: has_column(state, player, options, 10)

	def fill_slot_data(self):
		slot_data = {
			"ducks_please": bool(self.options.ducks_please),
			"duck_addiction": bool(self.options.duck_addiction),
			"so_many_ducks": bool(self.options.so_many_ducks),
			"ducks_galore": bool(self.options.ducks_galore),
			"ducklings": bool(self.options.ducklings)
		}
		return slot_data

	def generate_output(self, output_directory: str):
		if self.gen_puml: 
		    from Utils import visualize_regions
		    state = self.multiworld.get_all_state(False)
		    state.update_reachable_regions(self.player)
		    visualize_regions(self.get_region("Menu"), f"{self.player_name}_world.puml",
		                      show_entrance_names=True,
		                      regions_to_highlight=state.reachable_regions[self.player])