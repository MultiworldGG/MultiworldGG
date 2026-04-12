from dataclasses import dataclass
from Options import *
from .Locations import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class GoalRequirement(Choice):
	"""
	0 = Stage hunt (beat/loop all stages)
	1 = Kill Director (required ~75% of stages beaten)
	"""
	display_name = "Goal Requirement"
	option_stage_hunt = 0
	option_director = 1
	default = 0


class ChestChecksPerStage(Range):
	"""
	how many chest checks per stage
	from 5 to 10
	default: 7
	"""
	display_name = "Chest Checks Per Stage"
	range_start = 5
	range_end = 10
	default = 7


class EggInclusion(Choice):
	"""
	how to include eggs:
	0 = fully disabled
	1 = locked behind an item
	2 = fully unlocked
	"""
	display_name = "Egg Inclusion"
	option_disabled = 0
	option_locked_behind_item = 1
	option_unlocked = 2
	default = 1


class LockHyperBehindItem(Toggle):
	"""
	Lock the `Hyper` gamemode behind an item
	"""
	display_name = "Lock Hyper Behind Item"


class LockHurryBehindItem(Toggle):
	"""
	Lock the `Hurry` gamemode behind an item
	This will lock `Beat with [character]` and `[stage] beaten` checks until hurry is found
	"""
	display_name = "Lock Hurry Behind Item"


class LockArcanasBehindItem(Toggle):
	"""
	Lock the `Arcanas` gamemode behind an item
	"""
	display_name = "Lock Arcanas Behind Item"


class Enemysanity(Toggle):
	"""
	The first kill of an enemy is a check
	"""
	display_name = "Enemysanity"


class EnemysanityArcanaEnemies(Toggle):
	"""
	Allows Arcana specific enemies to be checks for enemysanity
	"""
	display_name = "Enemysanity Arcana Enemies"


class CharacterPoolSize(Range):
	"""
	Limit the amount of characters (select a random assortment of characters if higher)
	"""
	display_name = "Character Pool Size"
	range_start = 0
	range_end = 999
	default = 0


class StagePoolSize(Range):
	"""
	Limit the amount of stages (select a random assortment of stages if higher)
	"""
	display_name = "Stage Pool Size"
	range_start = 0
	range_end = 999
	default = 0


class AllowSecretCharacters(DefaultOnToggle):
	"""
	Allow the use of secret characters:
	[Exdash, Toastie, Smith IV, Random, Marrabbio, Avatar, Minnah, Leda, Cosmo, Trouser, Gains, Gyorunton, Red Death, Bats, Rose, Scorej-Oni, Gyoruntin, Young Maria, Familiar, Innocent, Cornell, Ferryman, Master Librarian, Hammer, Wind, Jonathan & Charlotte, Charlotte & Jonathan, Stella & Loretta, Loretta & Stella, Stella, Loretta, Brauner, Soleil, Dario, Dmitrii, Celia, Graham, Joachim, Walter, Carmilla, Olrox, Cave Troll, Axe Armor, Frozenshade, Succubus, Keremet, Sniper, Blackmore, Malphas, Death, Galamoth, Lolo, Hiss, Meow, and Purr, Kina, Imakoo, Door]
	"""
	display_name = "Allow Secret Characters"


class AllowMegaloCharacters(Toggle):
	"""
	Allow the use of megalo characters:
	[Megalo Syuuto, Je-Ne-Viv, Megalo Impostor, Megalo Elizabeth, Megalo Olrox, Megalo Dracula]
	"""
	display_name = "Allow Megalo Characters"


class AllowUnfairCharacters(Toggle):
	"""
	Allow the use of unfair characters:
	[Peppino, MissingN▯, Space Dette, Megalo Menya, Ghost, Fleaman, Megalo Death, Chaos]
	"""
	display_name = "Allow Unfair Characters"


class IncludedBaseCharacters(OptionSet):
	"""
	Base Characters to be randomized
	possible options:
	[Antonio Belpaese, Imelda Belpaese, Pasqualina Belpaese, Gennaro Belpaese, Arca Ladonna, Porta Ladonna, Lama Ladonna, Poe Ratcho, Suor Clerici, Dommario, Krochi Freetto, Christine Davain, Pugnala Provola, Giovanna Grana, Poppea Pecorina, Concetta Caciotta, Mortaccio, Yatta Cavallo, Bianca Ramba, O'Sole Meeo, Sir Ambrojoe, Iguana Gallo Valletto, Divano Thelma, Zi'Assunta Belpaese, Exdash Exiviiq, Toastie, Smith IV, Random, Boon Marrabbio, Avatar Infernas, Minnah Mannarah, Leda, Cosmo Pavone, Peppino, Big Trouser, missingN, Gains Boros, Gyorunton, Mask of the Red Death, Queen Sigma, Bat Robbert, Zi'Appunta Belpaese, She-Moon Eeta, Santa Ladonna, Gazebo, Chula-Reh, Space Dude, Bats Bats Bats, Rose De Infernas, Torino, Scorej-Oni, Gyoruntin, Secretino, Space Dette]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Base Characters"
	valid_keys = frozenset([*base_characters, "All", "Random"])
	default = frozenset(["All"])


class IncludedMoonspellCharacters(OptionSet):
	"""
	Moonspell Characters to be randomized
	possible options:
	[Miang Moonspell, Menya Moonspell, Syuuto Moonspell, Babi-Onna, McCoy-Oni, Megalo Menya Moonspell, Megalo Syuuto Moonspell, Gab'Et-Oni]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Moonspell Characters"
	valid_keys = frozenset([*moonspell_characters, "All", "Random"])
	default = frozenset([])


class IncludedFoscariCharacters(OptionSet):
	"""
	Foscari Characters to be randomized
	possible options:
	[Eleanor Uziron, Maruto Cuts, Keitha Muort, Luminaire Foscari, Genevieve Gruyère, Je-Ne-Viv, Sammy, Rottin'Ghoul]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Foscari Characters"
	valid_keys = frozenset([*foscari_characters, "All", "Random"])
	default = frozenset([])


class IncludedAmongusCharacters(OptionSet):
	"""
	Amongus Characters to be randomized
	possible options:
	[Crewmate Dino, Engineer Gino, Ghost Lino, Shapeshifter Nino, Guardian Pina, Impostor Rina, Scientist Mina, Horse, Megalo Impostor Rina]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Amongus Characters"
	valid_keys = frozenset([*amongus_characters, "All", "Random"])
	default = frozenset([])


class IncludedOperationGunsCharacters(OptionSet):
	"""
	Operation Guns Characters to be randomized
	possible options:
	[Bill Rizer, Lance Bean, Ariana, Lucia Zero, Brad Fang, Browny, Sheena Etranzi, Probotector, Stanley, Newt Plissken, Colonel Bahamut, Simondo]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Operation Guns Characters"
	valid_keys = frozenset([*operation_guns_characters, "All", "Random"])
	default = frozenset([])


class IncludedCastlevaniaCharacters(OptionSet):
	"""
	Castlevania Characters to be randomized
	possible options:
	[Leon Belmont, Sonia Belmont, Trevor Belmont, Christopher Belmont, Simon Belmont, Juste Belmont, Richter Belmont, Julius Belmont, Grant Danasty, Quincy Morris, John Morris, Jonathan Morris, Maxim Kischine, Henry, Soma Cruz, Vlad Tepes Dracula, Charlotte Aulin, Sypha Belnades, Julia Laforeze, Carrie Fernandez, Yoko Belnades, Rinaldo Gandolfi, Mina Hakuba, Elizabeth Bartley, Alucard, Reinhardt Schneider, Eric Lecarde, Isaac, Hector, Sara Trantoul, Vincent Dorin, Maria Renard, Shanoa, Albus, Lisa, Shaft, Saint Germain, Nathan Graves, Cornell, Barlowe, Young Maria Renard, Familiar, Innocent Devil, Blue Crescent Moon Cornell, Ferryman, Librarian, Hammer, Wind, Hugh Baldwin, Morris Baldwin, Annette, Tera, Jonathan & Charlotte, Charlotte & Jonathan, Stella & Loretta Lecarde, Loretta & Stella Lecarde, Stella Lecarde, Loretta Lecarde, Brauner, Soleil Belmont, Dario Bossi, Dmitri Blinov, Celia Fortner, Graham Jones, Joachim, Walter, Carmilla, Cave Troll, Fleaman, Axe Armor, Frozenshade, Amalaric Sniper, Stone Skull, Sword Ruler, Persephone, Keremet, Astarte, Drolta, Actrise, Atlantis Shrine Wizard, Succubus, Fake Trio, Slogra and Gaibon, Zephyr, Jiangshi, Blackmore, Count Olrox, Malphas, Death, Galamoth, Megalo Elizabeth Bartley, Megalo Olrox, Megalo Death, Megalo Dracula, Chaos, Gaibon and Slogra, Slogra, Kid Dracula, Aeon, Desmond Belmont, Dolores Belmont, Zoe Belmont, Fishman, Fake Trevor, Fake Sypha, Fake Grant, Genya Arikado]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Castlevania Characters"
	valid_keys = frozenset([*castlevania_characters, "All", "Random"])
	default = frozenset([])


class IncludedEmeraldCharacters(OptionSet):
	"""
	Emerald Characters to be randomized
	possible options:
	[Tsunanori Mido, Bonnie Blair, Formina Franklyn, Diva No. 5, Ameya Aisling, Siugnas, Final Emperor, Dolores, Macha, Lita, Kugutsu, Mr. S, Lolo, Hiss, Meow and Purr, Kina, Imakoo, Malevolent Door Spirit]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Emerald Characters"
	valid_keys = frozenset([*emerald_characters, "All", "Random"])
	default = frozenset([])


class IncludedBalatroCharacters(OptionSet):
	"""
	Balatro Characters to be randomized
	possible options:
	[Jimbo, Canio, Chicot, Perkeo]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Balatro Characters"
	valid_keys = frozenset([*balatro_characters, "All", "Random"])
	default = frozenset([])


class IncludedNormalStages(OptionSet):
	"""
	Normal Stages to be randomized
	possible options:
	[Mad Forest, Inlaid Library, Dairy Plant, Gallo Tower, Cappella Magna, Westwoods, Mazerella]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Normal Stages"
	valid_keys = frozenset([*normal_stages, "All", "Random"])
	default = frozenset(["All"])


class IncludedBonusStages(OptionSet):
	"""
	Bonus Stages to be randomized
	possible options:
	[Il Molise, Moongolow, Whiteout, The Coop, Space 54, Carlo Cart]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Bonus Stages"
	valid_keys = frozenset([*bonus_stages, "All", "Random"])
	default = frozenset([])


class IncludedChallengeStages(OptionSet):
	"""
	Challenge Stages to be randomized
	possible options:
	[Eudaimonia M., Green Acres, The Bone Zone, Boss Rash, Laborratory, Bat Country, Astral Stair, Tiny Bridge, Room 1665]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Challenge Stages"
	valid_keys = frozenset([*challenge_stages, "All", "Random"])
	default = frozenset([])


class IncludedMoonspellStages(OptionSet):
	"""
	Moonspell Stages to be randomized
	possible options:
	[Mt.Moonspell]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Moonspell Stages"
	valid_keys = frozenset([*moonspell_stages, "All", "Random"])
	default = frozenset([])


class IncludedFoscariStages(OptionSet):
	"""
	Foscari Stages to be randomized
	possible options:
	[Lake Foscari, Abyss Foscari]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Foscari Stages"
	valid_keys = frozenset([*foscari_stages, "All", "Random"])
	default = frozenset([])


class IncludedAmongusStages(OptionSet):
	"""
	Amongus Stages to be randomized
	possible options:
	[Polus Replica]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Amongus Stages"
	valid_keys = frozenset([*amongus_stages, "All", "Random"])
	default = frozenset([])


class IncludedOperationGunsStages(OptionSet):
	"""
	Operation Guns Stages to be randomized
	possible options:
	[Neo Galuga, Hectic Highway]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Operation Guns Stages"
	valid_keys = frozenset([*operation_guns_stages, "All", "Random"])
	default = frozenset([])


class IncludedCastlevaniaStages(OptionSet):
	"""
	Castlevania Stages to be randomized
	possible options:
	[Ode to Castlevania]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Castlevania Stages"
	valid_keys = frozenset([*castlevania_stages, "All", "Random"])
	default = frozenset([])


class IncludedEmeraldStages(OptionSet):
	"""
	Emerald Stages to be randomized
	possible options:
	[Emerald Diorama]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Emerald Stages"
	valid_keys = frozenset([*emerald_stages, "All", "Random"])
	default = frozenset([])


class IncludedBalatroStages(OptionSet):
	"""
	Balatro Stages to be randomized
	possible options:
	[Ante Chamber]
	"All" - adds all locations above
	"Random" - picks a random # of characters b/t list's max size / 2 and list's max size
	"""
	display_name = "Included Balatro Stages"
	valid_keys = frozenset([*balatro_stages, "All", "Random"])
	default = frozenset([])


@dataclass
class VampireSurvivorsOptions(PerGameCommonOptions):
	goal_requirement: GoalRequirement
	chest_checks_per_stage: ChestChecksPerStage
	egg_inclusion: EggInclusion
	lock_hyper_behind_item: LockHyperBehindItem
	lock_hurry_behind_item: LockHurryBehindItem
	lock_arcanas_behind_item: LockArcanasBehindItem
	enemysanity: Enemysanity
	enemysanity_arcana_enemies: EnemysanityArcanaEnemies
	character_pool_size: CharacterPoolSize
	stage_pool_size: StagePoolSize
	allow_secret_characters: AllowSecretCharacters
	allow_megalo_characters: AllowMegaloCharacters
	allow_unfair_characters: AllowUnfairCharacters
	included_base_characters: IncludedBaseCharacters
	included_moonspell_characters: IncludedMoonspellCharacters
	included_foscari_characters: IncludedFoscariCharacters
	included_amongus_characters: IncludedAmongusCharacters
	included_operation_guns_characters: IncludedOperationGunsCharacters
	included_castlevania_characters: IncludedCastlevaniaCharacters
	included_emerald_characters: IncludedEmeraldCharacters
	included_balatro_characters: IncludedBalatroCharacters
	included_normal_stages: IncludedNormalStages
	included_bonus_stages: IncludedBonusStages
	included_challenge_stages: IncludedChallengeStages
	included_moonspell_stages: IncludedMoonspellStages
	included_foscari_stages: IncludedFoscariStages
	included_amongus_stages: IncludedAmongusStages
	included_operation_guns_stages: IncludedOperationGunsStages
	included_castlevania_stages: IncludedCastlevaniaStages
	included_emerald_stages: IncludedEmeraldStages
	included_balatro_stages: IncludedBalatroStages

	def flatten_locations(self, world, list, self_list):
		if "Random" in self_list:
			return world.random.sample(list, world.random.randint(int(len(list) / 2), len(list)))
		else:
			return list if "All" in self_list else [loc for loc in self_list if loc != "Random"]

	def get_included_characters(self, world):
		return (self.flatten_locations(world, base_characters, self.included_base_characters) + self.flatten_locations(world, moonspell_characters, self.included_moonspell_characters) + self.flatten_locations(world, foscari_characters, self.included_foscari_characters) + self.flatten_locations(world, amongus_characters, self.included_amongus_characters) + self.flatten_locations(world, operation_guns_characters, self.included_operation_guns_characters) + self.flatten_locations(world, castlevania_characters, self.included_castlevania_characters) + self.flatten_locations(world, emerald_characters, self.included_emerald_characters) + self.flatten_locations(world, balatro_characters, self.included_balatro_characters))

	def get_included_stages(self, world):
		return (self.flatten_locations(world, normal_stages, self.included_normal_stages) + self.flatten_locations(world, bonus_stages, self.included_bonus_stages) + self.flatten_locations(world, challenge_stages, self.included_challenge_stages) + self.flatten_locations(world, moonspell_stages, self.included_moonspell_stages) + self.flatten_locations(world, foscari_stages, self.included_foscari_stages) + self.flatten_locations(world, amongus_stages, self.included_amongus_stages) + self.flatten_locations(world, operation_guns_stages, self.included_operation_guns_stages) + self.flatten_locations(world, castlevania_stages, self.included_castlevania_stages) + self.flatten_locations(world, emerald_stages, self.included_emerald_stages) + self.flatten_locations(world, balatro_stages, self.included_balatro_stages))

	def get_options_map(self, option):
		match option:
			case "goal_requirement":
				return self.goal_requirement
			case "chest_checks_per_stage":
				return self.chest_checks_per_stage
			case "egg_inclusion":
				return self.egg_inclusion
			case "lock_hyper_behind_item":
				return self.lock_hyper_behind_item
			case "lock_hurry_behind_item":
				return self.lock_hurry_behind_item
			case "lock_arcanas_behind_item":
				return self.lock_arcanas_behind_item
			case "enemysanity":
				return self.enemysanity
			case "enemysanity_arcana_enemies":
				return self.enemysanity_arcana_enemies
			case "character_pool_size":
				return self.character_pool_size
			case "stage_pool_size":
				return self.stage_pool_size
			case "allow_secret_characters":
				return self.allow_secret_characters
			case "allow_megalo_characters":
				return self.allow_megalo_characters
			case "allow_unfair_characters":
				return self.allow_unfair_characters
			case "included_base_characters":
				return self.included_base_characters
			case "included_moonspell_characters":
				return self.included_moonspell_characters
			case "included_foscari_characters":
				return self.included_foscari_characters
			case "included_amongus_characters":
				return self.included_amongus_characters
			case "included_operation_guns_characters":
				return self.included_operation_guns_characters
			case "included_castlevania_characters":
				return self.included_castlevania_characters
			case "included_emerald_characters":
				return self.included_emerald_characters
			case "included_balatro_characters":
				return self.included_balatro_characters
			case "included_normal_stages":
				return self.included_normal_stages
			case "included_bonus_stages":
				return self.included_bonus_stages
			case "included_challenge_stages":
				return self.included_challenge_stages
			case "included_moonspell_stages":
				return self.included_moonspell_stages
			case "included_foscari_stages":
				return self.included_foscari_stages
			case "included_amongus_stages":
				return self.included_amongus_stages
			case "included_operation_guns_stages":
				return self.included_operation_guns_stages
			case "included_castlevania_stages":
				return self.included_castlevania_stages
			case "included_emerald_stages":
				return self.included_emerald_stages
			case "included_balatro_stages":
				return self.included_balatro_stages
		

def check_options(world):
	options = world.options
	random = world.random
	settings = world.settings
	characters = options.get_included_characters(world)
	stages = options.get_included_stages(world)
	
	if not options.allow_secret_characters:
	    characters = [character for character in characters if character not in secret_characters]
	
	if not options.allow_megalo_characters:
	    characters = [character for character in characters if character not in megalo_characters]
	
	if not settings.allow_unfair_characters and options.allow_unfair_characters:
	    options.allow_unfair_characters = AllowUnfairCharacters(False)
	    raise_yaml_error(world.player_name,
	                     "`allow_unfair_characters` can not be enabled unless the host,yaml setting 'allow_unfair_characters' is also enabled")
	
	if not options.allow_unfair_characters:
	    characters = [character for character in characters if character not in unfair_characters]
	
	if len(stages) == 0:
	    raise_yaml_error(world.player_name, "You must have more than 0 stages included")
	
	if len(characters) == 0:
	    raise_yaml_error(world.player_name, "You must have more than 0 eligible characters included")
	
	if len(stages) > options.stage_pool_size > 0:
	    stages = random.sample(stages, options.stage_pool_size)
	    
	if len(characters) > options.character_pool_size > 0:
	    characters = random.sample(characters, options.character_pool_size)
	
	if EUDAI not in stages and options.goal_requirement == 1:
	    stages.append(EUDAI)
	
	if len(stages) == 1 and stages[0] == EUDAI:
	    raise_yaml_error(world.player_name, f"{EUDAI} CAN NOT BE YOUR ONLY STAGE")
	
	random.shuffle(characters)
	random.shuffle(stages)
	world.final_included_characters_list = characters
	world.final_included_stages_list = stages
	
	if world.options.goal_requirement == 1:
	  if world.ending_stage_count == 0:
		   world.ending_stage_count = int(len(world.final_included_stages_list) * .75)

def raise_yaml_error(player_name, error):
	raise OptionError(f'\n\n=== Vampire Survivors YAML ERROR ===\nVampire Survivors: {player_name} {error}, PLEASE FIX YOUR YAML\n\n')