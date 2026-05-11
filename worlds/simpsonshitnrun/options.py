from dataclasses import dataclass
from schema import Schema, And, SchemaError
from Options import Choice, OptionSet, PerGameCommonOptions, Range, Toggle, OptionGroup, OptionError
from .items import item_name_groups

VALID_CHAR_KEYS = ["Homer", "Bart", "Lisa", "Marge", "Apu", "All", "None"]

class OptionSetNoEmpty(OptionSet):
    schema = Schema(And(set[str], len))

class ISTicket(Choice):
    """Goal is watching the Itchy and Scratchy film in the Lobby.
       You'll receive the Ticket when you complete the requirements chosen."""
    display_name = "Itchy and Scratchy Ticket Requirement"
    default = 0
    option_missions_complete = 0
    option_story_missions_complete = 1
    option_final_mission_L7M7 = 2
    option_cars_collected = 3

class WaspAmount(Range):
    """ Number of Wasps additionally required to gain the Itchy and Scratchy ticket. There are 20 per level."""
    display_name = "Required Wasp Amount"
    range_start = 0
    range_end = 140
    default = 70

class CardAmount(Range):
    """Number of Cards additionally required to gain the Itchy and Scratchy ticket. There are 7 per level."""
    display_name = "Required Card Amount"
    range_start = 0
    range_end = 49
    default = 25

class RequiredMissionLevels(OptionSetNoEmpty):
    """If the ticket requires missions or story missions, choose which level's missions are required.
       Missions in other levels may still unlock required items.
       Has no effect if the ticket doesn't require missions.
       Valid options are 1, 2, 3, 4, 5, 6, 7, or All."""
    default = frozenset({"All"})
    valid_keys = ["1", "2", "3", "4", "5", "6", "7", "All"]
    display_name = "Required Mission Levels"

class EarlyLevel(Toggle):
    """If enabled, attempt to place at least one of your required levels in an early location."""
    display_name = "Early Level Item"
    default = True

class CarAmount(Range):
    """If the ticket requires cars collected, choose the amount of cars required."""
    display_name = "Required Car Amount"
    range_start = 10
    range_end = 81
    default = 50

class LockLevels(Toggle):
    """If enabled, levels are will be inaccessible to Free Roam until you receive their respective Level item."""
    display_name = "Lock Levels"
    default = True

class ShuffleLevels(Toggle):
    """Choose how you want Levels to be received.
       If shuffled, 6 Level X items will be shuffled into the item pool which will allow access to that level's missions
       Otherwise, 6 Progressive Level items will be shuffled into the item pool, allowing you to access levels in the vanilla order.
       Regardless of your choice, missions can be played in any order on an unlocked level.
       """
    display_name = "Shuffle Levels"
    default = True

class ShuffleStartingCar(Toggle):
    """Choose whether to shuffle starting car between available cars from your starting level.
       If disabled, you'll always start with your starting level's default car.
        """
    display_name = "Shuffle Starting Car"
    default = True

class ShuffleAttack(OptionSet):
    """Choose whether to add Attack to the pool for each character.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
    """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Attack"

class ShuffleJump(OptionSet):
    """Choose whether to add Jump to the pool for each character.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
    """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Jump"

class StartingJumpLevel(Range):
    """Choose how many Progressive Jump items to start with for each character.
       Characters who aren't included in ShuffleJump will start with Progressive Jump Level 2.
    """
    display_name = "Starting Jump Level"
    range_start = 0
    range_end = 2
    default = 1

class ShuffleGagfinder(OptionSet):
    """Choose whether to add a Gagfinder to the pool for each Character that will be required to
       unlock gags as that character. Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
       If None, gags will instead be locked until you receive their Level.
       """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Gagfinder"

class ShuffleCheckeredFlags(OptionSet):
    """Choose whether to add a Checkered Flag to the pool for each Character that will be required to
       unlock races as that character. Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
       If None, races will instead be locked until you receive their Level.
       """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Checkered Flags"

class ShuffleForward(OptionSet):
    """Choose whether to shuffle the ability to move forward or drive forward for each character into the item pool.
       Characters not chosen won't have a forward in the item pool and will always be able to move forward.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
       **THIS COULD CREATE VERY DIFFICULT SEEDS**
    """

    default = frozenset({"None"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Forward"

class EarlyForward(OptionSet):
    """If enabled and forward is shuffled, try to place each specified character's Forward item early.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None. Does nothing if the character's forward isn't shuffled.
    """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Early Forward"

class ShuffleEBrakes(OptionSet):
    """Choose whether to shuffle ability to use the E-Brake for each character into the item pool.
       Characters not chosen will always be able to use the E-Brake.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
       """

    default = frozenset({"All"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle E-Brake"

class ShuffleBumpers(OptionSet):
    """Choose whether to shuffle Frink-o-Matic Wasp Bumpers into the item pool.
       Characters not chosen won't have a Wasp Bumper in the item pool and *WILL NOT* be able to break wasps with cars.
       Valid options are Homer, Bart, Lisa, Marge, Apu, All, or None.
    """

    default = frozenset({"None"})
    valid_keys = VALID_CHAR_KEYS
    display_name = "Shuffle Bumpers"

class StartWithBumpers(Toggle):
    """If true, add all enabled Wasp Bumpers to the start inventory.
       If you want more granular control of this, use the generic start inventory."""

    display_name = "Start With Bumpers"
    default = False

class ShuffleCards(Toggle):
    """Randomize card locations. This option adds several possible locations for
       cards. There will still be 49 total cards with 7 in each level."""

    default = True
    display_name = "Shuffle Cards"

class AddMissionLocks(Range):
    """Add car requirements to a percentage of missions"""

    display_name = "Mission Locks"
    range_start = 0
    range_end = 100

class AdjustMissionTimers(Range):
    """Increase mission timers by the chosen percentage.
       For example, if a mission has a timer of 1:00 and the chosen value is 50, then the mission will have a timer of 1:30"""

    display_name = "Adjust Mission Timers"
    range_start = 0
    range_end = 100

class MinShopPrice(Range):
    """The minimum cost of any item in Gil's Shop. If this is greater than the max shop price, then the max will be used instead."""
    display_name = "Min Shop Price"
    range_start = 0
    range_end = 500
    default = 100

class MaxShopPrice(Range):
    """The maximum cost of any item in Gil's Shop."""
    display_name = "Max Shop Price"
    range_start = 0
    range_end = 500
    default = 300

class ShopScaleMod(Range):
    """The multiplier for shop costs per levels. For each level after L1, min and max will be multiplied by level number and this multiplier.
       L2 = Min/Max * Mod * 2, L3 = Min/Max * Mod * 3, etc.
    """
    display_name = "Shop Price Level Scale Multiplier"
    range_start = 1
    range_end = 5
    default = 2

class StartingWalletLevel(Range):
    """Choose how many Progressive Wallet Levels to start with.
       Level 1 shops are in logic with 1 level, level 2 with 2, etc.
       Your coin cap = MaxShopPrice * WalletLevel * ShopScaleMod and is unlimited at Wallet Level 7
    """
    display_name = "Starting Wallet Level"
    range_start = 0
    range_end = 7
    default = 1

class ShopHintPolicy(Choice):
    """Choose the level of hints sent when speaking to Gil for the first time on a level
       All: Hint all items in Gil's shop
       OnlyProg: Only hint progression items in Gil's shop
       None: No shop hints will be created
    """
    display_name = "Shop Hint Policy"
    option_all = 0
    option_onlyprog = 1
    option_none = 2

class ExtraHintPolicy(Toggle):
    """Place extra hints in various places."""
    default = True
    display_name = "Extra Hint Policy"

class FillerWrenchEfficiency(Range):
    """Percentage damage a filler wrench item will repair your cars."""
    display_name = "Filler Wrench Efficiency"
    default = 10
    range_start = 0
    range_end = 100

class FillerHitNRunResetEfficiency(Range):
    """Percentage a filler Hit N Run Reset item will lower your Hit N Run meter."""
    display_name = "Filler Hit N Run Reset Efficiency"
    default = 10
    range_start = 0
    range_end = 100

class ShuffleTraffic(Toggle):
    """Randomize traffic per level. Cars that are usually used as traffic in that level plus the starting car of the next level are unable to be chosen for their level."""
    default = True
    display_name = "Shuffle Traffic"

class TrafficBlacklist(OptionSet):
    """Block cars from appearing as traffic. There must be at least 35 cars available to shuffle.
    If there are less than 5 cars available for any level after applying the blacklist, then traffic will not be shuffled."""
    display_name = "Traffic Blacklist"
    valid_keys = list(item_name_groups['Cars'])

class EjectTraps(Toggle):
    """Whether to include Eject traps in the item pool."""
    default = True
    display_name = "Enable Eject Traps"

class DuffTraps(Toggle):
    """Whether to include Duff traps in the item pool."""
    default = True
    display_name = "Enable Duff Traps"

class LaunchTraps(Toggle):
    """Whether to include Launch traps in the item pool."""
    default = True
    display_name = "Enable Launch Traps"

class HNRTraps(Toggle):
    """Whether to include Hit N Run traps in the item pool."""
    default = True
    display_name = "Enable Hit N Run Traps"

class TrafficTraps(Toggle):
    """Whether to include Traffic traps in the item pool."""
    default = True
    display_name = "Enable Traffic Traps"

class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps.
       These traps are IN ADDITION to any enabled traps above, though it won't add trap types that have been disabled."""
    display_name = "Filler Traps"
    range_end = 100

@dataclass
class SimpsonsHitNRunOptions(PerGameCommonOptions):
    Itchy_And_Scratchy_Ticket_Requirement: ISTicket
    Wasp_Amount: WaspAmount
    Card_Amount: CardAmount
    Required_Mission_Levels: RequiredMissionLevels
    Car_Amount: CarAmount
    Lock_Levels: LockLevels
    Early_Level: EarlyLevel
    Shuffle_Levels: ShuffleLevels
    Starting_Car_Shuffle: ShuffleStartingCar
    Shuffle_Attack: ShuffleAttack
    Shuffle_Jump: ShuffleJump
    Start_Jump_Level: StartingJumpLevel
    Shuffle_Gagfinder: ShuffleGagfinder
    Shuffle_Checkered_Flags: ShuffleCheckeredFlags
    Shuffle_EBrakes: ShuffleEBrakes
    Shuffle_Bumpers: ShuffleBumpers
    Start_With_Bumpers: StartWithBumpers
    Shuffle_Forward: ShuffleForward
    Early_Forward: EarlyForward
    Shuffle_Cards: ShuffleCards
    Mission_Locks: AddMissionLocks
    Mission_Timers: AdjustMissionTimers
    Min_Shop_Price: MinShopPrice
    Max_Shop_Price: MaxShopPrice
    Shop_Scale_Modifier: ShopScaleMod
    Start_Wallet_Level: StartingWalletLevel
    Shop_Hint_Policy: ShopHintPolicy
    Extra_Hint_Policy: ExtraHintPolicy
    Filler_Wrench_Efficiency: FillerWrenchEfficiency
    Filler_HitNRun_Reset_Efficiency: FillerHitNRunResetEfficiency
    Shuffle_Traffic: ShuffleTraffic
    Traffic_Blacklist: TrafficBlacklist
    Filler_Traps: FillerTrapPercent
    Enable_Eject_Traps: EjectTraps
    Enable_Duff_Traps: DuffTraps
    Enable_Launch_Traps: LaunchTraps
    Enable_HitNRun_Traps: HNRTraps
    Enable_Traffic_Traps: TrafficTraps


option_groups = [
    OptionGroup(
        "Shuffles",
        [ShuffleLevels, ShuffleStartingCar, ShuffleAttack, ShuffleJump, StartingJumpLevel, ShuffleGagfinder, ShuffleBumpers, StartWithBumpers, ShuffleCheckeredFlags, ShuffleEBrakes, ShuffleForward, EarlyForward, ShuffleCards],
    ),
    OptionGroup(
        "Goals",
        [ISTicket, WaspAmount, CardAmount, RequiredMissionLevels, CarAmount],
    ),
    OptionGroup(
        "Gameplay Changes",
        [AddMissionLocks, MinShopPrice, MaxShopPrice, ShopScaleMod, ShopHintPolicy, ExtraHintPolicy, ShuffleTraffic],
    ),
    OptionGroup(
        "Traps",
        [EjectTraps, DuffTraps, LaunchTraps, HNRTraps, TrafficTraps, FillerTrapPercent],
    )
]