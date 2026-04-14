from dataclasses import dataclass

from .items import item_groups

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionDict, PerGameCommonOptions, StartInventoryPool, FreeText
from schema import Schema, Optional


class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
    default = 30


class StartingKong(Choice):
    """
    Which Kongs will be available at the start
    """
    display_name = "Starting Kong"
    option_dixie = 1
    option_kiddy = 2
    option_both = 3
    default = 1


class ShuffleLevels(Toggle):
    """
    Shuffles levels around. Does nothing to bosses.
    """
    display_name = "Shuffle Levels"


class Logic(Choice):
    """
    Logic difficulty. May become irrelevant if not a lot of items are added to the item pool.
    - **Strict**: Ensures everything is reachable as the original devs intended. For beginners or people who want to go out of logic with some tricks.
    - **Loose**: Reaching locations may require some level of mastery about the game's mechanics.
    - **Expert**: Locations expects players to be extremely good at the game with minimal amount of abilities. Hard to go out of logic.
    """
    display_name = "Logic Difficulty"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 0


class Goal(Choice):
    """
    Which K.Rool fights will count towards the goal.
    - **Kore**: Defeat Baron K. Roolenstein at Kastle Kaos.
    - **Knautilus**: Defeat Baron K. Roolenstein at Knautilus.
    - **Kompletionist**: Defeat Baron K. Roolenstein at both locations.
    """
    display_name = "Goal"
    option_kore = 1
    option_krematoa = 2
    option_kompletionist = 3
    default = 1


class RequiredBirds(Range):
    """
    How many birds are required to reveal Kastle Kaos in the main map.
    Selecting 0 will create an Access item instead.
    """
    display_name = "Required Birds"
    range_start = 0
    range_end = 6
    default = 4


class CogPlacement(Choice):
    """
    Where are the five required Cogs placed in the session which are used to open up Knautilus at Krematoa.
    Having all 5 cogs also unlocks every single Krematoa level immediately.

    ONLY "ANYWHERE" IS SUPPORTED AT THE MOMENT
    """
    display_name = "Cog Placement"
    option_anywhere = 0
    option_krematoa_level_clear = 1
    option_krematoa_anywhere = 2
    default = 1


class RequiredLakeLevels(Range):
    """
    How many levels in Lake Orangatanga need to be cleared to fight the world's boss
    """
    display_name = "Lake Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredForestLevels(Range):
    """
    How many levels in Kremwood Forest need to be cleared to fight the world's boss
    """
    display_name = "Forest Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredCoveLevels(Range):
    """
    How many levels in Cotton Top Cove need to be cleared to fight the world's boss
    """
    display_name = "Cove Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredMekanosLevels(Range):
    """
    How many levels in Mekanos need to be cleared to fight the world's boss
    """
    display_name = "Mekanos Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredK3Levels(Range):
    """
    How many levels in K3 need to be cleared to fight the world's boss
    """
    display_name = "K3 Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredRidgeLevels(Range):
    """
    How many levels in Razor Ridge need to be cleared to fight the world's boss
    """
    display_name = "Ridge Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredKoreLevels(Range):
    """
    How many levels in Kaos Kore need to be cleared to fight the world's boss
    """
    display_name = "Kore Levels Required"
    range_start = 1
    range_end = 5
    default = 4


class RequiredKrematoaLevels(Range):
    """
    How many levels in Krematoa need to be cleared to fight the world's boss
    """
    display_name = "Krematoa Levels Required"
    range_start = 1
    range_end = 5
    default = 5


class AbilityShuffle(OptionSet):
    """
    Which abilities will be added as items in the item pool
    If an ability is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Ability Shuffle"
    default = {ability for ability in item_groups["Abilities"]}
    valid_keys = {ability for ability in item_groups["Abilities"]}


class AnimalShuffle(OptionSet):
    """
    Which animal buddies will be added as items in the item pool
    If an animal buddy is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Animal Buddies Shuffle"
    default = {ability for ability in item_groups["Animals"]}
    valid_keys = {ability for ability in item_groups["Animals"]}


class BarrelShuffle(OptionSet):
    """
    Which kind of barrels will be added as items in the item pool
    If a barrel is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Barrel Shuffle"
    default = {ability for ability in item_groups["Barrels"]}
    valid_keys = {ability for ability in item_groups["Barrels"]}


class KONGChecks(Toggle):
    """
    Whether collecting all KONG letters in each level will grant a check
    """
    display_name = "KONG Letters Checks"


class DKCoinChecks(Toggle):
    """
    Whether collecting a DK Coin in levels will grant a check
    """
    display_name = "DK Coin Checks"


class BananaChecks(Toggle):
    """
    Whether collecting banana bunches in levels will grant a check
    """
    display_name = "Banana Bunches Checks"


class BalloonChecks(Toggle):
    """
    Whether collecting balloons in levels will grant a check
    """
    display_name = "Balloon Checks"


class CoinChecks(Toggle):
    """
    Whether collecting bear coins in levels will grant a check
    """
    display_name = "Bear Coin Checks"


class BirdChecks(Toggle):
    """
    Whether collecting a banana bird will grant a check
    """
    display_name = "Banana Bird Checks"


class EnergyLink(Toggle):
    """
    EnergyLink allows players to deposit energy extracted from collected bananas into a shared pool across games in the session.

    You can exchange energy for Backup DK Barrels. Great for players that find the base game hard.
    There's an additional item in the item pool that allows for better energy extraction from bananas.
    """
    display_name = "Energy Link"


class DefaultSaveFileName(FreeText):
    """
    Which name will be given to the save file when pressing start at the name entry menu.
    Limited to 5 letters.
    """
    display_name = "Save File Name"
    default = "DIXIE"


dkc3_option_groups = [
    OptionGroup("Goal", [
        Goal,
        RequiredBirds,
        CogPlacement,
        RequiredLakeLevels,
        RequiredForestLevels,
        RequiredCoveLevels,
        RequiredMekanosLevels,
        RequiredK3Levels,
        RequiredRidgeLevels,
        RequiredKoreLevels,
        RequiredKrematoaLevels,
    ]),
    OptionGroup("Locations", [
        Logic,
        KONGChecks,
        DKCoinChecks,
        BalloonChecks,
        BananaChecks,
        CoinChecks,
        BirdChecks,
    ]),
    OptionGroup("Shuffle", [
        StartingKong,
        ShuffleLevels,
        AbilityShuffle,
        AnimalShuffle,
        BarrelShuffle,
    ]),
]

@dataclass
class DKC3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    energy_link: EnergyLink
    shuffle_levels: ShuffleLevels
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    logic: Logic
    goal: Goal
    required_birds: RequiredBirds
    cog_placement: CogPlacement
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_objects: BarrelShuffle
    kong_checks: KONGChecks
    balloon_checks: BalloonChecks
    banana_checks: BananaChecks
    dk_coin_checks: DKCoinChecks
    coin_checks: CoinChecks
    bird_checks: BirdChecks
    required_lake_levels: RequiredLakeLevels
    required_forest_levels: RequiredForestLevels
    required_cove_levels: RequiredCoveLevels
    required_mekanos_levels: RequiredMekanosLevels
    required_k3_levels: RequiredK3Levels
    required_ridge_levels: RequiredRidgeLevels
    required_kore_levels: RequiredKoreLevels
    required_krematoa_levels: RequiredKrematoaLevels
    default_save_name: DefaultSaveFileName
