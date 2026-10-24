from dataclasses import dataclass
from Options import Toggle, DeathLink, Range, Choice, PerGameCommonOptions, FreeText, OptionGroup

# Goal Options

class Goal(Choice):
    """
    Trophy Mode: To win, the player needs to collect one trophy apparatus from each moon (11 with no custom moons).

    Collectathon: A new rare scrap is added, called the Archipelago Chest. To win, the player must collect a certain 
    amount of them as well as a selection of random scrap

    Credit Hunt: To win, the player needs to receive a specific amount of company credit items from the multiworld.
    """
    display_name = "Game Mode"
    option_trophy = 0
    option_collectathon = 1
    option_credit_hunt = 2
    default = 0
    slot = True
    slot_name = "goal"


class CollectathonScrapGoal(Range):
    """
    The number of collectathon scrap you need to complete the collectathon goal
    """
    display_name = "Collectathon Scrap Goal"
    range_start = 3
    range_end = 99
    default = 10
    slot = True
    slot_name = "collectathonGoal"


class CollectathonRandomScrap(Range):
    """
    Collectathon mode:
    The number of random scrap required in addition to the main collectathon scrap
    """
    display_name = "Collectathon Random Scrap"
    range_start = 0
    range_end = 20 # len(data["scrap"])
    default = 5


class CreditReplacement(Range):
    """
    Credit Hunt mode:
    Replaces the specified percent of filler items with company credits
    """
    display_name = "Credit Replacement"
    range_start = 5
    range_end = 80
    default = 50


class RequiredCredits(Range):
    """
    Credit Hunt mode:
    The percent of company credits in the pool that are required to beat the game. If there are 20 credits in the pool
    and the player sets this to 75, then once 75% of the 20 credits, or 15 credits, are collected, they will win
    """
    display_name = "Required Credits"
    range_start = 10
    range_end = 100
    default = 75


# Location Options

class GradeLocationsPerMoon(Range):
    """
    The total number of grade locations generated for each moon. A grade location is completed by collecting enough 
    scrap in one day to obtain the minimum required grade on a moon.
    """
    display_name = "Grade Locations Per Moon"
    range_start = 1
    range_end = 10
    default = 3
    slot = True
    slot_name = "gradeLocationsPerMoon"


class NumQuotas(Range):
    """
    The number of quota locations to create. A quota location is completed whenever the player fulfills
    money_per_quota_location-worth of quota. Progress accumulates over quotas and crew wipes.

    Ex: If money_per_quota_location = 70 and the first quota is 120, then 1 quota location will be completed when the 
        player fulfills their first quota. If the second quota is 200, then 3 additional quota locations will be 
        completed when the player fulfills their second quota. 320 total quota has been fulfilled at this point, so a
        total of 4 quota locations are complete.
    """
    display_name = "Num Quotas"
    range_start = 0
    range_end = 50
    default = 15
    slot = True
    slot_name = "numQuota"


class QuotaCheckpointEvery(Range):
    """
    How many quota locations the player must complete between each checkpoint unlock event.
    With the default values (num_quotas=15 and quota_checkpoint_every=3), quota locations will be grouped into five
    spheres with three locations each. This helps ensure that important early items are not stuck behind late quota
    locations. Set higher than num_quotas to disable checkpoints entirely and group all quota locations into a single
    sphere.
    """
    display_name = "Quota Checkpoint Every"
    range_start = 1
    range_end = 20
    default = 3
    slot = False


class MoneyPerQuotaLocation(Range):
    """
    The total amount of quota a player must obtain to complete each quota location
    For example, if money per quota location is 500, you need to reach 500 total quota for each quota location
    """
    display_name = "Money Per Quota Location"
    range_start = 50
    range_end = 2000
    default = 400
    slot = True
    slot_name = "moneyPerQuotaLocation"


class Scrapsanity(Toggle):
    """
    Enables scrapsanity, which adds locations for collecting each scrap for the first time.
    Warning: adds >50 locations to the randomizer
    """
    display_name = "Scrapsanity"
    slot = True
    slot_name = "scrapsanity"


# Item Options

class RandomizeCompanyBuilding(Toggle):
    """
    Locks the company building behind an item in the multiworld, preventing the player from routing there to sell scrap until they receive 
    the required item
    """
    display_name = "Randomize Company Building"
    slot = True
    default = 0
    slot_name = "randomizecompany"


class RandomizeScanner(Toggle):
    """
    Locks the scanner behind an item in the multiworld, rendering the player unable to scan until they receive it
    """
    display_name = "Randomize Scanner"
    default = 0
    slot = True
    slot_name = "scanner"


class RandomizeTerminal(Toggle):
    """
    Locks the terminal behind an item in the multiworld, preventing its use until the player receive the item
    """
    display_name = "Randomize Terminal"
    slot = True
    default = 0
    slot_name = "randomizeterminal"


# Starting Options

class StartingMoon(FreeText):
    """
    This is the only moon the player will have access to at the start of a multiworld. All other moons are locked until 
    received.
    This can be set to any moon name, or 'randomize', which randomly selects a starting moon.
    """
    display_name = "Starting Moon"
    default = "randomize"
    slot = False


class StartingStaminaBars(Range):
    """
    The player begins with this many stamina bars, and the rest have to be unlocked.
    """
    display_name = "Starting Stamina Bars"
    range_start = 0
    range_end = 4
    default = 4
    slot = True
    slot_name = "staminaBars"


class StartingInventorySlots(Range):
    """
    The player begins with this many inventory slots, and the rest have to be unlocked.
    """
    display_name = "Starting Inventory Slots"
    range_start = 1
    range_end = 4
    default = 4
    slot = True
    slot_name = "inventorySlots"


# Logic Options

class GradeLocationRequiredGrade(Choice):
    """
    The end-of-day grade required to complete a grade location on a moon. This option will be ignored if 
    split_moon_grades is true.
    """
    display_name = "Grade Location Required Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "allMoonRequiredGrade"


class SplitMoonGrades(Toggle):
    """
    Allows the player to customize the required grade for easy, medium, and hard moons separately.
    """
    display_name = "Split Moon Grades"
    slot = True
    slot_name = "splitgrades"


class EasyMoonLocationGrade(Choice):
    """
    The end-of-day grade required to complete a grade location on an easy difficulty moon
    """
    display_name = "Easy Moon Location Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "easyMoonRequiredGrade"


class MedMoonLocationGrade(Choice):
    """
    The end-of-day grade required to complete a grade location on a medium difficulty moon
    """
    display_name = "Medium Moon Location Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "mediumMoonRequiredGrade"


class HardMoonLocationGrade(Choice):
    """
    The end-of-day grade required to complete a grade location on a hard difficulty moon
    """
    display_name = "Hard Moon Location Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "hardMoonRequiredGrade"


class ScrapSpawnChance(Range):
    """
    Scrap will not contain important items or be required for the Collectathon goal if their spawn chance on an in-logic 
    moon is less than this percentage. A value of less than 3% can significantly slow down games, while values above 6% 
    exclude most scrap.
    """
    display_name = "Minimum Scrap Spawn Chance"
    default = 3
    range_start = 0
    range_end = 10
    slot = True
    slot_name = "minscrapchance"


class MonsterSpawnChance(Range):
    """
    A bestiary entry will not contain important items if the monster's spawn chance on an in-logic moon is greater than or equal to this percentage. 
    A value of less than 3% can significantly slow down games.
    """
    display_name = "Minimum Monster Spawn Chance"
    default = 5
    range_start = 0
    range_end = 10
    slot = True
    slot_name = "minmonsterchance"


class MinMoneyPerMoneyItem(Range):
    """
    The minimum amount of money that a money item can give the player.
    """
    display_name = "Min Money Per Money Item"
    range_start = 0
    range_end = 1000
    default = 100
    slot = True
    slot_name = "minMoney"


class MaxMoneyPerMoneyItem(Range):
    """
    The maximum amount of money that a money item can give the player.
    This can't be less than min_money.
    """
    display_name = "Max Money Per Money Item"
    range_start = 0
    range_end = 1000
    default = 300
    slot = True
    slot_name = "maxMoney"


class ModifyScrapSpawns(Toggle):
    """
    Modifies the spawn rates and availability of scrap on every moon to reduce the chance of a player getting stuck for 
    a long time trying to find a rare item that is blocking progression.
    """
    display_name = "Modify Scrap Spawns"
    default = 0
    slot = True
    slot_name = "fixscrapsanity"


class ExcludeShotguns(Toggle):
    """
    Guarantees that scrapsanity locations requiring the player to kill an enemy will not contain important items
    """
    display_name = "Exclude Killing"
    slot = True
    slot_name = "excludeshotguns"


class ExcludeHive(Toggle):
    """
    Guarantees that the Hive scrapsanity location will not contain an important item
    """
    display_name = "Exclude Hive"
    slot = True
    slot_name = "excludehive"


class ExcludeEgg(Toggle):
    """
    Guarantees that the Sapsucker Egg scrapsanity location will not contain an important item
    """
    display_name = "Exclude Egg"
    slot = True
    slot_name = "excludeegg"

# Trap/Filler Weights

class MoneyWeight(Range):
    """
    The weight of money items in the filler/trap pool. 
    When redeemed, this item grants between min_money and max_money credits, though they don't count toward the quota.
    """
    display_name = "Money Weight"
    range_start = 0
    range_end = 100
    default = 80
    slot = False


class BirthdayGiftWeight(Range):
    """
    The weight of birthday gifts in the filler/trap pool. 
    When redeemed, this item sends a random store item down in the dropship.
    """
    display_name = "Birthday Gift Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


class WeightReducers(Range):
    """
    The total weight of strength training items. Every item received reduces the carry weight of all scrap.
    """
    display_name = "Strength Training Weight"
    default = 5
    range_start = 0
    range_end = 100


class ScrapDupeWeight(Range):
    """
    The weight of clone scrap items in the filler/trap pool. 
    When redeemed, this item duplicates a random piece of scrap in the ship.
    """
    display_name = "Scrap Cloning Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


class DayIncreaseWeight(Range):
    """
    The weight of more time items in the filler/trap pool. 
    When redeemed, this item adds one day to the current quota (up to 9).
    """
    display_name = "More Time Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


class DayDecreaseWeight(Range):
    """
    The weight of less time traps in the filler/trap pool. 
    When consumed, this trap reduces the remaining time to complete the current quota by one day.
    """
    display_name = "Less Time Weight"
    range_start = 0
    range_end = 100
    default = 30
    slot = False


class BrackenTrapWeight(Range):
    """
    The weight of bracken traps in the filler/trap pool.
    When consumed, this trap spawns a bracken on the current or next moon visited.
    """
    display_name = "Bracken Trap Weight"
    range_start = 0
    range_end = 100
    default = 8
    slot = False


class HauntTrapWeight(Range):
    """
    The weight of haunt traps in the filler/trap pool.
    When consumed, this trap spawns a ghost girl on the current or next moon visited.
    """
    display_name = "Haunt Trap Weight"
    range_start = 0
    range_end = 100
    default = 4
    slot = False


# Protocols

class DeathLinkScrapLoss(Range):
    """
    The percentage of scrap lost when the last living player dies from death link. 0 means no scrap is lost, 50 means 
    half of the scrap in the ship is lost, 100 means all scrap is lost. This option does not preserve scrap if the last 
    player dies naturally, and does nothing if death link is disabled.
    """
    display_name = "Death Link Scrap Loss"
    range_start = 0
    range_end = 100
    default = 50
    slot = True
    slot_name = "DeathLinkScrapLossPercent"


# Unused

class LogicDifficulty(Choice):
    """
    Changes the logic to adjust the difficulty of what is logically required to complete checks.
    Easy:
    Medium:
    Hard:
    Min Logic: The minimum possible requirements. Could make worlds impossible if you aren't skilled enough to complete
    some checks.
    Min Logic MP: THe minimum possible requirements when playing multiplayer. Main change is that experimentation no
    longer requires a stamina bar because one player can bring stuff out of the facility and a second player can ferry
    to the ship.
    """
    display_name = "Logic Difficulty"
    option_Easy = 0
    option_Medium = 1
    option_Hard = 2
    option_Min_Logic = 3
    option_Min_Logic_MP = 4
    default = 1


# Will contain a diff from the original imported and the new one, find a way to interpret that.
class CustomContent(FreeText):
    """
    Contains any custom content the player wants to use. See the guide on the github page to use this option
    """
    display_name = "Custom Content"
    default = "false"
    slot = False


"""
Stuff to add:
Starting inventory spots replaces enable_inventory_unlock - done
Starting stamina bars - done
Scanner - done
Jumping
Movement keys
Holding your breath
Sprinting - done (0 stamina is the same as no sprinting)
Random items spawning in the ship - done
Items added to dropship - done
Extra quota days - done
Speed increase
"""


@dataclass
class LCOptions(PerGameCommonOptions):
    game_mode: Goal
    collectathon_scrap_goal: CollectathonScrapGoal
    collectathon_random_scrap: CollectathonRandomScrap
    credit_replacement: CreditReplacement
    required_credits: RequiredCredits

    grade_locations_per_moon: GradeLocationsPerMoon
    num_quotas: NumQuotas
    quota_checkpoint_every: QuotaCheckpointEvery
    money_per_quota_location: MoneyPerQuotaLocation
    scrapsanity: Scrapsanity

    randomize_company_building: RandomizeCompanyBuilding
    randomize_scanner: RandomizeScanner
    randomize_terminal: RandomizeTerminal

    starting_moon: StartingMoon
    starting_stamina_bars: StartingStaminaBars
    starting_inventory_slots: StartingInventorySlots

    all_moon_required_grade: GradeLocationRequiredGrade
    split_moon_grades: SplitMoonGrades
    easy_moon_required_grade: EasyMoonLocationGrade
    medium_moon_required_grade: MedMoonLocationGrade
    hard_moon_required_grade: HardMoonLocationGrade
    min_scrap_chance: ScrapSpawnChance
    min_monster_chance: MonsterSpawnChance
    min_money: MinMoneyPerMoneyItem
    max_money: MaxMoneyPerMoneyItem
    modify_scrap_spawns: ModifyScrapSpawns
    exclude_killing: ExcludeShotguns
    exclude_hive: ExcludeHive
    exclude_egg: ExcludeEgg

    money: MoneyWeight
    birthday: BirthdayGiftWeight
    weight_reducers: WeightReducers
    scrap_clone: ScrapDupeWeight
    time_add: DayIncreaseWeight
    time_trap: DayDecreaseWeight
    bracken_trap: BrackenTrapWeight
    haunt_trap: HauntTrapWeight

    death_link: DeathLink
    death_link_percent_scrap_lost: DeathLinkScrapLoss
