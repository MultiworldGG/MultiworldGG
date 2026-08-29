from worlds.AutoWorld import *
from .Locations import *
from .Rules import *
from .Options import *
from .Items import *
from .Regions import *
from .Settings import *
from typing import *
from BaseClasses import Tutorial

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]
class SlimeRancherWeb(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Slime Rancher with MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["SW_CreeperKing"]
    )
    tutorials = [setup_en]
	
class SlimeRancher(World):
	"""
	Slime Rancher is a 1st person farm life sim video game, playing in an open world. As Beatrix LeBeau you construct your ranch and explore the world of the Far Far Range in order to collect, raise, feed, and breed slimes. 
	"""
	game = "Slime Rancher"
	options_dataclass = SlimeRancherOptions
	options: SlimeRancherOptions
	settings: ClassVar[SlimeRancherSettings]
	topology_present = True
	ut_can_gen_without_yaml = True
	gen_puml = False
	location_name_to_id = {value: location_dict.index(value) + 1 for value in location_dict}
	item_name_to_id = {value: raw_items.index(value) + 1 for value in raw_items}
	item_name_groups = {
		"unlocks": region_unlocks
	}
	web = SlimeRancherWeb()
	location_name_groups = {
		"The Ranch": ["The Grotto - The Limitless Black of Space", "The Grotto - Overlooking the Slime Sea", "The Overgrowth - Artifical Moss Blanket", "The Lab - The Wonders of Plort Technology", "The Lab - Tinkerer's Starting Cache", "The Docks - Our Greater Purpose"],
		"Ogden's Retreat": ["Ogden's Retreat - That's a Whole Lotta Kookabobas", "The Wilds - Across From the Hunter's Sakura Tree", "The Wilds - On a Cliff Dividing Two Entrances", "The Wilds - A Precarious Ledge By the Waterfall", "The Wilds - An Outcropping Near the Beach", "The Wilds - Inside a Pink Tree Stump", "The Wilds - Hidden Bridge Behind a Triangular Staircase", "The Wilds - Double Waterfall Treasure", "The Wilds - On a Tiny Ledge Overlooking the Underground River", "The Wilds - Coral Ring Island Exit"],
		"Dry Reef": ["Dry Reef - Hobson's Greetings", "Dry Reef - Indigo Quarry Entrance", "Dry Reef - Great Big Tree", "Dry Reef - A Darn Good Boot", "Dry Reef - Map Data Node", "Dry Reef - Hidden Behind a Short Wall", "Dry Reef - Phosphor Gordo's Personal Pod", "Dry Reef - In the Cliff Tree's Roots", "Dry Reef - Nested by Tabby Gordo", "Dry Reef - Stony Hen Hen Coop", "Dry Reef - Hidden Away on an ARCH-ipelago", "Dry Reef - Overlooking the Tarr Hotspot", "Dry Reef - Hidden Crevice Under the Hidden Cliff", "Dry Reef - Hidden Treasure of the Pink Gordo", "Dry Reef - Nested in Crystal", "Dry Reef - Ruminating on the Beach", "Dry Reef - Carrot Patch Cache", "Dry Reef - Tiny Not-Huge Island", "Ring Island - We'd Get Along Just Fine", "Ring Island - Flower Viewing on a Cliff", "Ring Island - Perilously Perched Pod", "Ring Island - Hidden on the Backside of the Island", "Ring Island - King of the Hill", "Dry Reef - Hidden in the Shade", "Dry Reef - Beneath the Wooden Scaffolding", "The Slime Sea - Island Alone in the Sea"],
		"Post-Game": ["Ring Island Vault - Don't Get Too Greedy Pod 1", "Ring Island Vault - Don't Get Too Greedy Pod 2", "Ring Island Vault - Don't Get Too Greedy Pod 3", "Ring Island Vault - Don't Get Too Greedy Pod 4", "Ring Island Vault - The Quintessential Quintuplet #1", "Ring Island Vault - The Quintessential Quintuplet #2", "Ring Island Vault - The Quintessential Quintuplet #3", "Ring Island Vault - The Quintessential Quintuplet #4", "Ring Island Vault - The Quintessential Quintuplet #5", "Ring Island Vault - Mushroom Column Riches #1", "Ring Island Vault - Mushroom Column Riches #2", "Ring Island Vault - Mushroom Column Riches #3", "Ring Island Vault - Boring Column Riches #1", "Ring Island Vault - Boring Column Riches #2", "Ash Isle Vault - The Lone Pod Stands Alone", "Ash Isle Vault - Daniel #1", "Ash Isle Vault - Daniel #2", "Ash Isle Vault - Daniel #3", "Ash Isle Vault - The Cooler Daniel #1", "Ash Isle Vault - The Cooler Daniel #2", "Ash Isle Vault - The Cooler Daniel #3", "Ash Isle Vault - The Cooler Daniel #4", "Ash Isle Vault - The Cooler Daniel #5", "Ash Isle Vault - Golden Rain #1", "Ash Isle Vault - Golden Rain #2", "Ash Isle Vault - Golden Rain #3", "Ash Isle Vault - Golden Rain #4", "Ash Isle Vault - Golden Rain #5", "Ash Isle Vault - Okay Listen, I'm Running Out of Good Names For These Treasure Pods, And They All Look The Same So Hopefully You Can Take This As My Apology #1", "Ash Isle Vault - Okay Listen, I'm Running Out of Good Names For These Treasure Pods, And They All Look The Same So Hopefully You Can Take This As My Apology #2", "Ash Isle Vault - Okay Listen, I'm Running Out of Good Names For These Treasure Pods, And They All Look The Same So Hopefully You Can Take This As My Apology #3", "Ash Isle Vault - The Council Member 1", "Ash Isle Vault - The Council Member 2", "Ash Isle Vault - The Council Member 3", "Ash Isle Vault - The Council Member 4", "Moss Blanket Vault - The Slime Central's Left-Hand Man", "Moss Blanket Vault - The Slime Central's Right-Hand Man", "Moss Blanket Vault - What's Left of the Riches #1", "Moss Blanket Vault - What's Left of the Riches #2", "Moss Blanket Vault - What's Right of the Riches #1", "Moss Blanket Vault - What's Right of the Riches #2", "Moss Blanket Vault - A Mountain of Gold #1", "Moss Blanket Vault - A Mountain of Gold #2", "Moss Blanket Vault - A Mountain of Gold #3", "Moss Blanket Vault - A Mountain of Gold #4", "Moss Blanket Vault - A Mountain of Gold #5"],
		"The Slime Sea": ["The Slime Sea - In Between a Rock and an Island", "The Mustache Shrine - Mustache Stache Cache", "The Slime Sea - On the Giant Tree Stump"],
		"Indigo Quarry": ["Indigo Quarry - I Liked Her Laugh", "Indigo Quarry - Crystal Wind Chime", "Indigo Quarry - Peeping Puddle Slimes", "Indigo Quarry - Map Data Node", "Indigo Quarry - Skate Fast Eat Grass", "Indigo Quarry - Coral Tube Treasure", "Indigo Quarry - The Boom Zone", "Indigo Quarry - Above the Smoke and Ashes", "Indigo Quarry - Personal Puddle Pod", "Indigo Quarry - Hidden Behind Stalagtmites", "Indigo Quarry - On a Cliff Before Puddle Lake", "Indigo Quarry - Across Hexium Crystal Formations", "Indigo Quarry - Ashore Near Puddle Lake", "Indigo Quarry - Under a Hexium Crystal", "Indigo Quarry - Under Crumbled Scaffolding", "Indigo Quarry - Slightly Irradiated Reward", "Indigo Quarry - Through the Radiation Cave", "Indigo Quarry - Crystal Cache behind Rickety Bridges", "Ash Isles - Looking to the Stars", "Ash Isles - Atop a Firey Perch", "Ash Isles - The Edge of the World", "Ash Isles - Blooming from Fire Flowers", "Indigo Quarry - Treasure After the End", "Indigo Quarry - Follow the Ravine"],
		"Moss Blanket": ["Moss Blanket - New Ancient Jungle", "Moss Blanket - MOSS BLANKET STUCK", "Moss Blanket - Map Data Node", "Moss Blanket - Surrounded by Mushrooms", "Moss Blanket - Flowery Dead End", "Moss Blanket - Above the Hungry Hungry Largos", "Moss Blanket - In the Honey Heaven", "Moss Blanket - The Cupboard under the Stairs", "Moss Blanket - Under the Log River", "Moss Blanket - Behind a Lonely Mountain", "Moss Blanket - In the Roots of a Huge Tree", "Moss Blanket - Overlooking the Tiny Pond", "Moss Blanket - Under the Log Bridge", "Moss Blanket - Fairy Circle Treasure", "Moss Blanket - Not Quite Hidden", "Moss Blanket - Can't Recommend Love Enough", "Moss Blanket - Just Under a Ledge", "Moss Blanket - At the Bottom of a Sheer Wall", "Moss Blanket - Sunken Treasure", "Moss Blanket - Off the Unbeaten Path", "Moss Blanket - Peepers Peeled!", "Moss Blanket - Very, Very, Very Tall Tree", "Moss Blanket - The Lost Archipelago", "Moss Blanket - The 'Missed the Jump' Crevice"],
		"Ancient Ruins": ["Ancient Ruins Transition - Slime Buddy", "Ancient Ruins - These Folks Like Slimes", "Ancient Ruins - You Gotta Choose a Path", "Ancient Ruins - Ice-Cold Lemonade", "Ancient Ruins - Map Data Node", "Ancient Ruins - Tree Memorial", "Ancient Ruins - A Flowery Respite", "Ancient Ruins - Hidden Nook", "Ancient Ruins - The Hidden Turnabout", "Ancient Ruins - Caught Up in the Explosion", "Ancient Ruins - The End of a Long and Arduous Journey", "Ancient Ruins - In a Crumbled Pile", "Ancient Ruins - At the End of a Broken Pillar Path", "Ancient Ruins - Everything Quiet on the Western Front", "Ancient Ruins - Above the Ancient Teleporter", "Ancient Ruins - There's Slimes in the Walls", "Ancient Ruins - Collapsed Upper Staircase", "Ancient Ruins - The Room With No Door", "Ancient Ruins - Shrine Overlooking the Ancient Ruins", "Ancient Ruins - Hidden Nook on a High Up Platform", "Ancient Ruins - Follow the Sunken Pillars", "Ancient Ruins - Truly Untamed Country"],
		"Glass Desert": ["Glass Desert - You'll Risk Burning Your Tuchus!", "Glass Desert - Life Waiting to Flow", "Glass Desert - Map Data Node", "Glass Desert - Buried Among Rubble", "Glass Desert - Behind a False Wall", "Glass Desert - Atop the Pillar before a Chasm", "Glass Desert - Hidden in the Rafters", "Glass Desert - Slime Statue Offering", "Glass Desert - At the Tippy Top of the Highest Mountain", "Glass Desert - Halfway up a Towering Tower", "Glass Desert - In a High-up Nook", "Glass Desert - Situated on a Collapsed Bridge", "Glass Desert - Painted Hen Stowaway Crate", "Glass Desert - Flames Burning at an Unperceivable Pace", "Glass Desert - Two Doors", "Glass Desert - She Stole a Piece of My Heart", "Glass Desert - Sold the Ranch", "Glass Desert - I Wasn't Ready", "Glass Desert - The Sand Sea", "Glass Desert - Down in a Hole", "Glass Desert - Just Around the Brick Wall", "Glass Desert - Dead-End Forgotten to the World", "Glass Desert - Under the Private Island", "Glass Desert - Hiding Behind a Sheer Mountain", "Glass Desert - Hover from One Tower to Another", "Glass Desert - Stupidly High Up", "Glass Desert - Ruined Wall On a Cliff", "Glass Desert - In a Supporting Pillar", "Glass Desert - Hidden at the Edge of the Sand Sea", "Glass Desert - At the Base of a Fire Glass Sculpture", "Glass Desert - The Highest Fountain", "Glass Desert - Lonely Pillar in the Sand Sea", "Glass Desert - On a Private Island", "Glass Desert - Overlooking Great Glass Pillars", "Glass Desert - Jagged Rock Formation in a Plateu"],
		"Viktor's Workshop": ["The Slimeulation - Under a Cliff Bordering The Simulated Sea", "The Slimeulation - Not Quite Rendered Arch", "The Slimeulation - Just Around the Corner", "The Slimeulation - Blocky Crevice Beside Moss Entrance", "The Slimeulation - Underwater in a Ravine", "The Slimeulation - Offshoot of a Hazardous Pathway", "The Slimeulation - Looking Over the Puddle Slimes", "The Slimeulation - Non-Rendered Cliff", "The Slimeulation - Platforming On Blocky Clouds", "The Slimeulation - Off The Rendered Path", "The Slimeulation - On Top Of The Simulated Winding Path", "The Slimeulation - In Between Muhsrooms and Rivers", "The Slimeulation - Right Across from the Exit"],
		"Mochi's Manor": ["Nimble Valley - In a Nook on Top of The Final Stretch Arch", "Nimble Valley - Bordering the Slime Sea", "Nimble Valley - Inside the Magneticore Pillar", "Nimble Valley - Floating Outcropping Above a Crevice", "Nimble Valley - Floating Above the Second Stretch", "Nimble Valley - Hidden in some Magneticore Ore", "Nimble Valley - Overlooking the Beginner Start"]
	}

	def __init__(self, multiworld: "MultiWorld", player: int):
		super().__init__(multiworld, player)
		self.location_count = 0

	def generate_early(self):
		check_options(self)
		options = self.options
		if hasattr(self.multiworld, "re_gen_passthrough"):
			if "Slime Rancher" not in self.multiworld.re_gen_passthrough: return
			passthrough = self.multiworld.re_gen_passthrough["Slime Rancher"]
			if "goal_type" in passthrough:
				options.goal_type = GoalType(passthrough["goal_type"])
			
			if "mail_count" in passthrough:
				options.mail_count = MailCount(passthrough["mail_count"])
			
			if "start_with_dry_reef" in passthrough:
				options.start_with_dry_reef = StartWithDryReef(passthrough["start_with_dry_reef"])
			
			if "enable_stylish_dlc_treasure_pods" in passthrough:
				options.enable_stylish_dlc_treasure_pods = EnableStylishDlcTreasurePods(passthrough["enable_stylish_dlc_treasure_pods"])
			
			if "treasure_cracker_checks" in passthrough:
				options.treasure_cracker_checks = TreasureCrackerChecks(passthrough["treasure_cracker_checks"])
			
			if "include_7z" in passthrough:
				options.include_7z = Include7z(passthrough["include_7z"])
			
			if "plortsanity" in passthrough:
				options.plortsanity = Plortsanity(passthrough["plortsanity"])
			
			if "fix_market_rates" in passthrough:
				options.fix_market_rates = FixMarketRates(passthrough["fix_market_rates"])
			
			if "start_with_drone" in passthrough:
				options.start_with_drone = StartWithDrone(passthrough["start_with_drone"])
			
			if "trap_percent" in passthrough:
				options.trap_percent = TrapPercent(passthrough["trap_percent"])
			
			if "include_ogden" in passthrough:
				options.include_ogden = IncludeOgden(passthrough["include_ogden"])
			
			if "include_mochi" in passthrough:
				options.include_mochi = IncludeMochi(passthrough["include_mochi"])
			
			if "include_viktor" in passthrough:
				options.include_viktor = IncludeViktor(passthrough["include_viktor"])
			
			if "postgame" in passthrough:
				options.postgame = Postgame(passthrough["postgame"])
			
			if "easy_skips" in passthrough:
				options.easy_skips = EasySkips(passthrough["easy_skips"])
			
			if "precise_movement" in passthrough:
				options.precise_movement = PreciseMovement(passthrough["precise_movement"])
			
			if "dangerous_skips" in passthrough:
				options.dangerous_skips = DangerousSkips(passthrough["dangerous_skips"])
			
			if "obscure_locations" in passthrough:
				options.obscure_locations = ObscureLocations(passthrough["obscure_locations"])
			
			if "largo_jumps" in passthrough:
				options.largo_jumps = LargoJumps(passthrough["largo_jumps"])
			
			if "jetpack_boosts" in passthrough:
				options.jetpack_boosts = JetpackBoosts(passthrough["jetpack_boosts"])
			
			if "market_logic" in passthrough:
				options.market_logic = MarketLogic(passthrough["market_logic"])
			
		if self.options.start_with_dry_reef:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: Dry Reef"))
		if self.options.start_with_drone:
		    self.multiworld.push_precollected(self.create_item("Drone"))
		if not self.options.include_ogden:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: Ogden's Retreat"))
		if not self.options.include_ogden:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: The Wilds"))
		if not self.options.include_mochi:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: Mochi's Manor"))
		if not self.options.include_mochi:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: Nimble Valley"))
		if not self.options.include_viktor:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: Viktor's Workshop"))
		if not self.options.include_viktor:
		    self.multiworld.push_precollected(self.create_item("Region Unlock: The Slimeulations"))

	def create_regions(self):
		gen_create_regions(self)

	def create_item(self, name: str):
		return Item(name, item_table[name], self.item_name_to_id[name], self.player)

	def create_items(self):
		gen_create_items(self)

	def set_rules(self):
		player = self.player
		options = self.options
		match self.options.goal_type:
			case 0:
				self.multiworld.completion_condition[self.player] = lambda state: has_amount(state, player, options, "Note Read", 30)
			case 1:
				self.multiworld.completion_condition[self.player] = lambda state: has_amount(state, player, options, "7Zee Bought", len(corporate_locations))
			case 2:
				self.multiworld.completion_condition[self.player] = lambda state: has_all(state, player, options, credits_unlocks)
			case 3:
				self.multiworld.completion_condition[self.player] = lambda state: has_amount(state, player, options, "Casey's Letter", options.mail_count)
		

	def fill_slot_data(self):
		characters = [char for char in f"{self.multiworld.seed}{self.player_name}"]
		self.random.shuffle(characters)
		shuffled = f"ap_uuid_{''.join(characters).replace(" ", "_")}"
		slot_data = {
			"goal_type": int(self.options.goal_type),
			"mail_count": int(self.options.mail_count),
			"start_with_dry_reef": bool(self.options.start_with_dry_reef),
			"enable_stylish_dlc_treasure_pods": bool(self.options.enable_stylish_dlc_treasure_pods),
			"treasure_cracker_checks": int(self.options.treasure_cracker_checks),
			"include_7z": bool(self.options.include_7z),
			"plortsanity": int(self.options.plortsanity),
			"fix_market_rates": bool(self.options.fix_market_rates),
			"start_with_drone": bool(self.options.start_with_drone),
			"trap_percent": int(self.options.trap_percent),
			"include_ogden": bool(self.options.include_ogden),
			"include_mochi": bool(self.options.include_mochi),
			"include_viktor": bool(self.options.include_viktor),
			"postgame": bool(self.options.postgame),
			"easy_skips": bool(self.options.easy_skips),
			"precise_movement": bool(self.options.precise_movement),
			"dangerous_skips": bool(self.options.dangerous_skips),
			"obscure_locations": bool(self.options.obscure_locations),
			"largo_jumps": bool(self.options.largo_jumps),
			"jetpack_boosts": bool(self.options.jetpack_boosts),
			"market_logic": bool(self.options.market_logic),
			"uuid": str(shuffled)
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