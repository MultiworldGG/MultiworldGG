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
class VampireSurvivorsWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Vampire Survivors for a MultiworldGG Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SW_CreeperKing"]
    )
    
    tutorials = [setup_en]

class VampireSurvivors(World):
	"""
	Vampire Survivors is a 2022 independent roguelike shoot 'em up video game where players control an automatically attacking character while battling continuous waves of monsters, 
	aiming to survive the onslaught for as long as possible and unlock additional characters, weapons, and relics for future sessions.
	"""
	game = "Vampire Survivors"
	author: str = "SW_CreeperKing"
	options_dataclass = VampireSurvivorsOptions
	options: VampireSurvivorsOptions
	settings: ClassVar[VampireSurvivorsSettings]
	location_name_to_id = {value: location_dict.index(value) + 1 for value in location_dict}
	item_name_to_id = {value: raw_items.index(value) + 1 for value in raw_items}
	topology_present = True
	ut_can_gen_without_yaml = True
	gen_puml = False
	web = VampireSurvivorsWeb()
	item_name_groups = {
		"unlocks": unlock_character_items + unlock_stage_items + unlock_gamemodes
	}

	def __init__(self, multiworld: "MultiWorld", player: int):
		super().__init__(multiworld, player)
		self.location_count = 0
		self.starting_character = ""
		self.starting_stage = ""
		self.stage_goal_amount = 0
		self.final_included_characters_list = []
		self.final_included_stages_list = []
		self.ending_character_count = 0
		self.ending_stage_count = 0

	def generate_early(self):
		options = self.options
		if hasattr(self.multiworld, "re_gen_passthrough"):
			if "Vampire Survivors" not in self.multiworld.re_gen_passthrough: return
			passthrough = self.multiworld.re_gen_passthrough["Vampire Survivors"]
			if "starting_character" in passthrough:
				self.starting_character = passthrough["starting_character"]
			
			if "self.starting_stage" in passthrough:
				self.starting_stage = passthrough["self.starting_stage"]
			
			if "final_stages" in passthrough:
				self.final_included_stages_list = passthrough["final_stages"]
			
			if "final_chars" in passthrough:
				self.final_included_characters_list = passthrough["final_chars"]
			
			if "ending_stage_count" in passthrough:
				self.ending_stage_count = passthrough["ending_stage_count"]
			
			self.multiworld.push_precollected(self.create_item(f"Stage Unlock: {self.starting_stage}"))
			self.multiworld.push_precollected(self.create_item(f"Character Unlock: {self.starting_character}"))
			if self.options.lock_arcanas_behind_item.value:
			    self.multiworld.push_precollected(self.create_item("Gamemode Unlock: Arcanas"))
			if self.options.lock_hurry_behind_item.value:
			    self.multiworld.push_precollected(self.create_item("Gamemode Unlock: Hurry"))
		check_options(self)
		stages = [stage for stage in self.final_included_stages_list if stage != EUDAI]
		characters = self.final_included_characters_list
		
		if len(stages) > 1:
			stages_to_choose_from = [stage for stage in stages if stage in normal_stages]
		
			if len(stages_to_choose_from) == 0:
				stages_to_choose_from = [stage for stage in stages if stage in bonus_stages]
		
			if len(stages_to_choose_from) == 0:
				stages_to_choose_from = [stage for stage in stages if stage in challenge_stages]
		
			if len(stages_to_choose_from) == 0:
				self.starting_stage = self.random.choice(stages)
			else:
				self.starting_stage = self.random.choice(stages_to_choose_from)
		else:
			self.starting_stage = stages[0]
		
		if len(characters) > 1:  # choose lesser powerful characters to start with
			characters_to_choose_from = [character for character in characters if character in non_special_characters]
		
			if self.options.allow_secret_characters and len(characters_to_choose_from) == 0:
				characters_to_choose_from = [character for character in characters if character in secret_characters]
		
			if self.options.allow_megalo_characters and len(characters_to_choose_from) == 0:
				characters_to_choose_from = [character for character in characters if character in megalo_characters]
		
			if self.options.allow_unfair_characters and self.settings.allow_unfair_characters and len(
					characters_to_choose_from) == 0:
				characters_to_choose_from = [character for character in characters if character in unfair_characters]
		
			self.starting_character = self.random.choice(characters_to_choose_from)
		else:
			self.starting_character = characters[0]
		self.stage_goal_amount = len(stages)
		
		self.multiworld.push_precollected(self.create_item(f"Stage Unlock: {self.starting_stage}"))
		self.multiworld.push_precollected(self.create_item(f"Character Unlock: {self.starting_character}"))
		
		if not self.options.lock_arcanas_behind_item.value:
		    self.multiworld.push_precollected(self.create_item(f"Gamemode Unlock: Arcanas"))
		if not self.options.lock_hurry_behind_item.value:
			self.multiworld.push_precollected(self.create_item("Gamemode Unlock: Hurry"))

	def create_regions(self):
		gen_create_regions(self)

	def create_item(self, name: str):
		return Item(name, item_table[name], self.item_name_to_id[name], self.player)

	def create_items(self):
		gen_create_items(self)

	def set_rules(self):
		player = self.player
		options = self.options
		if self.options.goal_requirement == 0:
			self.multiworld.completion_condition[self.player] = lambda state: has_amount(state, player, options, "Beat a Stage", self.stage_goal_amount)
		elif self.options.goal_requirement == 1:
			self.multiworld.completion_condition[self.player] = lambda state: has_stage(state, player, options, EUDAI) and has_amount(state, player, options, "Beat a Stage", self.ending_stage_count)

	def fill_slot_data(self):
		slot_data = {
			"goal_requirement": int(self.options.goal_requirement),
			"chest_checks_per_stage": int(self.options.chest_checks_per_stage),
			"egg_inclusion": int(self.options.egg_inclusion.value),
			"lock_hyper_behind_item": bool(self.options.lock_hyper_behind_item),
			"lock_hurry_behind_item": bool(self.options.lock_hurry_behind_item),
			"lock_arcanas_behind_item": bool(self.options.lock_arcanas_behind_item),
			"enemysanity": bool(self.options.enemysanity),
			"enemysanity_arcana_enemies": bool(self.options.enemysanity_arcana_enemies),
			"character_pool_size": int(self.options.character_pool_size),
			"stage_pool_size": int(self.options.stage_pool_size),
			"allow_secret_characters": bool(self.options.allow_secret_characters),
			"allow_megalo_characters": bool(self.options.allow_megalo_characters),
			"allow_unfair_characters": bool(self.options.allow_unfair_characters),
			"included_base_characters": str(self.options.included_base_characters),
			"included_moonspell_characters": str(self.options.included_moonspell_characters),
			"included_foscari_characters": str(self.options.included_foscari_characters),
			"included_amongus_characters": str(self.options.included_amongus_characters),
			"included_operation_guns_characters": str(self.options.included_operation_guns_characters),
			"included_castlevania_characters": str(self.options.included_castlevania_characters),
			"included_emerald_characters": str(self.options.included_emerald_characters),
			"included_balatro_characters": str(self.options.included_balatro_characters),
			"included_normal_stages": str(self.options.included_normal_stages),
			"included_bonus_stages": str(self.options.included_bonus_stages),
			"included_challenge_stages": str(self.options.included_challenge_stages),
			"included_moonspell_stages": str(self.options.included_moonspell_stages),
			"included_foscari_stages": str(self.options.included_foscari_stages),
			"included_amongus_stages": str(self.options.included_amongus_stages),
			"included_operation_guns_stages": str(self.options.included_operation_guns_stages),
			"included_castlevania_stages": str(self.options.included_castlevania_stages),
			"included_emerald_stages": str(self.options.included_emerald_stages),
			"included_balatro_stages": str(self.options.included_balatro_stages),
			"starting_character": str(self.starting_character),
			"starting_stage": str(self.starting_stage),
			"stages_to_beat": str(self.final_included_stages_list),
			"is_hyper_locked": bool(self.options.lock_hyper_behind_item),
			"is_hurry_locked": bool(self.options.lock_hurry_behind_item),
			"is_arcanas_locked": bool(self.options.lock_arcanas_behind_item),
			"final_stages": self.final_included_stages_list,
			"final_chars": self.final_included_characters_list,
			"ending_stage_count": int(self.ending_stage_count)
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