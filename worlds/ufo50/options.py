from dataclasses import dataclass

from Options import (StartInventoryPool, Range, OptionSet, PerGameCommonOptions, OptionGroup, Choice, Toggle,
                     DefaultOnToggle, Visibility)

from .constants import game_ids


class AlwaysOnGames(OptionSet):
    """
    Choose which games you would like to enable.

    The following games have full implementations: Barbuta, Vainger, Night Manor, Divers, Grimstone, Golfaria and Porgy.
    Party House has a more minor implementation, and counts as an implemented game.
    There is a host.yaml setting that you must enable to include unimplemented games.
    Unimplemented games will only have Garden, Gold, and/or Cherry checks.
    The host.yaml setting is not required for the following games due to their short length:
    Ninpek, Magic Garden, Velgress, and Waldorf's Journey
    """
    internal_name = "always_on_games"
    display_name = "Always On Games"
    valid_keys = {game_name for game_name in game_ids.keys() if game_name != "Main Menu"}
    # default is here so the unit tests don't fail
    default = ["Barbuta"]


class RandomChoiceGames(OptionSet):
    """
    Choose which games have a chance of being enabled.
    The number of games that will be enabled is based on the Random Choice Game Count option.
    """
    internal_name = "random_choice_games"
    display_name = "Random Choice Games"
    valid_keys = {game_name for game_name in game_ids.keys() if game_name != "Main Menu"}


class RandomChoiceGameCount(Range):
    """
    Choose how many Random Choice Games will be included alongside your Always On Games.
    If your Random Choice Game Count is larger than the number of games in your Random Choice Games list, all of them will be enabled.
    """
    internal_name = "random_choice_game_count"
    display_name = "Random Choice Game Count"
    range_start = 0
    range_end = 50
    default = 0
    # this is super unnecessary to show in the spoiler, so just hide it
    visibility = Visibility.template | Visibility.simple_ui | Visibility.complex_ui


class StartingGameAmount(Range):
    """
    Choose how many games to have unlocked at the start.
    At least one of the starting games will always be one of the implemented games, to avoid issues with generation and very early BK.
    If this value is higher than the number of games you selected, you will start with all of them unlocked.
    If you put a game in your start inventory from pool, it will count towards the amount from this option.
    """
    internal_name = "starting_game_amount"
    display_name = "Starting Game Amount"
    range_start = 1
    range_end = 50
    default = 1


class GoalGames(OptionSet):
    """
    Choose which games you may have to complete to achieve your goal.
    """
    internal_name = "goal_games"
    display_name = "Goal Games"
    valid_keys = {game_name for game_name in game_ids.keys() if game_name != "Main Menu"}
    default = {game_name for game_name in game_ids.keys() if game_name != "Main Menu"}


class GoalGameAmount(Range):
    """
    Choose how many games you need to goal to achieve your goal among your Goal Games.
    If this number is less than the number of Goal Games you have selected, it will choose some of them at random to be your Goal Games.
    If this number is greater than or equal to your number of Goal Games, then all of your games will be your Goal Games.
    """
    internal_name = "goal_game_amount"
    display_name = "Goal Game Amount"
    range_start = 1
    range_end = 50
    default = 50
    # this is super unnecessary to show in the spoiler, so just hide it
    visibility = Visibility.template | Visibility.simple_ui | Visibility.complex_ui


class CherryAllowed(OptionSet):
    """
    Choose which games you want to include the Cherry goal in.
    If the game is set as your Goal Game, then you will need to Cherry that game to complete that goal.
    If the game is not set as a Goal Game, then Cherrying that game will be a check.
    If the game is not selected at all, then this option will not affect it.
    The defaults are ones where we believe the Cherry goal is reasonable in the context of a randomizer.
    """
    internal_name = "cherry_allowed_games"
    display_name = "Cherry-Allowed Games"
    valid_keys = {game_name for game_name in game_ids.keys() if game_name != "Main Menu"}
    # include the games where it makes sense to be Cherry by default
    default = {"Barbuta", "Night Manor"}


class PorgyFuelDifficulty(Choice):
    """
    Determine how much fuel you need to get checks.
    Hard means an efficient route with minimal damage.
    Medium means 25% more fuel than Hard.
    Easy means 50% more fuel than Hard.
    """
    internal_name = "porgy_fuel_difficulty"
    display_name = "Porgy - Fuel Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = 1


class PorgyCheckOnTouch(Toggle):
    """
    If enabled, you will check a location as soon as you touch it, rather than having to bring it back.
    For a shorter, quicker experience.
    """
    internal_name = "porgy_check_on_touch"
    display_name = "Porgy - Check on Touch"


class PorgyRadar(Choice):
    """
    Choose how the Radar System and its logic behave.
    Always On: The Radar System is always on without needing to equip it or receive it.
    Not Required: The Radar System is not logically required for concealed locations.
    Required: The Radar System is logically required for all concealed locations.
    Required No Tell: The Radar System is logically required for concealed locations without a visual cue.
    """
    internal_name = "porgy_radar"
    display_name = "Porgy - Radar Logic"
    option_always_on = 0
    option_not_required = 1
    option_required = 2
    option_required_no_tell = 3
    default = 2


class PorgyLanternless(Toggle):
    """
    If enabled, you will not logically require the Spotlight in the Abyss area.
    """
    internal_name = "porgy_lanternless"
    display_name = "Porgy - Lanternless"


# Night Manor
class NMEarlyPin(DefaultOnToggle):
    """
    If enabled, the Hairpin will be on the floor in the starting room on either the Bowl or Spoon checks.
    """
    internal_name = "nm_early_pin"
    display_name = "Night Manor - Early Hairpin"


# Divers
class DiversXp(Range):
    """
    Percentage of EXP enemies give you. 100 is vanilla, after scaling, and 300 is x3.
    """
    internal_name = "divers_xp"
    display_name = "Divers - XP"
    range_start = 100
    range_end = 300
    default = 100


class DiversCash(Range):
    """
    Percentage of Cash enemies give you. 100 is vanilla, after scaling, and 300 is x3.
    """
    internal_name = "divers_cash"
    display_name = "Divers - Cash"
    range_start = 100
    range_end = 300
    default = 200


class DiversRelicMult(Range):
    """
    Multiplier for relics received. Recommended if
    DiversStoreDepth is greater than 1
    """
    internal_name = "divers_relic_mult"
    display_name = "Divers - Relic Multiplier"
    range_start = 1
    range_end = 9
    default = 3


class DiversStoreDepth(Range):
    """
    Number of checks in each slot of the Store
    """
    internal_name = "divers_store_depth"
    display_name = "Divers - Store Depth"
    range_start = 1
    range_end = 6
    default = 2


class DiversXpItem(Range):
    """
    Choose how many XP multipliers will be items
    Each XP multiplier multiplies XP from enemies by 2
    """
    internal_name = "divers_xp_item"
    display_name = "Divers - XP Multiplier Items"
    range_start = 0
    range_end = 4
    default = 0


class DiversCashItem(Range):
    """
    Choose how many Cash multiplier will be items
    Each Cash multiplier multiplies Cash from enemies by 2
    """
    internal_name = "divers_cash_item"
    display_name = "Divers - Cash Multiplier Items"
    range_start = 0
    range_end = 4
    default = 0


class DiversStartWithFlippers(Toggle):
    """
    If Enabled, the player will start with Flippers
    """
    internal_name = "divers_start_flippers"
    display_name = "Divers - Start With Flippers"


class DiversPearl(Toggle):
    """
    If Enabled, each chest will be a pearl to bring home
    """
    internal_name = "divers_pearl"
    display_name = "Divers - Chests Have Pearls"


# Golfaria
class GolfariaStartWithBrakes(Toggle):
    """
    If Enabled, the player will start with Brakes
    """
    internal_name = "golfaria_start_brakes"
    display_name = "Golfaria - Start With Brakes"


class GolfariaDifficulty(Choice):
    """
    Difficulty setting for routing, affects logic
    In hardcore difficulty, you can only save at
    the waking cave checkpoint and collecting
    clubs doesn't increase your max strokes until
    the last boss.
    """
    internal_name = "golfaria_difficulty"
    display_name = "Golfaria - Difficulty"
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_hardcore = 4
    default = 1


class GolfariaHandicap(Range):
    """
    Difficulty setting for amount of strokes, affects logic
    1 = 10%, 2 = 20% etc.
    """
    internal_name = "golfaria_handicap"
    display_name = "Golfaria - Handicap"
    range_end = 5


class GolfariaHardcoreStrokes(Range):
    """
    Starting strokes for Hardcore mode only
    If set to lower than 20, clubs give you
    1 stroke each to a maximum of 20
    """
    internal_name = "golfaria_hardcore_strokes"
    display_name = "Golfaria - Hardcore Starting Strokes"
    range_start = 10
    range_end = 20
    default = 20


# Grimstone
class GrimstoneXp(Range):
    """
    Percentage of EXP enemies give you. 100 is vanilla, and 300 is x3.
    """
    internal_name = "grimstone_xp"
    display_name = "Grimstone - XP"
    range_start = 100
    range_end = 300
    default = 300


class GrimstoneCash(Range):
    """
    Percentage of Cash enemies give you. 100 is vanilla, and 300 is x3.
    """
    internal_name = "grimstone_cash"
    display_name = "Grimstone - Cash"
    range_start = 100
    range_end = 300
    default = 200


class GrimstoneXpItem(Range):
    """
    Choose how many XP multipliers will be items
    Each XP multiplier multiplies XP from enemies by 2
    """
    internal_name = "grimstone_xp_item"
    display_name = "Grimstone - XP Multiplier Items"
    default = 2
    range_end = 4


class GrimstoneCashItem(Range):
    """
    Choose how many Cash multipliers will be items
    Each Cash multiplier multiplies Cash from enemies by 2
    """
    internal_name = "grimstone_cash_item"
    display_name = "Grimstone - Cash Multiplier Items"
    default = 2
    range_end = 4


class GrimstoneShops(Range):
    """
    Shop mode for Grimstone
    0 = default
    1 = own filler only
    2 = shopsanity *DIFFICULT*
    Only enable shopsanity if you know what you are doing!
    """
    internal_name = "grimstone_shops"
    display_name = "Grimstone - Shops"
    range_start = 0
    range_end = 2
    default = 0


class GrimstoneRandomCharacters(Toggle):
    """
    Start Grimstone with random characters
    """
    internal_name = "grimstone_random_characters"
    display_name = "Grimstone - Random Characters"


class GrimstoneDuplicateCharacters(Toggle):
    """
    Allow duplicate characters in Grimstone
    """
    internal_name = "grimstone_duplicate_characters"
    display_name = "Grimstone - Duplicate Characters"


@dataclass
class UFO50Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    always_on_games: AlwaysOnGames
    random_choice_games: RandomChoiceGames
    random_choice_game_count: RandomChoiceGameCount
    starting_game_amount: StartingGameAmount
    goal_games: GoalGames
    goal_game_amount: GoalGameAmount
    cherry_allowed_games: CherryAllowed

    porgy_fuel_difficulty: PorgyFuelDifficulty
    porgy_check_on_touch: PorgyCheckOnTouch
    porgy_radar: PorgyRadar
    porgy_lanternless: PorgyLanternless

    nm_early_pin: NMEarlyPin

    divers_xp: DiversXp
    divers_cash: DiversCash
    divers_relic_mult: DiversRelicMult
    divers_store_depth: DiversStoreDepth
    divers_xp_item: DiversXpItem
    divers_cash_item: DiversCashItem
    divers_start_flippers: DiversStartWithFlippers
    divers_pearl: DiversPearl

    golfaria_start_brakes: GolfariaStartWithBrakes
    golfaria_difficulty: GolfariaDifficulty
    golfaria_handicap: GolfariaHandicap
    golfaria_hardcore_strokes: GolfariaHardcoreStrokes

    grimstone_xp: GrimstoneXp
    grimstone_cash: GrimstoneCash
    grimstone_xp_item: GrimstoneXpItem
    grimstone_cash_item: GrimstoneCashItem
    grimstone_shops: GrimstoneShops
    grimstone_random_characters: GrimstoneRandomCharacters
    grimstone_duplicate_characters: GrimstoneDuplicateCharacters


ufo50_option_groups = [
    OptionGroup("General Options", [
        AlwaysOnGames,
        RandomChoiceGames,
        RandomChoiceGameCount,
        StartingGameAmount,
        GoalGames,
        GoalGameAmount,
        CherryAllowed,
    ]),
    OptionGroup("Porgy Options", [
        PorgyFuelDifficulty,
        PorgyCheckOnTouch,
        PorgyRadar,
        PorgyLanternless,
    ]),
    OptionGroup("Night Manor Options", [
        NMEarlyPin,
    ]),
    OptionGroup("Divers Options", [
        DiversXp,
        DiversCash,
        DiversRelicMult,
        DiversStoreDepth,
        DiversXpItem,
        DiversCashItem,
        DiversStartWithFlippers,
        DiversPearl,
    ]),
    OptionGroup("Golfaria Options", [
        GolfariaStartWithBrakes,
        GolfariaDifficulty,
        GolfariaHandicap,
        GolfariaHardcoreStrokes,
    ]),
    OptionGroup("Grimstone Options", [
        GrimstoneXp,
        GrimstoneCash,
        GrimstoneXpItem,
        GrimstoneCashItem,
        GrimstoneShops,
        GrimstoneRandomCharacters,
        GrimstoneDuplicateCharacters,
    ]),

]
