"""
Option definitions for Paper Mario 64
"""

from Options import (
    Choice,
    Range,
    Toggle,
    DefaultOnToggle,
    FreeText,
    PerGameCommonOptions,
)
from dataclasses import dataclass


class ShuffleKeys(DefaultOnToggle):
    """If disabled, keys that are used within dungeons can only be found in their respective dungeons."""
    display_name = "Keysanity"


class ShuffleTradeEvents(Toggle):
    """Adds the 3 rewards obtained for doing the Trading Toad quests (started via Koopa Village's radio) into the item
    pool. These checks are available with 1, 3, and 5 star spirits saved."""
    display_name = "Include Trading Event Rewards"


class ShuffleHiddenPanels(Toggle):
    """Hidden panels can have any item; the star pieces normally hidden under them are added to the item pool. To flip
    hidden panels, you need Super Boots or Ultra Hammer."""
    display_name = "Include Hidden Panels"


class ShuffleDojoRewards(Range):
    """Number of Dojo fights with randomized rewards. The logic can only expect you to do the 2nd fight with 1 star
    spirit saved. The three Master fights are only in logic after you have 3, 4, and 5 star spirits saved."""
    display_name = "Dojo Rewards"
    range_start = 0
    range_end = 5
    default = 0


class ShuffleSuperMultiBlocks(Choice):
    """Off: Super Blocks and Multicoin blocks appear in their usual locations
    Shuffle: Shuffles the locations of the Super Blocks and Multicoin Brick Blocks together
    Anywhere: Multi coin blocks can be shuffled into non-block locations, which turns them into 'Coin Bag' items that
    grant you 10 coins."""
    display_name = "Shuffle Super/Multicoin Blocks"
    option_Off = 0
    option_Shuffle = 1
    option_Anywhere = 2


class GearShuffleMode(Choice):
    """Vanilla: Gear (Boots and Hammers) appear in their vanilla locations
    Gear Location Shuffle: Gear is shuffled amongst the upgrade chests and the bush in Jr. Troopa's playground
    Full Shuffle: Gear can be anywhere."""
    display_name = "Gear Shuffle"
    option_Vanilla = 0
    option_Gear_Location_Shuffle = 1
    option_Full_Shuffle = 2
    default = 2


class ShuffleLetters(Choice):
    """Vanilla: Letter rewards remain unshuffled.
    Vanilla Letter Chain: Shuffle delivery rewards, but don't shuffle anything in the long letter chain.
    Final Letter Chain Reward: Shuffle letter delivery rewards and the final reward of the long letter chain.
    Full shuffle: Every letter delivery reward is shuffled, effectively removing the letter
    chain as each letter in the chain is shuffled."""
    display_name = "Letter Delivery Rewards"
    option_Vanilla = 0
    option_Vanilla_Letter_Chain = 1
    option_Final_Letter_Chain_Reward = 2
    option_Full_Shuffle = 3


class ShuffleKootFavors(Choice):
    """Koopa Koot's Favors unlock after ridding the village of the Fuzzies, and three more are unlocked per star spirit
    saved up to 6 star spirits.
    Vanilla: Koopa Koot Favor rewards and quest items are unshuffled.
    Shuffle rewards: Shuffle the favor rewards, but not the key items for his quests.
    Full Shuffle: Shuffle the rewards AND the quest key items."""
    display_name = "Koopa Koot Favors"
    option_Vanilla = 0
    option_Shuffle_Rewards = 1
    option_Full_Shuffle = 2


class PartnerUpgradeShuffle(Choice):
    """Vanilla: Partners are upgraded through super blocks as usual.
    Super Block Locations: Super blocks are replaced by item blocks that give partner specific upgrade items.
    Full Shuffle: Super blocks are replaced with item blocks and specific partner upgrades are added as
    items in the pool."""
    display_name = "Partner Upgrades"
    option_Vanilla = 0
    option_Super_Block_Locations = 1
    option_Full_Shuffle = 2


class IncludeShops(DefaultOnToggle):
    """Shop items are included in the item pool.
    This includes regular item shops, Rowf's badge shop, and Merlow's star piece trade"""
    display_name = "Shopsanity"


class LogicRipCheatoItems(Range):
    """Number of items sold by Rip Cheato that can be required by logic.
    Items in logic will always be sold by him before the out of logic ones."""
    display_name = "Rip Cheato Items In Logic"
    range_start = 0
    range_end = 11
    default = 6


class LogicRowfItems(Range):
    """Determines how many sets of items sold by Rowf are candidates for progression items.
    He sells 4 items initially, and 3 more for each Star Spirit up to saved 4 Spirits, up to 16 total items.
    Note: You can talk to him and request he change his offerings."""
    display_name = "Rowf Items in Logic"
    range_start = 0
    range_end = 5
    default = 5


class LogicMerlowItems(Toggle):
    """Determines whether Merlow's Star Piece rewards can be required for progression. The items that you buy directly
    are never progression items. This is specifically for the rewards which are granted after spending X Star Pieces."""
    display_name = "Merlow Items in Logic"


class ShuffleOverworldCoins(Toggle):
    """Overworld coins are included in the item pool"""
    display_name = "Shuffle Overworld Coins"


class ShuffleFavorCoins(Toggle):
    """Coins from Koopa Koot's favor rewards are included in the item pool.
    Only has an effect when Koopa Koot's rewards are shuffled."""
    display_name = "Shuffle Favor Coins"


class ShuffleCoinBlocks(Toggle):
    """Single coin blocks are included in the item pool"""
    display_name = "Shuffle Coin Blocks"


class ShuffleFoliageCoins(Toggle):
    """Coins from bushes and trees are included in the item pool.
    It's recommended to turn on 'Foliage Item Hints' with this setting."""
    display_name = "Shuffle Foliage Coins"


class LocalConsumables(Range):
    """A percentage of consumable items will remain in the player's world instead of being shuffled into the multiworld.
    This can prevent other people from getting too many of your filler items, as well as make it easier to restock your
    inventory without farming items from enemies or using a potentially limited variety of consumables."""
    display_name = "Local Consumables Percentage"
    range_start = 0
    range_end = 100
    default = 100


# Partners
class ShufflePartners(Choice):
    """Partners become items in the item pool, and you get an item where you would normally get a partner."""
    display_name = "Shuffle Partners"
    option_Off = 0
    option_Partner_Locations = 1
    option_Full_Shuffle = 2


class PartnersAlwaysUsable(Toggle):
    """All partner field abilities are available to use even before you have unlocked them."""
    display_name = "Partners Always Usable"


class StartRandomPartners(DefaultOnToggle):
    """Start with a random set of partners."""
    display_name = "Start With Random Partners"


class StartPartners(Range):
    """Number of random partners you start with, from 1 to 8"""
    display_name = "Number of Starting Partners"
    range_start = 1
    range_end = 8
    default = 1


class StartWithGoombario(Toggle):
    """Have Goombario as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Goombario"


class StartWithKooper(Toggle):
    """Have Kooper as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Kooper"


class StartWithBombette(Toggle):
    """Have Bombette as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Bombette"


class StartWithParakarry(Toggle):
    """Have Parakarry as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Parakarry"


class StartWithBow(Toggle):
    """Have Bow as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Bow"


class StartWithWatt(Toggle):
    """Have Watt as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Watt"


class StartWithSushie(Toggle):
    """Have Sushie as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Sushie"


class StartWithLakilester(Toggle):
    """Have Lakilester as a starting partner. You must have at least one partner selected or be given a random one."""
    display_name = "Start With Lakilester"


class BadgeBPShuffle(Choice):
    """Vanilla: Badges have their original Badge Point (BP) costs.
    Balanced Random: Random BP costs 1-8, but weighted so most are +/-2 from vanilla.
    Shuffled: Original BP costs are shuffled together.
    Fully Random: Random BP costs from 1-6, unweighted."""
    display_name = "Badges BP"
    option_Vanilla = 0
    option_Balanced_Random = 1
    option_Shuffled = 2
    option_Fully_Random = 3


class BadgeFPShuffle(Choice):
    """Vanilla: Abilities granted by badges have their original Flower Point (FP) costs.
    Shuffled: Original FP costs are shuffled together.
    Balanced Random: Random FP costs 1-7, but weighted so most are +/-2 from vanilla.
    Fully Random: Random FP costs from 1-7, unweighted."""
    display_name = "Badges FP"
    option_Vanilla = 0
    option_Balanced_Random = 1
    option_Shuffled = 2
    option_Fully_Random = 3


class PartnerFPShuffle(Choice):
    """Vanilla: Partner special attacks have their original Flower Point (FP) costs.
    Shuffled: Original FP values are shuffled together.
    Balanced Random: Random FP values 1-8, but weighted so most are +/-2 from vanilla.
    Fully Random: Random FP values from 1-8, unweighted."""
    display_name = "Partners FP"
    option_Vanilla = 0
    option_Balanced_Random = 1
    option_Shuffled = 2
    option_Fully_Random = 3


class SPShuffle(Choice):
    """Vanilla: Star Spirit abilities have their original Star Power (SP) costs.
    Shuffled: Original SP costs are shuffled together.
    Balanced Random: Random SP costs 1-3, but weighted so most are +/-1 from vanilla.
    Fully Random: Random SP costs from 1-3, unweighted."""
    display_name = "SP Costs"
    option_Vanilla = 0
    option_Balanced_Random = 1
    option_Shuffled = 2
    option_Fully_Random = 3


class MysteryShuffle(Choice):
    """Vanilla: Mystery will pull from the vanilla item pool (one of six basic items).
    Random Pick: Mystery will be a random item for the full playthrough.
    Random Per Use: Mystery will be a random item on every use."""
    display_name = "Mystery"
    option_Vanilla = 0
    option_Random_Pick = 1
    option_Random_Per_Use = 2


class ShuffleBattleFormations(Toggle):
    """Shuffles which enemies you encounter and in what number.
    Enemies are limited to those that normally appear in the area."""
    display_name = "Shuffle Battle Formations"


class RandomPuzzles(Toggle):
    """Randomizes most of the game's puzzles.
    See https://github.com/icebound777/PMR-SeedGenerator/wiki/Random-Puzzles for a full list."""
    display_name = "Randomize Puzzles"


class BossShuffle(Toggle):
    """Shuffles end of chapter bosses. While enabled, Mario can run on the first turn of a boss battle.
    Note: This is not yet implemented and will fail to generate if set to True."""
    display_name = "Shuffle Bosses"


class BlooperDamageRequirements(Choice):
    """There are 3 Blooper fights. Regardless of what order you visit the fight locations, you always fight Blooper,
    then Electro Blooper, then Super Blooper. This setting can add logic such that you are able to deal enough damage
    per turn with jump and partner attacks to comfortably defeat all 3 Bloopers before needing to defeat any of them.
    Note that damage is calculated only by partners and boot upgrades, not badges or partner upgrades/abilities.
    None: No logical requirements to defeat Bloopers
    Low: 3 damage per turn required
    Medium: 6 damage per turn required
    High: 9 damage per turn required"""
    display_name = "Blooper Damage Requirements"
    option_None = 0
    option_Low = 1
    option_Medium = 2
    option_High = 3


# Difficulty settings
class EnemyDifficulty(Choice):
    """Vanilla: Original enemy stats.
    Shuffle Chapter Difficulty: Each chapter is assigned a new number, enemies are scaled accordingly.
    Progressive Scaling: Enemies scale as Mario gains more progression items and partners."""
    display_name = "Enemy Difficulty"
    option_Vanilla = 0
    option_Shuffle_Chapter_Difficulty = 1
    option_Progressive_Scaling = 2
    default = 2


class EnemyDamage(Choice):
    """Increases the damage done by enemy attacks."""
    display_name = "Enemy Difficulty"
    option_Normal = 1
    option_Double_Pain = 2
    option_Quadruple_Pain = 4
    default = option_Normal


class OneHitKO(Toggle):
    """Mario will die instantly from an enemy attack if a block action command is failed"""
    display_name = "One Hit KO"


class XPMultiplier(Range):
    """Increase or decrease the star points gained from enemies. Double the desired value for this setting.
    ex: if you want double XP, set this to 4; for vanilla XP, set this to 2"""
    display_name = "XP Multiplier"
    range_start = 0
    range_end = 4
    default = 2


class CapEnemyXP(Toggle):
    """Limits the amount of XP per defeated enemy to 5."""
    display_name = "Cap Enemy XP"


class DropStarPoints(Toggle):
    """Mario will drop star points when running away from battle.
    Equipping the Runaway Pay badge will prevent him from dropping star points."""
    display_name = "Drop Star Points"


class NoHeartBlocks(Toggle):
    """Remove heart blocks from the game"""
    display_name = "No Heart Blocks"


class NoSaveBlocks(Toggle):
    """Remove save blocks from the game. You can still save at the end of each chapter."""
    display_name = "No Save Blocks"


class NoHealingItems(Toggle):
    """HP/FP restoring items will have no effect."""
    display_name = "No Healing Items"


class BadgeSynergy(Toggle):
    """Increases Mario's attack power with boots or hammer attacks the more badges of similar type he wears."""
    display_name = "No Healing Items"


class MerlowRewardsPricing(Choice):
    """Cheap: Rewards every 5 star pieces spent, up to 30 total.
    Normal: Rewards every 10 star pieces spent, up to 60 total."""
    display_name = "Merlow Rewards Pricing"
    option_Cheap = 0
    option_Vanilla = 1


class ChetRippoAvailable(Toggle):
    """Determines if Chet Rippo, the shady NPC who you can pay to reallocate Mario's stats, appears in Toad Town."""
    display_name = "Chet Rippo Available"


class BowserDoorQuiz(Choice):
    """Quiz: The second Bowser door in Bowser's castle has a quiz. Pass it or be forced to fight the anti-guy unit.
    Anti Guys Unit: The second Bowser door in Bowser's castle has no quiz; you must fight the anti guys unit.
    Skip: The second Bowser door in Bowser's castle is open as though the quiz has already been completed."""
    display_name = "Bowser Door Quiz"
    option_Quiz = 0
    option_Anti_Guys_Unit = 1
    option_Skip = 2


class KentCKoopa(Choice):
    """Blocks Pleasant Path: You must pay 50 coins or defeat him to get into Pleasant Path.
    Must Defeat: You must defeat him to get into Pleasant Path. Expects two chapters completed and a way to flip him.
    Already Paid: Stands on the side of Pleasant Path as if already paid.
    Already Defeated: Removed from Pleasant Path as if already defeated."""
    display_name = "Kent C. Koopa"
    option_Blocks_Pleasant_Path = 0
    option_Must_Defeat = 1
    option_Already_Paid = 2
    option_Already_Defeated = 3


class SeedGoal(Choice):
    """Defeat Bowser: The game is complete once you've defeated Bowser to take back the Star Rod.
    Open Star Way: The game is complete once you've fulfilled the requirements to open Star Way"""
    display_name = "Seed Goal"
    option_Defeat_Bowser = 0
    option_Open_Star_Way = 1


class PowerStarHunt(Toggle):
    """Adds power stars into the item pool. You must collect a certain amount and give them to Eldstar at
    Shooting Star Summit to open up Star Way. """
    display_name = "Power Star Hunt"


class StarWaySpiritsRequired(Range):
    """Number of star spirits required to open up Star Way and access Chapter 8.
    Access requirements will also include power stars if Power Star Hunt is turned on."""
    display_name = "Spirits Required for Star Way"
    range_start = 0
    range_end = 7
    default = 5


class SpiritRequirements(Choice):
    """Determines if specific spirits are needed to open star way.
    Any: Any spirits can open Star Way.
    Specific: A set of specific spirits open Star Way. You can find which are required by visiting Shooting Star Summit.
    Specific and Limit Chapter Logic: Progression items will be limited to prologue, common areas, and areas in required
    chapters."""
    display_name = "Required Spirits"
    option_Any = 0
    option_Specific = 1
    option_Specific_And_Limit_Chapter_Logic = 2


class LimitChapterLogic(Toggle):
    """Progression items will only appear in required chapters, the prologue, and in common areas. You will not need to
    check the chapters that are out of logic whatsoever, and the checks in those chapters will not grant you
    hint points. You can still visit them for local items (badges, consumables, etc) if you want or need to."""
    display_name = "Limit Chapter Logic"


class ShuffleStarBeam(Toggle):
    """Star Beam becomes an item shuffled in the item pool. Another random item will replace Star Beam in Star Haven.
    Upon reaching the first Bowser fight in Peach's Castle, he will tell you where Star Beam is."""
    display_name = "Shuffle Star Beam"


class StarBeamSpiritsRequired(Range):
    """Number of star spirits required to obtain the item in the Star Beam location in Star Sanctuary.
    Forced to 0 when Limit Chapter Logic is active."""
    display_name = "Spirits Required for Star Beam"
    range_start = 0
    range_end = 7
    default = 0


class StarWayPowerStarsRequired(Range):
    """Number of power stars required to open up Star Way and access Chapter 8."""
    display_name = "Power Stars Required for Star Way"
    range_start = 0
    range_end = 120
    default = 50


class StarBeamPowerStarsRequired(Range):
    """Number of power stars required to be gifted the Star Beam in Star Sanctuary"""
    display_name = "Power Stars Required for Star Beam"
    range_start = 0
    range_end = 120
    default = 50


class TotalPowerStars(Range):
    """Number of power stars placed in the game world. Must be more than the "Required Power Stars".
    It's recommended that this is around 1.5 times the number of required stars."""
    display_name = "Total Power Stars"
    range_start = 0
    range_end = 120
    default = 70


# Difficulty Stats and Gear
class StartingBoots(Choice):
    """Level of the boots that Mario will start the game with.
    Note: While jumpless, you can still climb up some places with Parakarry.
    You can also hit floating blocks by using Kooper's ability beneath them."""
    display_name = "Starting Boots"
    option_Jumpless = -1
    option_Normal = 0
    option_Super = 1
    option_Ultra = 2


class StartingHammer(Choice):
    """Level of the hammer that Mario will start the game with.
    Note: Without hammer, you can still hit trees and break yellow blocks using Bombette's ability."""
    display_name = "Starting Hammer"
    option_Hammerless = -1
    option_Normal = 0
    option_Super = 1
    option_Ultra = 2


class StartingCoins(Range):
    """Amount of coins Mario will start the game with.
    Note: You will need to pay 50 coins to get past Kent C Koopa on the way to Koopa Village. It's recommended that you
    don't spend all your coins before paying him off."""
    display_name = "Starting Coins"
    range_start = 0
    range_end = 999
    default = 150


class StartingHP(Range):
    """Amount of Health Points Mario will start the game with
    Note: Mario must have at least one starting stat raised past its initial value (5 for HP and FP, 3 for BP)"""
    display_name = "Starting HP"
    range_start = 5
    range_end = 50
    default = 10
    increment = 5


class StartingFP(Range):
    """Amount of Flower Points Mario will start the game with
    Note: Mario must have at least one starting stat raised past its initial value (5 for HP and FP, 3 for BP)"""
    display_name = "Starting FP"
    range_start = 5
    range_end = 50
    default = 5
    increment = 5


class StartingBP(Range):
    """Amount of Badge Points Mario will start the game with
    Note: Mario must have at least one starting stat raised past its initial value (5 for HP and FP, 3 for BP)"""
    display_name = "Starting BP"
    range_start = 3
    range_end = 30
    default = 3
    increment = 3


class RandomStartingStats(Toggle):
    """Instead of choosing starting stats, you can have them randomized based on a chosen starting level.
    Setting this to true will overwrite the starting BP, HP, and FP stat settings
    Base stats are 5 HP, 5 FP, and 3 BP, with each level raising one of these at random"""
    display_name = "Random Starting Stats"


class RandomStartingStatsLevel(Range):
    """When random starting stats is true, this changes what level (1-27) Mario starts at.
    Starting stats will be randomly distributed and will overwrite the starting HP, FP, and BP stat settings"""
    display_name = "Random Starting Stats Level"
    range_start = 1
    range_end = 27
    default = 1


class StartingSP(Range):
    """Amount of Star Power Mario will start the game with.
    Starting with SP allows Mario to use star powers, which will be cast by Twink until star spirits are saved."""
    display_name = "Starting SP"
    range_start = 0
    range_end = 7
    default = 0


# Difficulty Starting Items
class RandomStartItems(Range):
    """Number of random items you want to start with."""
    display_name = "Random Starting Items"
    range_start = 0
    range_end = 16
    default = 0


# Difficulty Item Pool
class ConsumableItemPool(Choice):
    """Vanilla: Original consumable items.
    Mystery Only: All consumables are replaced by Mystery.
    Fully Random: Consumables are completely random.
    Balanced Random: Consumables are randomized and balanced according to Balanced Random Item Quality."""
    display_name = "Consumable Item Pool"
    option_Vanilla = 0
    option_Fully_Random = 1
    option_Balanced_Random = 2
    option_Mystery_Only = 3


class ConsumableItemQuality(Range):
    """Sets how powerful consumable items should be on average, where a higher % means better items.
    100% is the strength of the vanilla item pool."""
    display_name = "Consumable Item Quality (%)"
    range_start = 25
    range_end = 125
    default = 100
    increment = 25


class ProgressiveBadges(Toggle):
    """Badges that come in different power levels are changed to progressive badges.
    This affects jump/hammer charge, power and mega jump/hammer, and quake hammer.
    Intermediate beta badges are included for the involved badge families even if beta badges are turned off."""
    display_name = "Progressive Badges"


class ItemPouches(Toggle):
    """Adds 5 item pouches into the item pool. Every pouch found increases Mario's inventory size by 2.
    This increases total inventory size from 10 items up to a maximum of 20."""
    display_name = "Add Item Pouches"


class UnusedBadgeDupes(Toggle):
    """Adds unused duplicates of badges that can stack into the item pool."""
    display_name = "Add Unused Badge Duplicates"


class BetaItems(Toggle):
    """Adds unused beta badges and consumable items into the item pool."""
    display_name = "Add Beta Items"


class BadgePoolLimit(Range):
    """Sets the max amount of badges that can be in the item pool. There are 80 badges in vanilla."""
    display_name = "Badge Pool Limit"
    range_start = 0
    range_end = 128
    default = 128


class ItemTraps(Choice):
    """Replaces some items with fakes that deal 2 damage upon contact."""
    display_name = "Item Traps"
    option_No_Traps = 0
    option_Sparse = 1
    option_Moderate = 2
    option_Plenty = 3


# World settings
class StartingMap(Choice):
    """Sets the town/village where the game starts.
    This is also where the Homeward Shroom warps Mario.
    You may use the warp shroom from the key items menu in the overworld."""
    display_name = "Starting Location"
    option_Toad_Town = 0
    option_Goomba_Village = 1
    option_Dry_Dry_Outpost = 2
    option_Yoshi_Village = 5


class OpenPrologue(Toggle):
    """When enabled, Goomba King starts off defeated and the bridge to reach Goomba Village will be open from the start.
    When starting from anywhere other than Goomba Village, this will mean having to reach the village via sewers."""
    display_name = "Open Prologue"


class OpenMtRugged(Toggle):
    """When enabled, the boulder blocking the train from going to Mt. Rugged will be gone from the start.
    When disabled, you will have to use Bombette to blow up the boulder."""
    display_name = "Open Mt. Rugged"


class OpenForest(Toggle):
    """When enabled, Oakley allows you through Forever Forest with no requirements.
    When disabled, Oakley only allows you through once you have a Forest Pass (added randomizer item), and Fice T's
    cutscene will have an item check.
    """
    display_name = "Open Forest"


class OpenToybox(Toggle):
    """When enabled, you can open the door to enter Shy Guy's Toy Box from the start.
    When disabled, you will have to use Bow to hide from the Shy Guy to enter Shy Guy's Toy Box for the first time."""
    display_name = "Open Toy Box"


class OpenWhale(Toggle):
    """When enabled, you can ride the whale to Lavalava Island from the start.
    When disabled, you will have to use Watt to catch and defeat Fuzzipede in order to ride the whale."""
    display_name = "Open Whale"


class MagicalSeedsRequired(Range):
    """The amount of Magical Seeds required to open the gate to Flower Fields. Changing this does not remove the
    Bub-ulb checks."""
    display_name = "Magical Seeds Required"
    range_start = 0
    range_end = 4
    default = 4


class OpenBlueHouse(Toggle):
    """When enabled, the door to the Blue House in Toad Town's Southern District is unlocked from the start
    and the Odd Key is removed from the item pool.
    When disabled, you will have to use the Odd Key to open the Blue House door."""
    display_name = "Open Blue House"


class Chapter7BridgeVisible(Toggle):
    """When enabled, blocks leading to Shiver City are visible and can be hit from above with Super Boots.
    When disabled, they will be invisible and you will have to hit them from below with Ultra Boots."""
    display_name = "Ch.7 Bridge Visible"


class MirrorMode(Choice):
    """Off: The overworld is never mirrored.
    Always On: The overworld is always mirrored.
    Random On Every Load: Whether the overworld is mirrored or not is random with every screen transition.
    Static Random: Some overworld screens are mirrored, some are not, but they won't change within a playthrough.
    Note: The Static Random option is not yet implemented and will fail to generate."""
    display_name = "Mirror Mode"
    option_Off = 0
    option_Always_On = 1
    option_Random_On_Every_Load = 2
    option_Static_Random = 3


class BowserCastleMode(Choice):
    """Vanilla: Mario will need to go through the entire castle, requiring 5 keys and most partner abilities.
    Shortened: Multiple sections of Bowser's Castle will be skipped. No keys or partner abilities will be required.
    Boss Rush: The entire castle will be skipped until the hallway where you fight the Duplighosts."""
    display_name = "Bowser's Castle Mode"
    option_Vanilla = 0
    option_Shortened = 1
    option_Boss_Rush = 2


class ShuffleDungeonEntrances(Choice):
    """Shuffles the main entrance of every chapter dungeon. You can also choose to include Bowser's Castle's entrance.
    Note: This is not yet implemented and will fail to generate if set to True."""
    display_name = "Dungeon Entrance Shuffle"
    option_Off = 0
    option_Only_Spirit_Dungeons = 1
    option_Include_Bowsers_Castle = 2


# QoL settings
class HiddenBlockMode(Choice):
    """Vanilla: Hidden blocks are only visible while using Watt's ability.
    Watt Out: Hidden blocks are visible when Watt is your active partner, even without using her ability.
    Watt Obtained: Hidden blocks are always visible after you have obtained Watt as a partner.
    Always Visible: Hidden blocks are always visible."""
    display_name = "Hidden Block Mode"
    option_Vanilla = 0
    option_Watt_Out = 1
    option_Watt_Obtained = 2
    option_Always_Visible = 3


class PreventOOBLZS(Toggle):
    """When enabled, prevents out of bound and loading zone storage tricks. This setting does NOT affect logic.
    Warning: in some cases, attempting OOB exploits with this enabled can cause softlocks since the game fails to
    properly reset Mario's position."""
    display_name = "Prevent OOB/LZS Tricks"


class SkipQuiz(DefaultOnToggle):
    """When enabled, quiz rewards will be handed out without having to answer questions."""
    display_name = "Skip Quiz"


class QuizmoAlwaysAppears(DefaultOnToggle):
    """When enabled, Chuck Quizmo always appears somewhere in town until his location questions have been answered."""
    display_name = "Quizmo Always Appears"


class VisibleHiddenPanels(DefaultOnToggle):
    """When enabled, hidden panels will have an altered appearance to make identifying them easier.
    Recommended for players not familiar with every single hidden panel locations when shuffling hidden panels."""
    display_name = "Visible Hidden Panels"


class CutsceneMode(Choice):
    """Vanilla: Cutscenes from the original game are preserved.
    Shortened: Cutscenes are quicker but preserved with some condensed dialogue.
    Minimal: Most cutscenes and dialogues are removed."""
    display_name = "Cutscene Mode"
    option_Vanilla = 0
    option_Shortened = 1
    option_Minimal = 2
    default = 1


class AlwaysSpeedySpin(DefaultOnToggle):
    """When enabled, Mario will always spin fast when pressing Z without needing to equip the Speedy Spin badge.
    The Speedy Spin badge is also removed from the item pool."""
    display_name = "Always Speedy Spin"


class AlwaysPeekaboo(DefaultOnToggle):
    """When enabled, you will always be able to see enemy's HP bars without needing to equip the Peekaboo badge.
    The Peekaboo badge is also removed from the item pool."""
    display_name = "Always Peekaboo"


class AlwaysISpy(DefaultOnToggle):
    """When enabled, you will always get an indicator if you enter a room with a hidden panel without needing to equip
    the I Spy badge. The sound effect is removed, so it is only a visual cue.
    The I Spy badge is also removed from the item pool.
    Recommended for players not familiar with every single hidden panel locations when shuffling hidden panels."""
    display_name = "Always I Spy"


class ISpyPanelHints(Choice):
    """Off: Don't show panel hints.
    Vague: Display a generic item sprite based on the type of item inside the panel (e.g. badge, star piece, key item).
    Concrete: Display the exact sprite of the item inside the panel."""
    display_name = "I Spy Panel Hints"
    option_Off = 0
    option_Vague = 1
    option_Concrete = 2


class FoliageItemHints(DefaultOnToggle):
    """When enabled, bushes and trees will emit a glow when they are hiding something."""
    display_name = "Foliage Item Hints"


class CookWithoutFryingPan(Toggle):
    """When enabled, allows Tayce T. to cook for you without first finding the frying pan.
    When disabled, you will have to find the frying pan before Tayce T. can cook anything for you."""
    display_name = "Cook Without Frying Pan"


class SkipEpilogue(DefaultOnToggle):
    """When enabled, the game will skip directly to credits once you have acquired the Star Rod."""
    display_name = "Skip Epilogue"


# Cosmetic settings
class MarioColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Mario's Color Palette"
    option_Default = 0
    option_Luigi = 1
    option_Wario = 2
    option_Waluigi = 3
    option_Fire = 4
    option_Ice = 5
    option_Maker = 6
    option_Classic = 7
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class GoombarioColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Goombario's Color Palette"
    option_Default = 0
    option_Green = 1
    option_Red = 2
    option_Yellow = 3
    option_Blue = 4
    option_Grey = 5
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class KooperColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Kooper's Color Palette"
    option_Default = 0
    option_Green = 1
    option_Red = 2
    option_Purple = 3
    option_Grey = 4
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class BombetteColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Bombette's Color Palette"
    option_Default = 0
    option_Orange = 1
    option_Green = 2
    option_Yellow = 3
    option_Blue = 4
    option_Red = 5
    option_Purple = 6
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class ParakarryColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Parakarry's Color Palette"
    option_Default = 0
    option_Green = 1
    option_Red = 2
    option_Purple = 3
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class BowColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Bow's Color Palette"
    option_Default = 0
    option_Red = 1
    option_Pink = 2
    option_Blue = 3
    option_Grey = 4
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class WattColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Watt's Color Palette"
    option_Default = 0
    option_Blue = 1
    option_Pink = 2
    option_Green = 3
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class SushieColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Sushie's Color Palette"
    option_Default = 0
    option_Red = 1
    option_Yellow = 2
    option_Green = 3
    option_Blue = 4
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class LakilesterColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Lakilester's Color Palette"
    option_Default = 0
    option_Blue = 1
    option_Dark = 2
    option_Red = 3
    option_Green = 4
    option_Random_Pick = 10
    option_Random_Pick_No_Vanilla = 11
    option_Random_On_Every_Load = 12


class BossColorPalette(Choice):
    """Changes the way the sprites look in-game."""
    display_name = "Bosses Color Palettes"
    option_Default = 0
    option_Random_Pick = 2
    option_Random_Pick_No_Vanilla = 3
    option_Random_On_Every_Load = 4


class NPCColorPalette(Choice):
    """Changes the way the sprites look in-game."""
    display_name = "NPC Color Palettes"
    option_Default = 0
    option_Random_Pick = 2
    option_Random_Pick_No_Vanilla = 3
    option_Random_On_Every_Load = 4


class EnemyColorPalette(Choice):
    """Changes the way the sprites look in-game."""
    display_name = "Enemy Color Palettes"
    option_Default = 0
    option_Random_Pick = 2
    option_Random_Pick_No_Vanilla = 3
    option_Random_On_Every_Load = 4


class HammerColorPalette(Choice):
    """Changes the way the sprite looks in-game."""
    display_name = "Hammer Color Palette"
    option_Default = 0
    option_Random_Pick = 2
    option_Random_Pick_No_Vanilla = 3
    option_Random_On_Every_Load = 4


class StatusMenuColorPalette(Choice):
    """Changes the way the status menu at the top of the screen looks in-game."""
    display_name = "Status Menu Color Palette"
    option_Default = 0
    option_Blue = 1
    option_Green = 2
    option_Teal = 3
    option_Brown = 4
    option_Purple = 5
    option_Grey = 6
    option_Random_Pick = 7
    option_Animated = 8


class CoinColorPalette(Choice):
    """Changes the way the sprites look in-game."""
    display_name = "Coin Color Palette"
    option_Default = 0
    option_Red = 1
    option_Blue = 2
    option_Purple = 3
    option_Silver = 4


class RandomText(Toggle):
    """When enabled, all text in the game will be randomized."""
    display_name = "Random Text"


class RomanNumerals(Toggle):
    """When enabled, enemy HP bars will use roman numerals."""
    display_name = "Roman Numerals"


class ShuffleMusic(Choice):
    """Shuffles the different songs in the game.
    Shuffle By Mood: Songs will be shuffled within groups of similar moods such as relaxed, upbeat, battle.
    Shuffle By Type: Songs will be shuffled within groups of similar types such as overworld, battle, event.
    Full Shuffle: Any song can play anywhere in the game."""
    display_name = "Shuffle Music"
    option_Off = -1
    option_Shuffle_By_Mood = 0
    option_Shuffle_By_Type = 1
    option_Full_Shuffle = 2
    default = -1


class ShuffleJingles(Toggle):
    """When enabled, shuffles the different short music jingles in the game."""
    display_name = "Shuffle Jingles"


class RandomPitch(Toggle):
    """When enabled, randomizes the pitch of the game's music and sounds."""
    display_name = "Random Pitch"


class MuteDangerBeeps(Toggle):
    """When enabled, mutes the sound effect that plays when Mario is in danger."""
    display_name = "Mute Danger Beeps"


class PMRSiteSettingsString(FreeText):
    """Put a value for this if grabbing the settings string from https://pm64randomizer.com/. Keep in mind not to use
    settings specific to base PMR, and that AP-specific settings not on the site will keep their default values.
    If you aren't using the site to get your settings, leave this as 'None'."""
    display_name = "PMR Settings String"
    default = "None"


@dataclass
class PaperMarioOptions(PerGameCommonOptions):
    # Items
    keysanity: ShuffleKeys
    shuffle_hidden_panels: ShuffleHiddenPanels
    gear_shuffle_mode: GearShuffleMode
    trading_events: ShuffleTradeEvents
    koot_favors: ShuffleKootFavors
    koot_coins: ShuffleFavorCoins
    overworld_coins: ShuffleOverworldCoins
    foliage_coins: ShuffleFoliageCoins
    coin_blocks: ShuffleCoinBlocks
    include_shops: IncludeShops
    dojo: ShuffleDojoRewards
    partner_upgrades: PartnerUpgradeShuffle
    letter_rewards: ShuffleLetters
    super_multi_blocks: ShuffleSuperMultiBlocks
    rowf_items: LogicRowfItems
    merlow_items: LogicMerlowItems
    cheato_items: LogicRipCheatoItems
    local_consumables: LocalConsumables

    # Partner
    partners: ShufflePartners
    partners_always_usable: PartnersAlwaysUsable
    start_random_partners: StartRandomPartners
    start_partners: StartPartners
    start_with_goombario: StartWithGoombario
    start_with_kooper: StartWithKooper
    start_with_bombette: StartWithBombette
    start_with_parakarry: StartWithParakarry
    start_with_bow: StartWithBow
    start_with_watt: StartWithWatt
    start_with_sushie: StartWithSushie
    start_with_lakilester: StartWithLakilester

    # Gameplay
    badge_bp_shuffle: BadgeBPShuffle
    badge_fp_shuffle: BadgeFPShuffle
    partner_fp_shuffle: PartnerFPShuffle
    sp_shuffle: SPShuffle
    mystery_shuffle: MysteryShuffle
    formation_shuffle: ShuffleBattleFormations
    random_puzzles: RandomPuzzles
    boss_shuffle: BossShuffle
    blooper_damage_requirements: BlooperDamageRequirements

    # General Difficulty
    enemy_difficulty: EnemyDifficulty
    enemy_damage: EnemyDamage
    cap_enemy_xp: CapEnemyXP
    enemy_xp_multiplier: XPMultiplier
    no_save_blocks: NoSaveBlocks
    no_heart_blocks: NoHeartBlocks
    no_healing_items: NoHealingItems
    one_hit_ko: OneHitKO
    drop_star_points: DropStarPoints
    badge_synergy: BadgeSynergy
    merlow_rewards_pricing: MerlowRewardsPricing
    chet_rippo: ChetRippoAvailable
    bowser_door_quiz: BowserDoorQuiz
    kent_c_koopa: KentCKoopa

    # Goals
    seed_goal: SeedGoal
    power_star_hunt: PowerStarHunt
    spirit_requirements: SpiritRequirements
    star_way_spirits: StarWaySpiritsRequired
    star_way_power_stars: StarWayPowerStarsRequired
    shuffle_star_beam: ShuffleStarBeam
    star_beam_spirits: StarBeamSpiritsRequired
    star_beam_power_stars: StarBeamPowerStarsRequired
    total_power_stars: TotalPowerStars

    # Stats and Gear
    starting_boots: StartingBoots
    starting_hammer: StartingHammer
    starting_coins: StartingCoins
    starting_hp: StartingHP
    starting_bp: StartingBP
    starting_fp: StartingFP
    starting_sp: StartingSP
    random_start_items: RandomStartItems
    random_start_stats: RandomStartingStats
    random_start_stats_level: RandomStartingStatsLevel

    # Item Pool
    consumable_item_pool: ConsumableItemPool
    consumable_item_quality: ConsumableItemQuality
    item_traps: ItemTraps
    item_pouches: ItemPouches
    unused_badge_dupes: UnusedBadgeDupes
    beta_items: BetaItems
    progressive_badges: ProgressiveBadges
    badge_pool_limit: BadgePoolLimit

    # World Settings
    starting_map: StartingMap
    open_prologue: OpenPrologue
    open_mt_rugged: OpenMtRugged
    open_forest: OpenForest
    magical_seeds: MagicalSeedsRequired
    open_toybox: OpenToybox
    open_whale: OpenWhale
    open_blue_house: OpenBlueHouse
    ch7_bridge_visible: Chapter7BridgeVisible
    mirror_mode: MirrorMode
    bowser_castle_mode: BowserCastleMode
    shuffle_dungeon_entrances: ShuffleDungeonEntrances

    # Quality of Life Settings
    hidden_block_mode: HiddenBlockMode
    prevent_ooblzs: PreventOOBLZS
    skip_quiz: SkipQuiz
    quizmo_always_appears: QuizmoAlwaysAppears
    visible_hidden_panels: VisibleHiddenPanels
    always_speedy_spin: AlwaysSpeedySpin
    always_peekaboo: AlwaysPeekaboo
    always_ispy: AlwaysISpy
    ispy_panel_hints: ISpyPanelHints
    foliage_item_hints: FoliageItemHints
    cook_without_frying_pan: CookWithoutFryingPan
    cutscene_mode: CutsceneMode
    skip_epilogue: SkipEpilogue

    # Cosmetics
    mario_palette: MarioColorPalette
    goombario_palette: GoombarioColorPalette
    kooper_palette: KooperColorPalette
    bombette_palette: BombetteColorPalette
    parakarry_palette: ParakarryColorPalette
    bow_palette: BowColorPalette
    watt_palette: WattColorPalette
    sushie_palette: SushieColorPalette
    lakilester_palette: LakilesterColorPalette
    boss_palette: BossColorPalette
    npc_palette: NPCColorPalette
    enemy_palette: EnemyColorPalette
    hammer_palette: HammerColorPalette
    status_menu_palette: StatusMenuColorPalette
    coin_palette: CoinColorPalette
    random_text: RandomText
    roman_numerals: RomanNumerals

    # Audio
    shuffle_music: ShuffleMusic
    shuffle_jingles: ShuffleJingles
    random_pitch: RandomPitch
    mute_danger_beeps: MuteDangerBeeps

    pmr_settings_string: PMRSiteSettingsString
