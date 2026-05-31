from BaseClasses import ItemClassification
from .Locations import *
from .Options import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

dlc_items = [
	"Ducks Please Ducks",
	"Duck Addiction Ducks",
	"So Many Ducks Ducks",
	"Ducks Galore Ducks",
	"Ducklings Ducks"
]

item_table = {
	"Progressive Column Unlock": ItemClassification.progression,
	"Progressive Spawn Speed Upgrade": ItemClassification.useful,
	"Random Duck": ItemClassification.filler,
	**{item: ItemClassification.progression for item in dlc_items}
}

raw_items = [item for item, classification in item_table.items()]

def gen_create_items(world):
	pool = world.multiworld.itempool
	options = world.options
	for _ in range(9):
		world.location_count -= 1
		pool.append(world.create_item("Progressive Column Unlock"))
	for _ in range(9):
		world.location_count -= 1
		pool.append(world.create_item("Progressive Spawn Speed Upgrade"))
	if options.ducks_please:
		world.location_count -= 1
		pool.append(world.create_item("Ducks Please Ducks"))
	if options.duck_addiction:
		world.location_count -= 1
		pool.append(world.create_item("Duck Addiction Ducks"))
	if options.so_many_ducks:
		world.location_count -= 1
		pool.append(world.create_item("So Many Ducks Ducks"))
	if options.ducks_galore:
		world.location_count -= 1
		pool.append(world.create_item("Ducks Galore Ducks"))
	if options.ducklings:
		world.location_count -= 1
		pool.append(world.create_item("Ducklings Ducks"))
	for _ in range(world.location_count):
		pool.append(world.create_item("Random Duck"))