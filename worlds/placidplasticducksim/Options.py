from dataclasses import dataclass
from Options import *
from .Locations import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class DucksPlease(Toggle):
	"""
	Enable ducks from the Ducks, Please DLC
	"""
	display_name = "Ducks Please"


class DuckAddiction(Toggle):
	"""
	Enable ducks from the Duck Addiction DLC
	"""
	display_name = "Duck Addiction"


class SoManyDucks(Toggle):
	"""
	Enable ducks from the So Many Ducks DLC
	"""
	display_name = "So Many Ducks"


class DucksGalore(Toggle):
	"""
	Enable the ducks from the Ducks Galore DLC
	"""
	display_name = "Ducks Galore"


class Ducklings(Toggle):
	"""
	Enable the ducks from the Ducklings DLC
	"""
	display_name = "Ducklings"


@dataclass
class PlacidPlasticDuckSimulatorOptions(PerGameCommonOptions):
	ducks_please: DucksPlease
	duck_addiction: DuckAddiction
	so_many_ducks: SoManyDucks
	ducks_galore: DucksGalore
	ducklings: Ducklings

	def get_options_map(self, option):
		match option:
			case "ducks_please":
				return self.ducks_please
			case "duck_addiction":
				return self.duck_addiction
			case "so_many_ducks":
				return self.so_many_ducks
			case "ducks_galore":
				return self.ducks_galore
			case "ducklings":
				return self.ducklings
		

def check_options(world):
	options = world.options
	random = world.random
	settings = world.settings

def raise_yaml_error(player_name, error):
	raise OptionError(f'\n\n=== Placid Plastic Duck Simulator YAML ERROR ===\nPlacid Plastic Duck Simulator: {player_name} {error}, PLEASE FIX YOUR YAML\n\n')