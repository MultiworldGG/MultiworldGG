from worlds.AutoWorld import WebWorld, World
from BaseClasses import Region, Tutorial, ItemClassification, Item, Location
from rule_builder.rules import Has
from dataclasses import dataclass
from Options import PerGameCommonOptions, TextChoice, Range

GAME = "Archipelaballs"
MAX_LEVEL = 500

class TargetScore(Range):
	"""Score needed to goal"""
	display_name = "Target Score"
	default = 100
	range_start = 50
	range_end = MAX_LEVEL

class DeathLink(TextChoice):
	"""When you die, everyone who enabled death link dies. Of course, the reverse is true too. If you enter a group name, you are only linked to the people in the same group.

	This can be adjusted later in the client, unless race mode is enabled."""

	display_name = "Death Link"
	default = 0
	option_false = 0
	option_true = 1

	@classmethod
	def get_option_name(cls, value):
		return value if isinstance(value, str) else ('Yes' if value else 'No')

@dataclass
class BallOptions(PerGameCommonOptions):
	target_score: TargetScore
	death_link: DeathLink

class WebBalls(WebWorld):
	setup_en = Tutorial(
		tutorial_name = "Multiworld Setup Guide",
		description = "A guide to playing Archipelaballs",
		language = "English",
		file_name = "setup_en.md",
		link = "setup/en",
		authors = ["StellatedCUBE"]
	)

	tutorials = [setup_en]
	game_info_languages = ["en"]
	rich_text_options_doc = True

class Ball(Item):
	game = GAME

class Row(Location):
	game = GAME

class Archipelaballs(World):
	'''A mobile game for Archipelago similar to Ketchapp's "Ballz"'''
	game = GAME
	web = WebBalls()
	options_dataclass = BallOptions
	item_name_to_id = {'ball': 1}
	location_name_to_id = {
		'Row %d' % i: i
		for i in range(2, MAX_LEVEL)
	}
	ut_can_gen_without_yaml = True

	def create_item(self, _ = None):
		return Ball('ball', ItemClassification.progression | ItemClassification.deprioritized, 1, self.player)
	
	def generate_early(self):
		if getattr(self.multiworld, "generation_is_fake", False):
			self.options.target_score.value = MAX_LEVEL
	
	def create_regions(self):
		region = Region("Menu", self.player, self.multiworld)
		self.multiworld.regions.append(region)

		self.rows = []
		for i in range(2, self.options.target_score.value):
			row = Row(self.player, 'row %d' % i, i, region)
			self.rows.append(row);
			region.locations.append(row)
			if i > 3:
				self.set_rule(row, Has('ball', i - 3))

		self.set_completion_rule(Has('ball', self.options.target_score.value - 5))
	
	def create_items(self):
		if not self.multiworld.precollected_items[self.player]:
			self.push_precollected(self.create_item())
		for i in range(2, self.options.target_score.value):
			self.multiworld.itempool.append(self.create_item())
	
	def fill_slot_data(self):
		slot_data = {
			'd': self.options.death_link.value,
			't': self.options.target_score.value
		}

		if len(self.multiworld.worlds) > 1:
			slot_data['l'] = hex(sum((row.item.player == self.player) << i for i, row in enumerate(self.rows)))[2:]

		return slot_data
