from BaseClasses import ItemClassification
from .Locations import *
from .Options import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

region_unlocks = [
	"Region Unlock: Dry Reef",
	"Region Unlock: Indigo Quarry",
	"Region Unlock: Moss Blanket",
	"Region Unlock: Glass Desert",
	"Region Unlock: Ancient Ruins",
	"Region Unlock: Ancient Ruins Transition",
	"Region Unlock: The Wilds",
	"Region Unlock: Ogden's Retreat",
	"Region Unlock: Nimble Valley",
	"Region Unlock: Mochi's Manor",
	"Region Unlock: The Slimeulations",
	"Region Unlock: Viktor's Workshop",
	"Region Unlock: The Grotto",
	"Region Unlock: The Overgrowth",
	"Region Unlock: The Lab",
	"Region Unlock: The Docks"
]

non_progressive_useful_items = {
	"Air Burst": 1,
	"Liquid Slot": 1,
	"Golden Sure Shot": 1,
	"Drone": 4,
	"Advanced Drone": 4,
	"Market Link": 3
}

progressive_useful_item_count = {
	"Progressive Max Health": 4,
	"Progressive Max Ammo": 4,
	"Progressive Run Efficiency": 2,
	"Progressive Market Stonks": 5
}

progressive_progression_item_count = {
	"Progressive Max Energy": 3,
	"Progressive Jetpack": 2,
	"Progressive Treasure Cracker": 3
}

filler_items = [
	"75x Newbucks",
	"81x Newbucks",
	"99x Newbucks",
	"100x Newbucks"
]

credits_unlocks = [
	"Region Unlock: Dry Reef",
	"Region Unlock: Indigo Quarry",
	"Region Unlock: Moss Blanket",
	"Region Unlock: Glass Desert",
	"Region Unlock: Ancient Ruins",
	"Region Unlock: Ancient Ruins Transition"
]

item_table = {
	**{item: ItemClassification.progression for item in region_unlocks},
	**{item: ItemClassification.useful for item in non_progressive_useful_items},
	**{item: ItemClassification.useful for item in progressive_useful_item_count},
	**{item: ItemClassification.progression for item in progressive_progression_item_count},
	**{item: ItemClassification.filler for item in filler_items},
	"Trap Slime": ItemClassification.trap,
	"Casey's Letter": ItemClassification.progression_skip_balancing
}

raw_items = [item for item, classification in item_table.items()]

def gen_create_items(world):
	pool = world.multiworld.itempool
	options = world.options
	for zone in region_unlocks:
	    if "Reef" in zone and options.start_with_dry_reef: continue
	    if "Wilds" in zone and not options.include_ogden: continue
	    if "Retreat" in zone and not options.include_ogden: continue
	    if "Nimble" in zone and not options.include_mochi: continue
	    if "Manor" in zone and not options.include_mochi: continue
	    if "Slimeulations" in zone and not options.include_viktor: continue
	    if "Workshop" in zone and not options.include_viktor: continue
	    world.location_count -= 1
	    pool.append(world.create_item(zone))
	
	for item, amt in non_progressive_useful_items.items():
		world.location_count -= amt
		for _ in range(amt):
			pool.append(world.create_item(item))
	
	for item, amt in progressive_useful_item_count.items():
		world.location_count -= amt
		for _ in range(amt):
			pool.append(world.create_item(item))
	
	for item, amt in progressive_progression_item_count.items():
		world.location_count -= amt
		for _ in range(amt):
			pool.append(world.create_item(item))
	
	if options.goal_type == 3:
		for _ in range(options.mail_count):
			world.location_count -= 1
			pool.append(world.create_item("Casey's Letter"))
	
	for _ in range(int(world.location_count * (options.trap_percent / 100))):
		world.location_count -= 1
		pool.append(world.create_item("Trap Slime"))
	for _ in range(world.location_count):
		pool.append(world.create_item(world.random.choice(filler_items)))