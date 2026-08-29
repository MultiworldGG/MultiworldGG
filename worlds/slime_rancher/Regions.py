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
		"The Ranch": Region("The Ranch", world.player, world.multiworld),
		"The Grotto": Region("The Grotto", world.player, world.multiworld),
		"The Overgrowth": Region("The Overgrowth", world.player, world.multiworld),
		"The Lab": Region("The Lab", world.player, world.multiworld),
		"The Docks": Region("The Docks", world.player, world.multiworld),
		"Dry Reef - Main": Region("Dry Reef - Main", world.player, world.multiworld),
		"Dry Reef - Beach": Region("Dry Reef - Beach", world.player, world.multiworld),
		"Dry Reef - Ring Island": Region("Dry Reef - Ring Island", world.player, world.multiworld),
		"The Slime Sea - Between Grotto and Dry Reef Island 2": Region("The Slime Sea - Between Grotto and Dry Reef Island 2", world.player, world.multiworld),
		"Dry Reef - Offshoot": Region("Dry Reef - Offshoot", world.player, world.multiworld),
		"The Slime Sea - Between Grotto and Dry Reef Island 1": Region("The Slime Sea - Between Grotto and Dry Reef Island 1", world.player, world.multiworld),
		"Moss Blanket - Hunter's Domain": Region("Moss Blanket - Hunter's Domain", world.player, world.multiworld),
		"The Slime Sea - Off Moss Blanket": Region("The Slime Sea - Off Moss Blanket", world.player, world.multiworld),
		"Indigo Quarry - Before First Bridge": Region("Indigo Quarry - Before First Bridge", world.player, world.multiworld),
		"Indigo Quarry - After The Bridge": Region("Indigo Quarry - After The Bridge", world.player, world.multiworld),
		"Indigo Quarry - Ancient Ruins Transition Overlap": Region("Indigo Quarry - Ancient Ruins Transition Overlap", world.player, world.multiworld),
		"Indigo Quarry - Ash Isles": Region("Indigo Quarry - Ash Isles", world.player, world.multiworld),
		"Ancient Ruins Transition": Region("Ancient Ruins Transition", world.player, world.multiworld),
		"Moss Blanket - Main": Region("Moss Blanket - Main", world.player, world.multiworld),
		"Moss Blanket - Mushroom Island": Region("Moss Blanket - Mushroom Island", world.player, world.multiworld),
		"Ancient Ruins - Main": Region("Ancient Ruins - Main", world.player, world.multiworld),
		"Ancient Ruins - Teleporter Room": Region("Ancient Ruins - Teleporter Room", world.player, world.multiworld),
		"Glass Desert - First Half": Region("Glass Desert - First Half", world.player, world.multiworld),
		"Glass Desert - Second Half": Region("Glass Desert - Second Half", world.player, world.multiworld)
	}
	
	if options.postgame or (options.easy_skips and options.postgame) or options.postgame or (options.precise_movement and options.postgame) or options.postgame or options.postgame:
		region_map["Post-Game"] = Region("Post-Game", world.player, world.multiworld)
	if options.postgame or (options.easy_skips and options.postgame):
		region_map["Dry Reef - H Vault"] = Region("Dry Reef - H Vault", world.player, world.multiworld)
	if options.obscure_locations:
		region_map["The Slime Sea - Mustache Shrine"] = Region("The Slime Sea - Mustache Shrine", world.player, world.multiworld)
	if options.postgame or (options.precise_movement and options.postgame):
		region_map["Indigo Quarry - H Vault"] = Region("Indigo Quarry - H Vault", world.player, world.multiworld)
	if options.postgame:
		region_map["Moss Blanket - H Vault"] = Region("Moss Blanket - H Vault", world.player, world.multiworld)
	if options.include_ogden:
		region_map["Ogden's Retreat"] = Region("Ogden's Retreat", world.player, world.multiworld)
		region_map["The Wilds"] = Region("The Wilds", world.player, world.multiworld)
	if options.include_mochi:
		region_map["Mochi's Manor"] = Region("Mochi's Manor", world.player, world.multiworld)
		region_map["Nimble Valley"] = Region("Nimble Valley", world.player, world.multiworld)
	if options.include_viktor:
		region_map["Viktor's Workshop"] = Region("Viktor's Workshop", world.player, world.multiworld)
		region_map["The Slimeulation"] = Region("The Slimeulation", world.player, world.multiworld)
	connect_region("Menu", "The Ranch", region_map, None, lambda state: True, False)
	connect_region("The Ranch", "The Grotto", region_map, None, lambda state: has_region(state, player, options, "The Grotto"), False)
	connect_region("The Ranch", "The Overgrowth", region_map, None, lambda state: has_region(state, player, options, "The Overgrowth"), False)
	connect_region("The Ranch", "The Lab", region_map, None, lambda state: has_region(state, player, options, "The Lab"), False)
	connect_region("The Overgrowth", "The Docks", region_map, None, lambda state: has_region(state, player, options, "The Docks"), False)
	connect_region("Dry Reef - Main", "The Docks", region_map, None, lambda state: has_region(state, player, options, "The Docks"), False)
	connect_region("The Overgrowth", "Ogden's Retreat", region_map, None, lambda state: has_region(state, player, options, "Ogden's Retreat") and has(state, player, options, 'Boom Plort') and has(state, player, options, 'Honey Plort') and has(state, player, options, 'Hunter Plort') and has_gate(state, player, options, "Slime Gate - Dry Reef to Moss Blanket"), False)
	connect_region("The Grotto", "Mochi's Manor", region_map, None, lambda state: has_region(state, player, options, "Mochi's Manor") and has(state, player, options, 'Boom Plort') and has(state, player, options, 'Rad Plort') and has(state, player, options, 'Crystal Plort') and has_gate(state, player, options, "Slime Gate - Dry Reef to Indigo Quarry"), False)
	connect_region("The Lab", "Viktor's Workshop", region_map, None, lambda state: has_region(state, player, options, "Viktor's Workshop") and has(state, player, options, 'Quantum Plort') and has_gate(state, player, options, "Slime Gate - Ancient Ruins Transition to Ancient Ruins"), False)
	connect_region("The Ranch", "Dry Reef - Main", region_map, None, lambda state: has_region(state, player, options, "Dry Reef"), False)
	connect_region("The Overgrowth", "Dry Reef - Beach", region_map, None, lambda state: has_region(state, player, options, "Dry Reef"), False)
	connect_region("Dry Reef - Main", "Dry Reef - Beach", region_map, None, lambda state: has_region(state, player, options, "Dry Reef"), False)
	connect_region("Dry Reef - Beach", "Dry Reef - Ring Island", region_map, None, lambda state: (has_region(state, player, options, "Dry Reef") and get_yaml_option(state, player, options, 'easy_skips')) or (has_region(state, player, options, "Dry Reef") and has_jetpack(state, player, options)), False)
	connect_region("The Slime Sea - Between Grotto and Dry Reef Island 2", "Dry Reef - Offshoot", region_map, None, lambda state: has_region(state, player, options, "Dry Reef") and has_jetpack(state, player, options), False)
	connect_region("The Grotto", "The Slime Sea - Between Grotto and Dry Reef Island 1", region_map, None, lambda state: (get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'obscure_locations')) or has_jetpack(state, player, options), False)
	connect_region("The Slime Sea - Between Grotto and Dry Reef Island 2", "The Slime Sea - Between Grotto and Dry Reef Island 1", region_map, None, lambda state: has_jetpack(state, player, options), False)
	connect_region("The Slime Sea - Between Grotto and Dry Reef Island 1", "The Slime Sea - Between Grotto and Dry Reef Island 2", region_map, None, lambda state: has_jetpack(state, player, options) or (get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'dangerous_skips')), False)
	connect_region("Dry Reef - Offshoot", "The Slime Sea - Between Grotto and Dry Reef Island 2", region_map, None, lambda state: has_jetpack(state, player, options), False)
	connect_region("Moss Blanket - Hunter's Domain", "The Slime Sea - Off Moss Blanket", region_map, None, lambda state: (has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options) and has_energy(state, player, options, 3)) or (has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options) and has_energy(state, player, options, 2) and get_yaml_option(state, player, options, 'obscure_locations')), False)
	connect_region("Dry Reef - Main", "Indigo Quarry - Before First Bridge", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry"), False)
	connect_region("Indigo Quarry - After The Bridge", "Indigo Quarry - Before First Bridge", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry") and has_jetpack(state, player, options), False)
	connect_region("Indigo Quarry - Before First Bridge", "Indigo Quarry - After The Bridge", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry") and has_jetpack(state, player, options), False)
	connect_region("Indigo Quarry - Ancient Ruins Transition Overlap", "Indigo Quarry - After The Bridge", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry"), False)
	connect_region("Indigo Quarry - After The Bridge", "Indigo Quarry - Ash Isles", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry"), False)
	connect_region("Indigo Quarry - After The Bridge", "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry") and has_region(state, player, options, "Ancient Ruins Transition"), False)
	connect_region("Ancient Ruins Transition", "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, None, lambda state: has_region(state, player, options, "Indigo Quarry") and has_region(state, player, options, "Ancient Ruins Transition"), False)
	connect_region("Dry Reef - Main", "Moss Blanket - Main", region_map, None, lambda state: has_region(state, player, options, "Moss Blanket") or (has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options) and get_yaml_option(state, player, options, 'easy_skips')), False)
	connect_region("Moss Blanket - Main", "Moss Blanket - Mushroom Island", region_map, None, lambda state: (has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options)) or (has_region(state, player, options, "Moss Blanket") and get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'obscure_locations')), False)
	connect_region("Moss Blanket - Main", "Moss Blanket - Hunter's Domain", region_map, None, lambda state: (has_region(state, player, options, "Moss Blanket") and get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'dangerous_skips')) or (has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options)), False)
	connect_region("Moss Blanket - Main", "Ancient Ruins Transition", region_map, None, lambda state: has_region(state, player, options, "Ancient Ruins Transition"), False)
	connect_region("Indigo Quarry - Ancient Ruins Transition Overlap", "Ancient Ruins Transition", region_map, None, lambda state: has_region(state, player, options, "Ancient Ruins Transition"), False)
	connect_region("Ancient Ruins Transition", "Ancient Ruins - Main", region_map, None, lambda state: has_region(state, player, options, "Ancient Ruins") and has(state, player, options, 'Tabby Plort') and has(state, player, options, 'Rock Plort') and has(state, player, options, 'Phosphor Plort') and has(state, player, options, 'Boom Plort') and has(state, player, options, 'Rad Plort') and has(state, player, options, 'Honey Plort'), False)
	connect_region("Ancient Ruins - Main", "Ancient Ruins - Teleporter Room", region_map, None, lambda state: has_region(state, player, options, "Ancient Ruins"), False)
	connect_region("Ancient Ruins - Teleporter Room", "Glass Desert - First Half", region_map, None, lambda state: has_region(state, player, options, "Glass Desert") and has(state, player, options, 'Quantum Plort'), False)
	connect_region("Glass Desert - First Half", "Glass Desert - Second Half", region_map, None, lambda state: has_region(state, player, options, "Glass Desert") or (has_region(state, player, options, "Glass Desert") and has_jetpack(state, player, options) and get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'obscure_locations')) or (has_region(state, player, options, "Glass Desert") and has_jetpack(state, player, options) and has_energy(state, player, options, 1) and get_yaml_option(state, player, options, 'obscure_locations')), False)
	connect_region("Ogden's Retreat", "The Wilds", region_map, None, lambda state: has_region(state, player, options, "The Wilds"), False)
	connect_region("Mochi's Manor", "Nimble Valley", region_map, None, lambda state: has_region(state, player, options, "Nimble Valley"), False)
	connect_region("Viktor's Workshop", "The Slimeulation", region_map, None, lambda state: has_region(state, player, options, "The Slimeulations"), False)
	if options.obscure_locations:
		connect_region("The Ranch", "The Docks", region_map, None, lambda state: has_region(state, player, options, "The Docks") and get_yaml_option(state, player, options, 'obscure_locations'), False)
	
	if options.obscure_locations:
		connect_region("The Ranch", "Dry Reef - Beach", region_map, None, lambda state: has_region(state, player, options, "Dry Reef") and get_yaml_option(state, player, options, 'obscure_locations'), False)
	
	if options.postgame or (options.easy_skips and options.postgame):
		connect_region("Post-Game", "Dry Reef - H Vault", region_map, None, lambda state: (has_region(state, player, options, "Dry Reef") and has_jetpack(state, player, options) and get_yaml_option(state, player, options, 'postgame')) or (has_region(state, player, options, "Dry Reef") and get_yaml_option(state, player, options, 'easy_skips') and get_yaml_option(state, player, options, 'postgame')), False)
	
	if options.precise_movement:
		connect_region("Dry Reef - Main", "Dry Reef - Offshoot", region_map, None, lambda state: has_region(state, player, options, "Dry Reef") and get_yaml_option(state, player, options, 'precise_movement'), False)
	
	if options.obscure_locations:
		connect_region("Dry Reef - Main", "The Slime Sea - Mustache Shrine", region_map, None, lambda state: has_jetpack(state, player, options) and has_energy(state, player, options, 3) and get_yaml_option(state, player, options, 'obscure_locations'), False)
	
	if options.postgame or (options.precise_movement and options.postgame):
		connect_region("Post-Game", "Indigo Quarry - H Vault", region_map, None, lambda state: (has_region(state, player, options, "Indigo Quarry") and has_jetpack(state, player, options) and get_yaml_option(state, player, options, 'postgame')) or (has_region(state, player, options, "Indigo Quarry") and get_yaml_option(state, player, options, 'precise_movement') and get_yaml_option(state, player, options, 'postgame')), False)
	
	if options.postgame:
		connect_region("Post-Game", "Moss Blanket - H Vault", region_map, None, lambda state: has_region(state, player, options, "Moss Blanket") and has_jetpack(state, player, options) and get_yaml_option(state, player, options, 'postgame'), False)
	
	if options.postgame:
		connect_region("Glass Desert - Second Half", "Post-Game", region_map, None, lambda state: get_yaml_option(state, player, options, 'postgame'), False)
	
	make_location(world, "Buy Personal Upgrade (Heart Module lv.1)", "Menu", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Heart Module lv.2)", "Dry Reef - Main", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Heart Module lv.3)", "Dry Reef - Main", region_map, rule_map, False)
	if world.options.include_7z:
		make_location(world, "Buy Personal Upgrade (Heart Module lv.4)", "Ancient Ruins - Main", region_map, rule_map, False)
	
	make_location(world, "Buy Personal Upgrade (Tank Booster lv.1)", "Menu", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Tank Booster lv.2)", "Dry Reef - Main", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Tank Booster lv.3)", "Dry Reef - Main", region_map, rule_map, False)
	if world.options.include_7z:
		make_location(world, "Buy Personal Upgrade (Tank Booster lv.4)", "Ancient Ruins - Main", region_map, rule_map, False)
	
	make_location(world, "Buy Personal Upgrade (Dash Boots lv.1)", "Menu", region_map, rule_map, False)
	if world.options.include_7z:
		make_location(world, "Buy Personal Upgrade (Dash Boots lv.2)", "Ancient Ruins - Main", region_map, rule_map, False)
	
	make_location(world, "Buy Personal Upgrade (Power Core lv.1)", "Menu", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Power Core lv.2)", "Dry Reef - Main", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Power Core lv.3)", "Dry Reef - Main", region_map, rule_map, False)
	if 1 <= world.options.treasure_cracker_checks:
		make_location(world, "Buy Personal Upgrade (Treasure Cracker lv.1)", "The Lab", region_map, rule_map, False)
	
	if 2 <= world.options.treasure_cracker_checks:
		make_location(world, "Buy Personal Upgrade (Treasure Cracker lv.2)", "The Lab", region_map, rule_map, False)
	
	if 3 <= world.options.treasure_cracker_checks:
		make_location(world, "Buy Personal Upgrade (Treasure Cracker lv.3)", "The Lab", region_map, rule_map, False)
	
	make_location(world, "Buy Personal Upgrade (Jetpack)", "Menu", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Air Drive)", "Dry Reef - Main", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Pulse Wave)", "Menu", region_map, rule_map, False)
	make_location(world, "Buy Personal Upgrade (Liquid Slot)", "Menu", region_map, rule_map, False)
	for location in interactables:
		if location[1] in region_map:
			make_location(world, location[0], location[1], region_map, rule_map, False)
	if world.options.goal_type == 0:
		make_event_location(world, "Read: The Grotto - The Limitless Black of Space", "The Grotto - The Limitless Black of Space", "Note Read", None, "The Grotto", region_map, rule_map, False)
		make_event_location(world, "Read: The Overgrowth - Artifical Moss Blanket", "The Overgrowth - Artifical Moss Blanket", "Note Read", None, "The Overgrowth", region_map, rule_map, False)
		make_event_location(world, "Read: The Lab - The Wonders of Plort Technology", "The Lab - The Wonders of Plort Technology", "Note Read", None, "The Lab", region_map, rule_map, False)
		make_event_location(world, "Read: The Docks - Our Greater Purpose", "The Docks - Our Greater Purpose", "Note Read", None, "The Docks", region_map, rule_map, False)
		make_event_location(world, "Read: Dry Reef - Hobson's Greetings", "Dry Reef - Hobson's Greetings", "Note Read", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Dry Reef - Indigo Quarry Entrance", "Dry Reef - Indigo Quarry Entrance", "Note Read", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Dry Reef - Great Big Tree", "Dry Reef - Great Big Tree", "Note Read", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Dry Reef - A Darn Good Boot", "Dry Reef - A Darn Good Boot", "Note Read", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Dry Reef - Ruminating on the Beach", "Dry Reef - Ruminating on the Beach", "Note Read", None, "Dry Reef - Beach", region_map, rule_map, False)
		make_event_location(world, "Read: Ring Island - We'd Get Along Just Fine", "Ring Island - We'd Get Along Just Fine", "Note Read", None, "Dry Reef - Ring Island", region_map, rule_map, False)
		make_event_location(world, "Read: Indigo Quarry - I Liked Her Laugh", "Indigo Quarry - I Liked Her Laugh", "Note Read", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
		make_event_location(world, "Read: Indigo Quarry - Crystal Wind Chime", "Indigo Quarry - Crystal Wind Chime", "Note Read", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
		make_event_location(world, "Read: Indigo Quarry - Peeping Puddle Slimes", "Indigo Quarry - Peeping Puddle Slimes", "Note Read", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
		make_event_location(world, "Read: Ash Isles - Looking to the Stars", "Ash Isles - Looking to the Stars", "Note Read", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
		make_event_location(world, "Read: Moss Blanket - New Ancient Jungle", "Moss Blanket - New Ancient Jungle", "Note Read", None, "Moss Blanket - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Moss Blanket - MOSS BLANKET STUCK", "Moss Blanket - MOSS BLANKET STUCK", "Note Read", None, "Moss Blanket - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Moss Blanket - Can't Recommend Love Enough", "Moss Blanket - Can't Recommend Love Enough", "Note Read", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
		make_event_location(world, "Read: Moss Blanket - Peepers Peeled!", "Moss Blanket - Peepers Peeled!", "Note Read", None, "Moss Blanket - Hunter's Domain", region_map, rule_map, False)
		make_event_location(world, "Read: Ancient Ruins - These Folks Like Slimes", "Ancient Ruins - These Folks Like Slimes", "Note Read", None, "Ancient Ruins - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Ancient Ruins - You Gotta Choose a Path", "Ancient Ruins - You Gotta Choose a Path", "Note Read", None, "Ancient Ruins - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Ancient Ruins - Ice-Cold Lemonade", "Ancient Ruins - Ice-Cold Lemonade", "Note Read", None, "Ancient Ruins - Main", region_map, rule_map, False)
		make_event_location(world, "Read: Ancient Ruins - Truly Untamed Country", "Ancient Ruins - Truly Untamed Country", "Note Read", None, "Ancient Ruins - Teleporter Room", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - You'll Risk Burning Your Tuchus!", "Glass Desert - You'll Risk Burning Your Tuchus!", "Note Read", None, "Glass Desert - First Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - Life Waiting to Flow", "Glass Desert - Life Waiting to Flow", "Note Read", None, "Glass Desert - First Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - Flames Burning at an Unperceivable Pace", "Glass Desert - Flames Burning at an Unperceivable Pace", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - Two Doors", "Glass Desert - Two Doors", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - She Stole a Piece of My Heart", "Glass Desert - She Stole a Piece of My Heart", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - Sold the Ranch", "Glass Desert - Sold the Ranch", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - I Wasn't Ready", "Glass Desert - I Wasn't Ready", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		make_event_location(world, "Read: Glass Desert - The Sand Sea", "Glass Desert - The Sand Sea", "Note Read", None, "Glass Desert - Second Half", region_map, rule_map, False)
		
	
	if world.options.enable_stylish_dlc_treasure_pods:
		for location in dlc_interactables:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map, False)
	
	if world.options.include_7z:
		for location in corporate_locations:
			if location[1] in region_map:
				make_location(world, location[0], location[1], region_map, rule_map, False)
	
	if world.options.include_7z and world.options.goal_type == 1:
		for location in corporate_locations:
			if location[1] in region_map:
				make_event_location(world, f"Bought: {location[0]}", location[0], "7Zee Bought", None, location[1], region_map, rule_map, False)
	
	make_event_location(world, "Pink (The Ranch)", "''", "Pink Plort", None, "The Ranch", region_map, rule_map, False)
	make_event_location(world, "Pink (Dry Reef - Main)", "''", "Pink Plort", None, "Dry Reef - Main", region_map, rule_map, False)
	make_event_location(world, "Tabby (Dry Reef - Main)", "''", "Tabby Plort", None, "Dry Reef - Main", region_map, rule_map, False)
	make_event_location(world, "Rock (Dry Reef - Main)", "''", "Rock Plort", None, "Dry Reef - Main", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Dry Reef - Main)", "''", "Phosphor Plort", None, "Dry Reef - Main", region_map, rule_map, False)
	make_event_location(world, "Lucky (Dry Reef - Main)", "''", "Lucky Plort", None, "Dry Reef - Main", region_map, rule_map, False)
	make_event_location(world, "Pink (Dry Reef - Beach)", "''", "Pink Plort", None, "Dry Reef - Beach", region_map, rule_map, False)
	make_event_location(world, "Tabby (Dry Reef - Beach)", "''", "Tabby Plort", None, "Dry Reef - Beach", region_map, rule_map, False)
	make_event_location(world, "Rock (Dry Reef - Beach)", "''", "Rock Plort", None, "Dry Reef - Beach", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Dry Reef - Beach)", "''", "Phosphor Plort", None, "Dry Reef - Beach", region_map, rule_map, False)
	make_event_location(world, "Lucky (Dry Reef - Beach)", "''", "Lucky Plort", None, "Dry Reef - Beach", region_map, rule_map, False)
	make_event_location(world, "Pink (Dry Reef - Ring Island)", "''", "Pink Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Tabby (Dry Reef - Ring Island)", "''", "Tabby Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Rock (Dry Reef - Ring Island)", "''", "Rock Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Dry Reef - Ring Island)", "''", "Phosphor Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Lucky (Dry Reef - Ring Island)", "''", "Lucky Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Puddle (Dry Reef - Ring Island)", "''", "Puddle Plort", None, "Dry Reef - Ring Island", region_map, rule_map, False)
	make_event_location(world, "Pink (The Slime Sea - Between Grotto and Dry Reef Island 2)", "''", "Pink Plort", None, "The Slime Sea - Between Grotto and Dry Reef Island 2", region_map, rule_map, False)
	make_event_location(world, "Phosphor (The Slime Sea - Between Grotto and Dry Reef Island 2)", "''", "Phosphor Plort", None, "The Slime Sea - Between Grotto and Dry Reef Island 2", region_map, rule_map, False)
	make_event_location(world, "Lucky (The Slime Sea - Between Grotto and Dry Reef Island 2)", "''", "Lucky Plort", None, "The Slime Sea - Between Grotto and Dry Reef Island 2", region_map, rule_map, False)
	make_event_location(world, "Pink (Indigo Quarry - Before First Bridge)", "''", "Pink Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Rock (Indigo Quarry - Before First Bridge)", "''", "Rock Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Indigo Quarry - Before First Bridge)", "''", "Phosphor Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Boom (Indigo Quarry - Before First Bridge)", "''", "Boom Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Rad (Indigo Quarry - Before First Bridge)", "''", "Rad Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Crystal (Indigo Quarry - Before First Bridge)", "''", "Crystal Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Lucky (Indigo Quarry - Before First Bridge)", "''", "Lucky Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Puddle (Indigo Quarry - Before First Bridge)", "''", "Puddle Plort", None, "Indigo Quarry - Before First Bridge", region_map, rule_map, False)
	make_event_location(world, "Pink (Indigo Quarry - After The Bridge)", "''", "Pink Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Rock (Indigo Quarry - After The Bridge)", "''", "Rock Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Indigo Quarry - After The Bridge)", "''", "Phosphor Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Boom (Indigo Quarry - After The Bridge)", "''", "Boom Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Rad (Indigo Quarry - After The Bridge)", "''", "Rad Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Lucky (Indigo Quarry - After The Bridge)", "''", "Lucky Plort", None, "Indigo Quarry - After The Bridge", region_map, rule_map, False)
	make_event_location(world, "Pink (Indigo Quarry - Ash Isles)", "''", "Pink Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Rock (Indigo Quarry - Ash Isles)", "''", "Rock Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Indigo Quarry - Ash Isles)", "''", "Phosphor Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Boom (Indigo Quarry - Ash Isles)", "''", "Boom Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Crystal (Indigo Quarry - Ash Isles)", "''", "Crystal Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Lucky (Indigo Quarry - Ash Isles)", "''", "Lucky Plort", None, "Indigo Quarry - Ash Isles", region_map, rule_map, False)
	make_event_location(world, "Pink (Indigo Quarry - Ancient Ruins Transition Overlap)", "''", "Pink Plort", None, "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, rule_map, False)
	make_event_location(world, "Rock (Indigo Quarry - Ancient Ruins Transition Overlap)", "''", "Rock Plort", None, "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Indigo Quarry - Ancient Ruins Transition Overlap)", "''", "Phosphor Plort", None, "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, rule_map, False)
	make_event_location(world, "Boom (Indigo Quarry - Ancient Ruins Transition Overlap)", "''", "Boom Plort", None, "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, rule_map, False)
	make_event_location(world, "Lucky (Indigo Quarry - Ancient Ruins Transition Overlap)", "''", "Lucky Plort", None, "Indigo Quarry - Ancient Ruins Transition Overlap", region_map, rule_map, False)
	make_event_location(world, "Pink (Moss Blanket - Main)", "''", "Pink Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Tabby (Moss Blanket - Main)", "''", "Tabby Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Moss Blanket - Main)", "''", "Phosphor Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Boom (Moss Blanket - Main)", "''", "Boom Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Honey (Moss Blanket - Main)", "''", "Honey Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Hunter (Moss Blanket - Main)", "''", "Hunter Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Lucky (Moss Blanket - Main)", "''", "Lucky Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Puddle (Moss Blanket - Main)", "''", "Puddle Plort", None, "Moss Blanket - Main", region_map, rule_map, False)
	make_event_location(world, "Pink (Moss Blanket - Mushroom Island)", "''", "Pink Plort", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
	make_event_location(world, "Tabby (Moss Blanket - Mushroom Island)", "''", "Tabby Plort", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Moss Blanket - Mushroom Island)", "''", "Phosphor Plort", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
	make_event_location(world, "Hunter (Moss Blanket - Mushroom Island)", "''", "Hunter Plort", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
	make_event_location(world, "Lucky (Moss Blanket - Mushroom Island)", "''", "Lucky Plort", None, "Moss Blanket - Mushroom Island", region_map, rule_map, False)
	make_event_location(world, "Pink (Ancient Ruins - Main)", "''", "Pink Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Tabby (Ancient Ruins - Main)", "''", "Tabby Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Rock (Ancient Ruins - Main)", "''", "Rock Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Ancient Ruins - Main)", "''", "Phosphor Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Boom (Ancient Ruins - Main)", "''", "Boom Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Quantum (Ancient Ruins - Main)", "''", "Quantum Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Lucky (Ancient Ruins - Main)", "''", "Lucky Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Puddle (Ancient Ruins - Main)", "''", "Puddle Plort", None, "Ancient Ruins - Main", region_map, rule_map, False)
	make_event_location(world, "Pink (Glass Desert - First Half)", "''", "Pink Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Tabby (Glass Desert - First Half)", "''", "Tabby Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Rock (Glass Desert - First Half)", "''", "Rock Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Dervish (Glass Desert - First Half)", "''", "Dervish Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Tangle (Glass Desert - First Half)", "''", "Tangle Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Mosaic (Glass Desert - First Half)", "''", "Mosaic Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Lucky (Glass Desert - First Half)", "''", "Lucky Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Gold (Glass Desert - First Half)", "''", "Gold Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Fire (Glass Desert - First Half)", "''", "Fire Plort", None, "Glass Desert - First Half", region_map, rule_map, False)
	make_event_location(world, "Pink (Glass Desert - Second Half)", "''", "Pink Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Tabby (Glass Desert - Second Half)", "''", "Tabby Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Rock (Glass Desert - Second Half)", "''", "Rock Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Dervish (Glass Desert - Second Half)", "''", "Dervish Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Tangle (Glass Desert - Second Half)", "''", "Tangle Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Mosaic (Glass Desert - Second Half)", "''", "Mosaic Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Lucky (Glass Desert - Second Half)", "''", "Lucky Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Fire (Glass Desert - Second Half)", "''", "Fire Plort", None, "Glass Desert - Second Half", region_map, rule_map, False)
	make_event_location(world, "Pink (The Wilds)", "''", "Pink Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Tabby (The Wilds)", "''", "Tabby Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Rock (The Wilds)", "''", "Rock Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Rad (The Wilds)", "''", "Rad Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Hunter (The Wilds)", "''", "Hunter Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Lucky (The Wilds)", "''", "Lucky Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Saber (The Wilds)", "''", "Saber Plort", None, "The Wilds", region_map, rule_map, False)
	make_event_location(world, "Tabby (Dry Reef - Offshoot)", "''", "Tabby Plort", None, "Dry Reef - Offshoot", region_map, rule_map, False)
	make_event_location(world, "Rock (Dry Reef - Offshoot)", "''", "Rock Plort", None, "Dry Reef - Offshoot", region_map, rule_map, False)
	make_event_location(world, "Lucky (Dry Reef - Offshoot)", "''", "Lucky Plort", None, "Dry Reef - Offshoot", region_map, rule_map, False)
	make_event_location(world, "Phosphor (The Slime Sea - Between Grotto and Dry Reef Island 1)", "''", "Phosphor Plort", None, "The Slime Sea - Between Grotto and Dry Reef Island 1", region_map, rule_map, False)
	make_event_location(world, "Lucky (The Slime Sea - Between Grotto and Dry Reef Island 1)", "''", "Lucky Plort", None, "The Slime Sea - Between Grotto and Dry Reef Island 1", region_map, rule_map, False)
	make_event_location(world, "Phosphor (Moss Blanket - Hunter's Domain)", "''", "Phosphor Plort", None, "Moss Blanket - Hunter's Domain", region_map, rule_map, False)
	make_event_location(world, "Hunter (Moss Blanket - Hunter's Domain)", "''", "Hunter Plort", None, "Moss Blanket - Hunter's Domain", region_map, rule_map, False)
	make_event_location(world, "Lucky (Moss Blanket - Hunter's Domain)", "''", "Lucky Plort", None, "Moss Blanket - Hunter's Domain", region_map, rule_map, False)
	make_event_location(world, "Lucky (The Slime Sea - Mustache Shrine)", "''", "Lucky Plort", None, "The Slime Sea - Mustache Shrine", region_map, rule_map, False)
	make_event_location(world, "Lucky (Ancient Ruins Transition)", "''", "Lucky Plort", None, "Ancient Ruins Transition", region_map, rule_map, False)
	make_event_location(world, "Lucky (The Slime Sea - Off Moss Blanket)", "''", "Lucky Plort", None, "The Slime Sea - Off Moss Blanket", region_map, rule_map, False)
	make_event_location(world, "Quicksilver (Nimble Valley)", "''", "Quicksilver Plort", None, "Nimble Valley", region_map, rule_map, False)
	make_event_location(world, "Glitch (The Slimeulation)", "''", "Glitch Plort", None, "The Slimeulation", region_map, rule_map, False)
	
	if options.market_logic:
		make_event_location(world, "ML_Tabby (The Ranch)", "''", "Tabby Plort", None, "The Ranch", region_map, rule_map, False)
		make_event_location(world, "ML_Rock (The Ranch)", "''", "Rock Plort", None, "The Ranch", region_map, rule_map, False)
		make_event_location(world, "ML_Phosphor (The Ranch)", "''", "Phosphor Plort", None, "The Ranch", region_map, rule_map, False)
		make_event_location(world, "ML_Boom (Dry Reef - Main)", "''", "Boom Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "ML_Rad (Dry Reef - Main)", "''", "Rad Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "ML_Crystal (Dry Reef - Main)", "''", "Crystal Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "ML_Honey (Dry Reef - Main)", "''", "Honey Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "ML_Hunter (Dry Reef - Main)", "''", "Hunter Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		make_event_location(world, "ML_Puddle (Dry Reef - Main)", "''", "Puddle Plort", None, "Dry Reef - Main", region_map, rule_map, False)
		
	
	for location in gates:
		if location[1] in region_map:
			make_event_location(world, f"Event: {location[0]}", location[0], f"Opened Gate: {location[0]}", None, location[1], region_map, rule_map, False)
	if options.plortsanity > 0:
		make_location(world, "Sell a Pink Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Tabby Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Rock Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Phosphor Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Boom Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Rad Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Crystal Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Honey Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Hunter Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Quantum Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Dervish Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Tangle Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Mosaic Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Puddle Plort", "Menu", region_map, rule_map, False)
		make_location(world, "Sell a Fire Plort", "Menu", region_map, rule_map, False)
		
	
	if options.include_ogden and options.plortsanity > 0:
		make_location(world, "Sell a Saber Plort", "Menu", region_map, rule_map, False)
	
	if options.plortsanity > 1:
		make_location(world, "Sell a Gold Plort", "Menu", region_map, rule_map, False)
	
	
	for region in region_map.values():
		world.multiworld.regions.append(region)

def connect_region(from_region, to_region, region_map, name, rule, is_connection_crucial):
	if from_region not in region_map:
	   if is_connection_crucial: throw_needed_region_error(from_region, f"connect_region, from: [{from_region}]")
	   return
	if to_region not in region_map:
	   if is_connection_crucial: throw_needed_region_error(to_region, f"connect_region, to: [{to_region}]")
	   return
	region_map[from_region].connect(region_map[to_region], name, rule = rule)

def make_location(world, location_name, region_name, region_map, rule_map, is_location_crucial):
	loc = make_location_adv(world, location_name, location_name, world.location_name_to_id[location_name], region_name, region_map, rule_map, is_location_crucial)
	if loc is not None: world.location_count += 1
	return loc

def make_event_location(world, location_name_a, location_name_b, item_name, id, region_name, region_map, rule_map, is_location_crucial):
	location = make_location_adv(world, location_name_a, location_name_b, id, region_name, region_map, rule_map, is_location_crucial)
	if location is None: return None
	return location.place_locked_item(Item(item_name, ItemClassification.progression, None, world.player))

def make_location_adv(world, location_name_a, location_name_b, id, region_name, region_map, rule_map, is_location_crucial):
	if region_name not in region_map:
	   if is_location_crucial: throw_needed_region_error(region_name, f"make_location_adv, [{location_name_a}]")
	   return None
	
	location = Location(world.player, location_name_a, id, region_map[region_name])
	region_map[region_name].locations.append(location)
	
	if location_name_b in rule_map:
	   location.access_rule = rule_map[location_name_b]
	
	if location_name_a in priority_map:
	   location.progress_type = priority_map[location_name_a]
	
	return location

def throw_needed_region_error(region_name, sender):
	raise ValueError(f"For an unknown reason the region, [{region_name}] was not added as a region, it is required for [{sender}]")