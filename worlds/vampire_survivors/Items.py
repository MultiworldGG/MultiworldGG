from BaseClasses import ItemClassification
from .Locations import *
from .Options import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

unlock_character_items = [f"Character Unlock: {character}" for character in all_characters]

unlock_stage_items = [f"Stage Unlock: {stage}" for stage in (all_stages + [EUDAI])]

unlock_gamemodes = [f"Gamemode Unlock: {gamemode}" for gamemode in ["Hyper", "Hurry", "Arcanas", "Eggs"]]

filler_items = ['Empty Coffins', 'Floor Chickens', 'Suspiciously Clean Skull', 'Easter Eggs', 'Progressive Nothing']

item_table = {
	**{item: ItemClassification.progression for item in unlock_character_items},
	**{item: ItemClassification.progression for item in unlock_stage_items},
	**{item: ItemClassification.progression for item in unlock_gamemodes},
	**{item: ItemClassification.filler for item in filler_items}
}

raw_items = [item for item, classification in item_table.items()]

def gen_create_items(world):
	pool = world.multiworld.itempool
	options = world.options
	stages = world.final_included_stages_list
	characters = world.final_included_characters_list
	for stage in stages:
		if stage == world.starting_stage:
			continue
		pool.append(world.create_item(f"Stage Unlock: {stage}"))
	for character in characters:
		if character == world.starting_character:
			continue
		pool.append(world.create_item(f"Character Unlock: {character}"))
	if options.lock_hurry_behind_item:
		world.location_count -= 1
		pool.append(world.create_item("Gamemode Unlock: Hurry"))
	if options.lock_hyper_behind_item:
		world.location_count -= 1
		pool.append(world.create_item("Gamemode Unlock: Hyper"))
	if options.lock_arcanas_behind_item:
		world.location_count -= 1
		pool.append(world.create_item("Gamemode Unlock: Arcanas"))
	if options.egg_inclusion:
		world.location_count -= 1
		pool.append(world.create_item("Gamemode Unlock: Eggs"))
	world.location_count -= (len(stages) - 1) + (len(characters) - 1)
	for _ in range(world.location_count):
		pool.append(world.create_item(world.random.choice(filler_items)))