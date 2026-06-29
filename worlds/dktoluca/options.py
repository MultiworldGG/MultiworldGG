from dataclasses import dataclass

from .items import item_groups
from .data.palettes import palettes

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionDict, PerGameCommonOptions, StartInventoryPool, FreeText
from schema import Schema, Optional, And


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
    - **Kastle Kaos**: Defeat Baron K. Roolenstein at Kastle Kaos.
    - **Knautilus**: Defeat Baron K. Roolenstein at Knautilus.
    - **Kompletionist**: Defeat Baron K. Roolenstein at both locations.
    """
    display_name = "Goal"
    option_kastle_kaos = 1
    option_knautilus = 2
    option_kompletionist = 3
    default = 1


class SwapKRool(Toggle):
    """
    Swaps Kastle KAOS and Knautilus on the map.
    """
    display_name = "Swap K. Rool"


class RequiredBirds(Range):
    """
    How many birds are required to reveal Kastle Kaos in the main map.
    Selecting 0 will create an Access item instead.
    """
    display_name = "Required Birds"
    range_start = 0
    range_end = 6
    default = 4


class ExtraBirds(Range):
    """
    How many additional banana birds will be in the item pool.
    """
    display_name = "Extra Birds"
    range_start = 0
    range_end = 6
    default = 0


class CogPlacement(Choice):
    """
    Where are the five required Cogs placed in the session which are used to open up Knautilus at Krematoa.
    Having all five cogs also unlocks every single Krematoa level immediately.
    """
    display_name = "Cog Placement"
    option_anywhere = 0
    option_krematoa_level_clear = 1
    option_krematoa_anywhere = 2
    default = 1


class ExtraCogs(Range):
    """
    How many additional cogs will be in the item pool.
    """
    display_name = "Extra Cogs"
    range_start = 0
    range_end = 5
    default = 0


class ExtraBonusCoins(Range):
    """
    How many additional bonus coins will be in the item pool. These unlock Krematoa levels.
    """
    display_name = "Extra Bonus Coins"
    range_start = 0
    range_end = 5
    default = 0


class VehicleUnlock(Choice):
    """
    Controls how vehicles are unlocked through the game.

    Items: Get vehicles from multiworld items
    Banana Birds: Get vehicles after getting a certain number of banana birds.
                  Hovercraft: Get 1 banana birds
                  Turbo Ski: Get 2 banana birds
                  Gyrocopter: Get 4 banana birds
    World Unlocks: Get vehicles after getting worlds
                   Obtaining either Cove or Mekanos grants one
                   Obtaining either K3 or Ridge grants one
                   Obtaining Krematoa grants one
    """
    display_name = "Vehicle Unlock"
    option_item = 0
    option_banana_birds = 1
    option_world_unlocks = 2


class RequiredLakeLevels(Range):
    """
    How many levels in Lake Orangatanga need to be cleared to fight the world's boss
    """
    display_name = "Lake Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredForestLevels(Range):
    """
    How many levels in Kremwood Forest need to be cleared to fight the world's boss
    """
    display_name = "Forest Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredCoveLevels(Range):
    """
    How many levels in Cotton Top Cove need to be cleared to fight the world's boss
    """
    display_name = "Cove Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredMekanosLevels(Range):
    """
    How many levels in Mekanos need to be cleared to fight the world's boss
    """
    display_name = "Mekanos Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredK3Levels(Range):
    """
    How many levels in K3 need to be cleared to fight the world's boss
    """
    display_name = "K3 Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredRidgeLevels(Range):
    """
    How many levels in Razor Ridge need to be cleared to fight the world's boss
    """
    display_name = "Ridge Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredKoreLevels(Range):
    """
    How many levels in Kaos Kore need to be cleared to fight the world's boss
    """
    display_name = "Kore Levels Required"
    range_start = 0
    range_end = 5
    default = 4


class RequiredKrematoaLevels(Range):
    """
    How many levels in Krematoa need to be cleared to fight the world's boss
    """
    display_name = "Krematoa Levels Required"
    range_start = 0
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


class KONGLocations(Toggle):
    """
    Whether collecting all KONG letters in each level will be considered a location
    """
    display_name = "KONG Letters Locations"


class DKCoinLocations(Toggle):
    """
    Whether collecting a DK Coin in levels will be considered a location
    """
    display_name = "DK Coin Locations"


class BananaLocations(Toggle):
    """
    Whether collecting banana bunches in levels will be considered a location
    """
    display_name = "Banana Bunches Locations"


class BalloonLocations(Toggle):
    """
    Whether collecting balloons in levels will be considered a location
    """
    display_name = "Balloon Locations"


class CoinLocations(Toggle):
    """
    Whether collecting bear coins in levels will be considered a location
    """
    display_name = "Bear Coin Locations"


class BirdLocations(Toggle):
    """
    Whether collecting a banana bird will be considered a location
    """
    display_name = "Banana Bird Locations"


class SwankyLocations(Toggle):
    """
    Whether completing Swanky's Sideshow games in each world will be considered a location
    """
    display_name = "Swanky Locations"


class TradeShuffle(Toggle):
    """
    Shuffles Bear Brothers' trade items among themselves.
    """
    display_name = "Trade Shuffle"


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

class Palettes(OptionDict):
    """
    palettes
    """
    display_name = "Palettes"
    schema = Schema({
        Optional("Dixie"): And(str, lambda p: p in palettes["Dixie"].keys()),
        Optional("Dixie Inactive"): And(str, lambda p: p in palettes["Dixie"].keys()),
        Optional("Dixie Invincible"): And(str, lambda p: p in palettes["Dixie"].keys()),
        Optional("Kiddy"): And(str, lambda p: p in palettes["Kiddy"].keys()),
        Optional("Kiddy Inactive"): And(str, lambda p: p in palettes["Kiddy"].keys()),
        Optional("Kiddy Invincible"): And(str, lambda p: p in palettes["Kiddy"].keys()),
    })
    default = {
        "Dixie": "original",
        "Dixie Inactive": "original_inactive",
        "Dixie Invincible": "original_invincible",
        "Kiddy": "original",
        "Kiddy Inactive": "original_inactive",
        "Kiddy Invincible": "original_invincible",
    }

class PaletteFilters(OptionDict):
    """
    Applies a filter that can brighten or darken your selected palette
    Doesn't produce results similar to the original ones, but it's good enough
    
    Positive numbers create a brighter color palette (the higher the number, the brighter the palette)
    Negative numbers create a darker color palette (the higher (or lower lol) the negative number, the darker the palette)
    
    Treat the values as percentages
    """
    display_name = "Palette Filters"
    schema = Schema({
        Optional("Dixie"): And(int, lambda x: -100 <= x <= 100),
        Optional("Dixie Inactive"): And(int, lambda x: -100 <= x <= 100),
        Optional("Dixie Invincible"): And(int, lambda x: -100 <= x <= 100),
        Optional("Kiddy"): And(int, lambda x: -100 <= x <= 100),
        Optional("Kiddy Inactive"): And(int, lambda x: -100 <= x <= 100),
        Optional("Kiddy Invincible"): And(int, lambda x: -100 <= x <= 100),
    })
    default = {
        "Dixie": 0,
        "Dixie Inactive": 0,
        "Dixie Invincible": 0,
        "Kiddy": 0,
        "Kiddy Inactive": 0,
        "Kiddy Invincible": 0,
    }


dkc3_option_groups = [
    OptionGroup("Goal", [
        Goal,
        SwapKRool,
        RequiredBirds,
        ExtraBirds,
        CogPlacement,
        ExtraCogs,
        ExtraBonusCoins,
        VehicleUnlock,
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
        KONGLocations,
        DKCoinLocations,
        BalloonLocations,
        BananaLocations,
        CoinLocations,
        BirdLocations,
        SwankyLocations,
    ]),
    OptionGroup("Shuffle", [
        StartingKong,
        ShuffleLevels,
        AbilityShuffle,
        AnimalShuffle,
        BarrelShuffle,
    ]),
    OptionGroup("Misc", [
        Palettes,
        PaletteFilters,
        DefaultSaveFileName,
        TradeShuffle,
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
    swap_krool: SwapKRool
    required_birds: RequiredBirds
    extra_birds: ExtraBirds
    cog_placement: CogPlacement
    extra_cogs: ExtraCogs
    extra_bonus_coins: ExtraBonusCoins
    vehicle_unlock: VehicleUnlock
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_objects: BarrelShuffle
    kong_locations: KONGLocations
    balloon_locations: BalloonLocations
    banana_locations: BananaLocations
    dk_coin_locations: DKCoinLocations
    coin_locations: CoinLocations
    bird_locations: BirdLocations
    swanky_locations: SwankyLocations
    required_lake_levels: RequiredLakeLevels
    required_forest_levels: RequiredForestLevels
    required_cove_levels: RequiredCoveLevels
    required_mekanos_levels: RequiredMekanosLevels
    required_k3_levels: RequiredK3Levels
    required_ridge_levels: RequiredRidgeLevels
    required_kore_levels: RequiredKoreLevels
    required_krematoa_levels: RequiredKrematoaLevels
    palettes: Palettes
    palette_filters: PaletteFilters
    default_save_name: DefaultSaveFileName
    trade_shuffle: TradeShuffle
