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
		"Characters": Region("Characters", world.player, world.multiworld),
		"Enemies": Region("Enemies", world.player, world.multiworld),
		"Mad Forest": Region("Mad Forest", world.player, world.multiworld),
		"Eudaimonia M.": Region("Eudaimonia M.", world.player, world.multiworld),
		"Inlaid Library": Region("Inlaid Library", world.player, world.multiworld),
		"Dairy Plant": Region("Dairy Plant", world.player, world.multiworld),
		"Gallo Tower": Region("Gallo Tower", world.player, world.multiworld),
		"Cappella Magna": Region("Cappella Magna", world.player, world.multiworld),
		"Il Molise": Region("Il Molise", world.player, world.multiworld),
		"Moongolow": Region("Moongolow", world.player, world.multiworld),
		"Green Acres": Region("Green Acres", world.player, world.multiworld),
		"The Bone Zone": Region("The Bone Zone", world.player, world.multiworld),
		"Boss Rash": Region("Boss Rash", world.player, world.multiworld),
		"Whiteout": Region("Whiteout", world.player, world.multiworld),
		"The Coop": Region("The Coop", world.player, world.multiworld),
		"Space 54": Region("Space 54", world.player, world.multiworld),
		"Carlo Cart": Region("Carlo Cart", world.player, world.multiworld),
		"Laborratory": Region("Laborratory", world.player, world.multiworld),
		"Westwoods": Region("Westwoods", world.player, world.multiworld),
		"Bat Country": Region("Bat Country", world.player, world.multiworld),
		"Astral Stair": Region("Astral Stair", world.player, world.multiworld),
		"Mazerella": Region("Mazerella", world.player, world.multiworld),
		"Tiny Bridge": Region("Tiny Bridge", world.player, world.multiworld),
		"Mt.Moonspell": Region("Mt.Moonspell", world.player, world.multiworld),
		"Lake Foscari": Region("Lake Foscari", world.player, world.multiworld),
		"Abyss Foscari": Region("Abyss Foscari", world.player, world.multiworld),
		"Ante Chamber": Region("Ante Chamber", world.player, world.multiworld),
		"Room 1665": Region("Room 1665", world.player, world.multiworld),
		"Neo Galuga": Region("Neo Galuga", world.player, world.multiworld),
		"Hectic Highway": Region("Hectic Highway", world.player, world.multiworld),
		"Ode to Castlevania": Region("Ode to Castlevania", world.player, world.multiworld),
		"Polus Replica": Region("Polus Replica", world.player, world.multiworld),
		"Emerald Diorama": Region("Emerald Diorama", world.player, world.multiworld)
	}
	
	region_map["Menu"].connect(region_map["Characters"])
	region_map["Menu"].connect(region_map["Enemies"])
	stages = world.final_included_stages_list
	characters = world.final_included_characters_list
	chest_checks = options.chest_checks_per_stage
	for stage in stages:
		make_location(world, f"{stage} Beaten", region_map[stage], rule_map)
		make_event_location(world, f"Event: [{stage} Beaten]", f"{stage} Beaten", "Beat a Stage", None, region_map[stage], rule_map)
		if stage != EUDAI:
			for i in range(chest_checks):
				make_location(world, f"Open Chest #{i + 1} on {stage}", region_map[stage], rule_map)
		if stage == EUDAI and options.goal_requirement == 1:
			region_map["Menu"].connect(region_map[stage], rule = lambda state, stage_name=stage: has_stage(state, player, options, EUDAI) and has_amount(state, player, options, "Beat a Stage", world.ending_stage_count))
		else:
			region_map["Menu"].connect(region_map[stage], rule = lambda state, stage_name=stage: has_stage(state, player, options, f"{stage_name}"))
	for character in characters:
		make_location(world, f'Beat with {character}', region_map['Characters'], rule_map)
	if options.enemysanity:
		for enemy, raw_find_locs in enemy_map.items():
			if enemy in enemy_arcana_map and not options.enemysanity_arcana_enemies:
				continue
			if enemy == 'Death' and ('Ode to Castlevania' not in stages or 'Richter Belmont' not in characters):
				continue
			if not any(loc in stages for loc in raw_find_locs):
				continue
			make_location(world, f"Kill {enemy}", region_map['Enemies'], rule_map)
	
	for region in region_map.values():
		world.multiworld.regions.append(region)

def make_location(world, location_name, region, rule_map):
	world.location_count += 1
	return make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region, rule_map)

def make_event_location(world, location_name_a, location_name_b, item_name, id, region, rule_map):
	location = make_location_adv(world, location_name_a, location_name_b, id, region, rule_map)
	location.place_locked_item(Item(item_name, ItemClassification.progression, None, world.player))

def make_location_adv(world, location_name_a, location_name_b, id, region, rule_map):
	location = Location(world.player, location_name_a, id, region)
	region.locations.append(location)
	
	if location_name_b in rule_map:
	   location.access_rule = rule_map[location_name_b]
	
	if location_name_a in priority_map:
	   location.progress_type = priority_map[location_name_a]
	
	return location