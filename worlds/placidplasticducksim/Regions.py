from BaseClasses import Location, Region, Item, ItemClassification, LocationProgressType
from .Locations import *
from .Rules import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

priority_map = []

def gen_create_regions(world):
	player = world.player
	options = world.options
	rule_map = get_rule_map(player, options)
	
	region_map = {
		"Menu": Region("Menu", world.player, world.multiworld),
		"Column 1": Region("Column 1", world.player, world.multiworld),
		"Column 2": Region("Column 2", world.player, world.multiworld),
		"Column 3": Region("Column 3", world.player, world.multiworld),
		"Column 4": Region("Column 4", world.player, world.multiworld),
		"Column 5": Region("Column 5", world.player, world.multiworld),
		"Column 6": Region("Column 6", world.player, world.multiworld),
		"Column 7": Region("Column 7", world.player, world.multiworld),
		"Column 8": Region("Column 8", world.player, world.multiworld),
		"Column 9": Region("Column 9", world.player, world.multiworld),
		"Column 10": Region("Column 10", world.player, world.multiworld)
	}
	
	connect_region("Menu", "Column 1", region_map, None, lambda state: has_column(state, player, options, 1))
	connect_region("Column 1", "Column 2", region_map, None, lambda state: has_column(state, player, options, 2))
	connect_region("Column 2", "Column 3", region_map, None, lambda state: has_column(state, player, options, 3))
	connect_region("Column 3", "Column 4", region_map, None, lambda state: has_column(state, player, options, 4))
	connect_region("Column 4", "Column 5", region_map, None, lambda state: has_column(state, player, options, 5))
	connect_region("Column 5", "Column 6", region_map, None, lambda state: has_column(state, player, options, 6))
	connect_region("Column 6", "Column 7", region_map, None, lambda state: has_column(state, player, options, 7))
	connect_region("Column 7", "Column 8", region_map, None, lambda state: has_column(state, player, options, 8))
	connect_region("Column 8", "Column 9", region_map, None, lambda state: has_column(state, player, options, 9))
	connect_region("Column 9", "Column 10", region_map, None, lambda state: has_column(state, player, options, 10))
	for location in base_game:
		if location[1] in region_map:
			make_location(world, location[0], location[1], region_map, rule_map)
	if options.ducks_please:
		for location in ducks_please:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map)
	
	if options.duck_addiction:
		for location in duck_addiction:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map)
	
	if options.so_many_ducks:
		for location in so_many_ducks:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map)
	
	if options.ducks_galore:
		for location in ducks_galore:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map)
	
	if options.ducklings:
		for location in ducklings:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map)
	
	
	for region in region_map.values():
		world.multiworld.regions.append(region)

def connect_region(from_region, to_region, region_map, name, rule):
	if from_region not in region_map: return
	if to_region not in region_map: return
	region_map[from_region].connect(region_map[to_region], name, rule = rule)

def make_location(world, location_name, region_name, region_map, rule_map):
	if region_name not in region_map: return None
	world.location_count += 1
	return make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region_name, region_map, rule_map)

def make_event_location(world, location_name_a, location_name_b, item_name, id, region_name, region_map, rule_map):
	if region_name not in region_map: return None
	location = make_location_adv(world, location_name_a, location_name_b, id, region_name, region_map, rule_map)
	if location is None: return None
	return location.place_locked_item(Item(item_name, ItemClassification.progression, None, world.player))

def make_location_adv(world, location_name_a, location_name_b, id, region_name, region_map, rule_map):
	if region_name not in region_map: return None
	location = Location(world.player, location_name_a, id, region_map[region_name])
	region_map[region_name].locations.append(location)
	
	if location_name_b in rule_map:
	   location.access_rule = rule_map[location_name_b]
	
	if location_name_a in priority_map:
	   location.progress_type = priority_map[location_name_a]
	
	return location