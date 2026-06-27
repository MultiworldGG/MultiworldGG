from dataclasses import dataclass
from Options import Toggle, DeathLink, Range, Choice, PerGameCommonOptions, FreeText, OptionGroup


class Goal(Choice):
    """
    Trophy Mode: Each moon has a rare trophy scrap, the goal is to get all of them (11 with no custom moons)

    Collectathon: A new rare scrap is added, you need to collect at least ten of it to win

    Credit Hunt: You must receive a number of company credit items as specified by the yaml to win. This can lead to
    very short or very long games depending on your settings
    """
    display_name = "Game Mode"
    option_trophy = 0
    option_collectathon = 1
    option_credit_hunt = 2
    default = 0
    slot = True
    slot_name = "goal"


class ChecksPerMoon(Range):
    """
    The total number of checks you can get at one moon
    """
    display_name = "Checks Per Moon"
    range_start = 1
    range_end = 10
    default = 3
    slot = True
    slot_name = "checksPerMoon"


class MoneyPerQuotaCheck(Range):
    """
    The total amount of quota you have to acheive to meet each quota check
    For example, if money per quota check is 1000, you need to reach 1000 total quota for each quota check
    """
    display_name = "Money Per Quota Check"
    range_start = 100
    range_end = 10000
    default = 500
    slot = True
    slot_name = "moneyPerQuotaCheck"


class NumQuotas(Range):
    """
    The number of quota locations to create. A quota location is completed whenever the player fulfills
    money_per_quota_check-worth of quota. Progress accumulates over quotas and crew wipes.

    Ex: If money_per_quota_check = 70 and the first quota is 120, then 1 quota location will be completed when the 
        player fulfills their first quota. If the second quota is 200, then 3 additional quota locations will be 
        completed when the player fulfills their second quota. 320 total quota has been fulfilled at this point, so a
        total of 4 quota locations are complete.
    """
    display_name = "Num Quotas"
    range_start = 10
    range_end = 50
    default = 20
    slot = True
    slot_name = "numQuota"


class QuotaCheckpointEvery(Range):
    """
    How many quota locations the player must complete between each checkpoint unlock event.
    With the default values (num_quotas=20 and quota_checkpoint_every=5), quota locations will be grouped into four
    spheres with five locations each. This helps ensure that important early items are not stuck behind late quota
    locations. Set higher than num_quotas to disable checkpoints entirely and group all quota locations into a single
    sphere.
    """
    display_name = "Quota Checkpoint Every"
    range_start = 1
    range_end = 20
    default = 5
    slot = False


class BrackenTrapWeight(Range):
    """
    The weight of the bracken traps in the pool.
    """
    display_name = "Bracken Trap Weight"
    range_start = 0
    range_end = 100
    default = 8
    slot = False


class HauntTrapWeight(Range):
    """
    The weight of haunt traps in the pool.
    """
    display_name = "Haunt Trap Weight"
    range_start = 0
    range_end = 100
    default = 4
    slot = False


class MoneyWeight(Range):
    """
    The weight of money drops in the pool. Each money drop can give anywhere from 100-1000 scrap,
    though it doesn't count towards the quota
    """
    display_name = "Money Weight"
    range_start = 0
    range_end = 100
    default = 80
    slot = False


class DayIncreaseWeight(Range):
    """
    The weight of extra day items in the pool
    """
    display_name = "Extra Day Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


class DayDecreaseWeight(Range):
    """
    The weight of day decrease traps in the pool.
    """
    display_name = "Lose a Day Weight"
    range_start = 0
    range_end = 100
    default = 30
    slot = False


class ScrapDupeWeight(Range):
    """
    The weight of scrap duplication items in the pool
    """
    display_name = "Scrap Cloning Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


class BirthdayGiftWeight(Range):
    """
    The weight of birthday gifts in the pool(random item sent in a dropship)
    """
    display_name = "Birthday Gift Weight"
    range_start = 0
    range_end = 100
    default = 20
    slot = False


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


class MinMoneyCheck(Range):
    """
    The minimum amount of money that a money check can give you
    """
    display_name = "Min Money Check Amount"
    range_start = 0
    range_end = 5000
    default = 100
    slot = True
    slot_name = "minMoney"


class MaxMoneyCheck(Range):
    """
    The maximum amount of money that a money check can give you
    """
    display_name = "Max Money Check Amount"
    range_start = 0
    range_end = 10000
    default = 1000
    slot = True
    slot_name = "maxMoney"


class StartingMoon(FreeText):
    """
    The moon you start on
    """
    display_name = "Starting Moon"
    default = "randomize"
    slot = False


class MoonCheckGrade(Choice):
    """
    The grade you need to get to get a check on a moon
    """
    display_name = "Moon Check Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "moonRank"


"""
Stuff to add:
Starting inventory spots replaces enable_inventory_unlock - done
Starting stamina bars - done
Scanner - done
Jumping
Movement keys
Holding your breath
Sprinting
Random items spawning in the ship - done
Items added to dropship - done
Extra quota days - done
Speed increase
"""


class StartingInventorySlots(Range):
    """
    The number of inventory slots you start the game with
    """
    display_name = "Starting Inventory Slots"
    range_start = 1
    range_end = 4
    default = 4
    slot = True
    slot_name = "inventorySlots"


class StartingStaminaBars(Range):
    """
    The number of stamina bars you start the game with
    """
    display_name = "Starting Stamina Bars"
    range_start = 0
    range_end = 4
    default = 4
    slot = True
    slot_name = "staminaBars"


class RandomizeScanner(Toggle):
    """
    Allows you to randomize your scanner, rendering you unable to scan until you receive the check
    """
    display_name = "Randomize Scanner"
    default = 0
    slot = True
    slot_name = "scanner"


class MonsterSpawnChance(Range):
    """
    Monsters will be in logic if their spawn chance on an in-logic moon is greater than or equal to this percentage. A
    value of less than 3% can significantly slow down your game.
    """
    display_name = "Minimum Monster Spawn Chance"
    default = 5
    range_start = 0
    range_end = 20
    slot = True
    slot_name = "minmonsterchance"


class WeightReducers(Range):
    """
    The total weight of strength training items. Every item received makes you 2% stronger.
    """
    display_name = "Strength Training Weight"
    default = 5
    range_start = 0
    range_end = 100


class Scrapsanity(Toggle):
    """
    Enables scrapsanity, where the first time each item is recovered from a moon is a check,
    adds >50 checks to the randomizer
    """
    display_name = "Scrapsanity"
    slot = True
    slot_name = "scrapsanity"


class ScrapSpawnChance(Range):
    """
    Scrap will be in logic if their spawn chance on an in-logic moon is greater than or equal to this percentage. A
    value of less than 3% can significantly slow down your game.
    """
    display_name = "Minimum Scrap Spawn Chance"
    default = 3
    range_start = 0
    range_end = 20
    slot = True
    slot_name = "minscrapchance"


class ExcludeShotguns(Toggle):
    """
    Makes it so there is guaranteed to be a filler item or trap in every check that can only be obtained through killing
    """
    display_name = "Exclude Killing"
    slot = True
    slot_name = "excludeshotguns"


class ExcludeHive(Toggle):
    """
    Makes it so there is guaranteed to be a filler item or trap in the hive scrapsanity check
    """
    display_name = "Exclude Hive"
    slot = True
    slot_name = "excludehive"


class ExcludeEgg(Toggle):
    """
    Makes it so there is guaranteed to be a filler item or trap in the sapsucker egg scrapsanity check
    """
    display_name = "Exclude Egg"
    slot = True
    slot_name = "excludeegg"


class SplitMoonGrades(Toggle):
    """
    Enables customizing the required grade for easy, medium, and hard moons separately.
    """
    display_name = "Split Moon Grades"
    slot = True
    slot_name = "splitgrades"


class EasyMoonCheckGrade(Choice):
    """
    The grade you need to get to get a check on an easy moon
    """
    display_name = "Easy Moon Check Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "lowMoon"


class MedMoonCheckGrade(Choice):
    """
    The grade you need to get to get a check on a medium difficulty moon
    """
    display_name = "Medium Moon Check Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "medMoon"


class HighMoonCheckGrade(Choice):
    """
    The grade you need to get to get a check on a hard moon
    """
    display_name = "Hard Moon Check Grade"
    option_S = 0
    option_A = 1
    option_B = 2
    option_C = 3
    option_D = 4
    option_F = 5
    default = 2
    slot = True
    slot_name = "highMoon"


class RandomizeCompanyBuilding(Toggle):
    """
    Adds the company building to the item pool
    """
    display_name = "Randomize Company Building"
    slot = True
    default = 0
    slot_name = "randomizecompany"


class RandomizeTerminal(Toggle):
    """
    Adds the terminal to the item pool
    """
    display_name = "Randomize Terminal"
    slot = True
    default = 0
    slot_name = "randomizeterminal"


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
    and you set this to 75, then once 75% of the 20 credits, or 15 credits, are collected, you will win
    """
    display_name = "Required Credits"
    range_start = 10
    range_end = 100
    default = 75


class ModifyScrapSpawns(Toggle):
    """
    Modifies the spawn rates and availability of scrap on every moon to make sure that you are never stuck for a long
    time trying to find that one specific scrap to unlock your terminal.
    """
    display_name = "Modify Scrap Spawns"
    default = 0
    slot = True
    slot_name = "fixscrapsanity"


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


@dataclass
class LCOptions(PerGameCommonOptions):
    game_mode: Goal #done
    collectathon_scrap_goal: CollectathonScrapGoal #done
    credit_replacement: CreditReplacement #done
    required_credits: RequiredCredits #done
    checks_per_moon: ChecksPerMoon #done
    money_per_quota_check: MoneyPerQuotaCheck #done
    num_quotas: NumQuotas #done
    quota_checkpoint_every: QuotaCheckpointEvery #done
    starting_inventory_slots: StartingInventorySlots #done
    starting_stamina_bars: StartingStaminaBars #done
    randomize_scanner: RandomizeScanner #done
    min_monster_chance: MonsterSpawnChance #done
    randomize_terminal: RandomizeTerminal #done
    randomize_company_building: RandomizeCompanyBuilding #done
    scrapsanity: Scrapsanity #done
    min_scrap_chance: ScrapSpawnChance #done
    exclude_killing: ExcludeShotguns
    exclude_hive: ExcludeHive
    exclude_egg: ExcludeEgg
    modify_scrap_spawns: ModifyScrapSpawns
    min_money: MinMoneyCheck #done
    max_money: MaxMoneyCheck #done
    starting_moon: StartingMoon #done
    split_moon_grades: SplitMoonGrades #done
    moon_grade: MoonCheckGrade #done
    low_moon_grade: EasyMoonCheckGrade #done
    medium_moon_grade: MedMoonCheckGrade #done
    high_moon_grade: HighMoonCheckGrade #done
    time_add: DayIncreaseWeight #done
    scrap_clone: ScrapDupeWeight #done
    birthday: BirthdayGiftWeight #done
    weight_reducers: WeightReducers #done
    bracken_trap: BrackenTrapWeight #done
    haunt_trap: HauntTrapWeight #done
    time_trap: DayDecreaseWeight #done
    money: MoneyWeight #done
    death_link: DeathLink
