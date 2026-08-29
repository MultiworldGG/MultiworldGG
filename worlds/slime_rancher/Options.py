from dataclasses import dataclass
from Options import *
from .Locations import *

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class GoalType(Choice):
	"""
	What criteria to goal
	notes = read all notes
	7Zee = buy all 7Zee ranks
	credits = get to the end credits
	mail = mcguffin hunt, Casey's Letters 
	"""
	display_name = "Goal Type"
	option_notes = 0
	option_7Zee = 1
	option_credits = 2
	option_mail = 3
	default = 0


class MailCount(Range):
	"""
	How many Casey's Letters to add to the pool for mcguffin hunt
	8-20
	"""
	display_name = "Mail Count"
	range_start = 8
	range_end = 20
	default = 8


class StartWithDryReef(DefaultOnToggle):
	"""
	Start with the Dry Reef unlocked
	"""
	display_name = "Start With Dry Reef"


class EnableStylishDlcTreasurePods(Toggle):
	"""
	Whether the Secret Style DLC Treasure Pods are locations in the pool.
	
	This will add approximately 17 checks
	
	note: THIS WILL NOT GIVE YOU DLC\nYOU MUST __***OWN***__ THE DLC
	"""
	display_name = "Enable Stylish Dlc Treasure Pods"


class TreasureCrackerChecks(Range):
	"""
	which levels of the treasure cracker is considered as checks
	default: level 1
	level 1 requires crafting 1 gadget
	level 2 requires crafting 20 gadgets
	level 3 requires crafting 50 gadgets
	"""
	display_name = "Treasure Cracker Checks"
	range_start = 0
	range_end = 3
	default = 1


class Include7z(Toggle):
	"""
	Include unlockables behind 7z as checks
	estimated to appear in sphere 2 and above
	
	This will add 54 checks
	"""
	display_name = "Include 7z"


class Plortsanity(Choice):
	"""
	Selling a plort for the first time will send a check
	
	This will add approximately 16 checks
	"""
	display_name = "Plortsanity"
	option_off = 0
	option_all_except_gold = 1
	option_all = 2
	default = 1


class FixMarketRates(DefaultOnToggle):
	"""
	Overrides the default market behavior:
	instead of https://slimerancher.fandom.com/wiki/Plort_Market_(Slime_Rancher)
	it will make all plort prices 150% base value, base value listed in the above link
	"""
	display_name = "Fix Market Rates"


class StartWithDrone(DefaultOnToggle):
	"""
	Start with a Drone
	"""
	display_name = "Start With Drone"


class TrapPercent(Range):
	"""
	what percent of filler should be replaced with traps
	"""
	display_name = "Trap Percent"
	range_start = 0
	range_end = 100
	default = 15


class IncludeOgden(Toggle):
	"""
	Include Ogden's Retreat
	
	This will add 10 checks
	"""
	display_name = "Include Ogden"


class IncludeMochi(Toggle):
	"""
	Include Mochi's Manor
	
	This will add 7 checks
	"""
	display_name = "Include Mochi"


class IncludeViktor(Toggle):
	"""
	Include Viktor's Workshop
	
	This will add 13 checks
	"""
	display_name = "Include Viktor"


class Postgame(Toggle):
	"""
	Include Post-Credit Locations, i.e. Item Vaults
	
	This will add 42 checks
	"""
	display_name = "Postgame"


class EasySkips(Toggle):
	"""
	Enable Skips that many new players end up finding on their first playthrough
	"""
	display_name = "Easy Skips"


class PreciseMovement(Toggle):
	"""
	Enable Skips that require tighter movement than average
	"""
	display_name = "Precise Movement"


class DangerousSkips(Toggle):
	"""
	Enable Skips that have a high chance of taking damage or getting killed
	"""
	display_name = "Dangerous Skips"


class ObscureLocations(Toggle):
	"""
	Enable Skips that abuse the terrain, usually in unintuitive ways
	"""
	display_name = "Obscure Locations"


class LargoJumps(Toggle):
	"""
	Enable Skips where you jump off a largo midair
	"""
	display_name = "Largo Jumps"


class JetpackBoosts(Toggle):
	"""
	Enable Skips where you use the ability to get rid of jetpack's startup times through careful jumping, allowing for more energy conservation
	"""
	display_name = "Jetpack Boosts"


class MarketLogic(Toggle):
	"""
	Enable Logic tied to early trading when opening slime gates
	"""
	display_name = "Market Logic"


@dataclass
class SlimeRancherOptions(PerGameCommonOptions):
	goal_type: GoalType
	mail_count: MailCount
	start_with_dry_reef: StartWithDryReef
	enable_stylish_dlc_treasure_pods: EnableStylishDlcTreasurePods
	treasure_cracker_checks: TreasureCrackerChecks
	include_7z: Include7z
	plortsanity: Plortsanity
	fix_market_rates: FixMarketRates
	start_with_drone: StartWithDrone
	trap_percent: TrapPercent
	include_ogden: IncludeOgden
	include_mochi: IncludeMochi
	include_viktor: IncludeViktor
	postgame: Postgame
	easy_skips: EasySkips
	precise_movement: PreciseMovement
	dangerous_skips: DangerousSkips
	obscure_locations: ObscureLocations
	largo_jumps: LargoJumps
	jetpack_boosts: JetpackBoosts
	market_logic: MarketLogic

	def get_options_map(self, option):
		match option:
			case "goal_type":
				return self.goal_type
			case "mail_count":
				return self.mail_count
			case "start_with_dry_reef":
				return self.start_with_dry_reef
			case "enable_stylish_dlc_treasure_pods":
				return self.enable_stylish_dlc_treasure_pods
			case "treasure_cracker_checks":
				return self.treasure_cracker_checks
			case "include_7z":
				return self.include_7z
			case "plortsanity":
				return self.plortsanity
			case "fix_market_rates":
				return self.fix_market_rates
			case "start_with_drone":
				return self.start_with_drone
			case "trap_percent":
				return self.trap_percent
			case "include_ogden":
				return self.include_ogden
			case "include_mochi":
				return self.include_mochi
			case "include_viktor":
				return self.include_viktor
			case "postgame":
				return self.postgame
			case "easy_skips":
				return self.easy_skips
			case "precise_movement":
				return self.precise_movement
			case "dangerous_skips":
				return self.dangerous_skips
			case "obscure_locations":
				return self.obscure_locations
			case "largo_jumps":
				return self.largo_jumps
			case "jetpack_boosts":
				return self.jetpack_boosts
			case "market_logic":
				return self.market_logic
		

def check_options(world):
	options = world.options
	random = world.random
	settings = world.settings
	if options.goal_type == 1 and not options.include_7z:
	    raise_yaml_error(world.player, "7Zee goal type requires you to include 7Zee locations")
	if options.accessibility == Accessibility.option_minimal:
	    print("Slime Rancher doesn't support accessibility minimal, defaulting accessibility to full")
	    options.accessibility = Accessibility(Accessibility.option_full)

def raise_yaml_error(player_name, error):
	raise OptionError(f'\n\n=== Slime Rancher YAML ERROR ===\nSlime Rancher: {player_name} {error}, PLEASE FIX YOUR YAML\n\n')