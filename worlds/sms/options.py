from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range, Toggle


class LevelAccess(Choice):
    """If on "vanilla", the main levels are accessed in the way they are in the base game (e.g. Ricco Harbor is accessible after collecting 3 Shine Sprites).
    If on "tickets", each level has a ticket item that must be acquired to access the level.
    To reduce generation failures in testing, you'll automatically receive one free ticket at the start."""
    display_name = "Level Access"
    option_vanilla = 0
    option_tickets = 1


class EnableCoinShines(Toggle):
    """Turn off to ignore the 100 coin Shine Sprites, which removes 8 Shine Sprites from the pool.
    You can still collect them, but they don't do anything."""
    display_name = "Enable 100 Coin Shines"

# Keep in mind this needs to account for blue coins, nozzles, tickets, and any other progression items and still have
# Several locations to place filler/move around.
class CoronaMountainShines(Range):
    """How many Shine Sprites are required to access Corona Mountain and the Delfino Airstrip revisit.
    If this is more than the locations available, This will be automatically adjusted to 90-80% of locations available
    after all other progression items are created / accounted for."""
    display_name = "Corona Mountain Shines"
    range_start = 0
    range_end = 345
    default = 50

class ExtraShines(Range):
    """How many extra shine sprites you want added to the pool. This is a percentage so it ranges from 0 to 90
    If more shines would be added than locations possible it will add as many as it can"""
    display_name = "Extra Shines"
    range_start = 0
    range_end = 90
    default = 15


class BlueCoinSanity(Choice):
    """Full shuffle: adds Blue Coins to the pool and makes Blue Coins locations.
    Trade Shines Only: Adds the trade shines from the boathouse. Will NOT add the blue coin locations though.
    """
    display_name = "Blue Coinsanity"
    option_no_blue_coins = 0
    option_full_shuffle = 1
    option_trade_shines_only = 2
    default = 0


class BlueCoinMaximum(Range):
    """How many Blue Coins to include in the pool if Blue Coinsanity is on.
    Does nothing if Blue Coinsanity full_shuffle is off.
    Corresponding trade shines will be removed from locations.
    Removed Blue Coins will be replaced by extra Shine Sprites or other filler items."""
    display_name = "Blue Coin Maximum"
    range_start = 0
    range_end = 240
    default = 240


class TradeShineMaximum(Range):
    """The number of Shines from the boathouse trades that will be shuffled. If the Blue Coin Maximum is not enough
    to obtain this amount, it will decrease automatically.
    Keep in mind that if this value is too high, there is a chance you will have to nearly 100% the game."""
    display_name = "Trade Shine Maximum"
    range_start = 0
    range_end = 24
    default = 12


class StartingNozzle(Choice):
    """If on, you will start with no Spray Nozzle, and in fact, no FLUDD at all. (Still in non-enforce mode)
    You will skip directly to Delfino Plaza, and the first Airstrip mission will be removed from locations.
    In this early version of this setting, you are expected to spray unusual things with Hover."""
    display_name = "Starting Nozzle"
    option_spray = 0
    option_hover = 1
    option_fluddless = 2
    default = 0

class Difficulty(Choice):
    """This enables difficulty settings. Higher difficulty settings will include checks in logic that normally
    are not possible without doing difficult or unintended things. This includes spraying things with different
    nozzles, doing difficult platforming, and executing glitches."""
    display_name = "Difficulty"
    option_normal = 0
    option_hard = 1
    option_advanced = 2
    option_salty_tears = 3
    default = 0


class NozzleBoxes(Toggle):
    """Enables Nozzle Boxes as a location."""
    display_name = "Enable Nozzle Boxes"


class AllShinesSelectable(Toggle):
    """
    Enables you to select every shine without having to complete each in order.
    You will still need access to each hub (Gelato Beach, Noki Bay, Pinna Park, etc.)
    """
    display_name = "All Shines Selectable"


@dataclass
class SmsOptions(PerGameCommonOptions):
    level_access: LevelAccess
    enable_coin_shines: EnableCoinShines
    corona_mountain_shines: CoronaMountainShines
    extra_shines: ExtraShines
    nozzle_boxes: NozzleBoxes
    all_shines_selectable: AllShinesSelectable
    blue_coin_sanity: BlueCoinSanity
    blue_coin_maximum: BlueCoinMaximum
    trade_shine_maximum: TradeShineMaximum
    starting_nozzle: StartingNozzle
    death_link: DeathLink
    difficulty: Difficulty
