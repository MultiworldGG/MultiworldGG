from dataclasses import dataclass

from Options import Choice, DeathLinkMixin, OptionSet, PerGameCommonOptions, Range, Toggle

from .constants import (
    ABYSSAL_TERRORS_CHARACTERS,
    BASE_GAME_CHARACTERS,
    MAX_LEGENDARY_CRATE_DROP_GROUPS,
    MAX_LEGENDARY_CRATE_DROPS,
    MAX_NORMAL_CRATE_DROP_GROUPS,
    MAX_NORMAL_CRATE_DROPS,
    MAX_REQUIRED_RUN_WINS,
    MAX_SHOP_SLOTS,
    NUM_WAVES,
    TOTAL_NUM_CHARACTERS,
)


class NumberRequiredWins(Range):
    """The number of runs you need to win to complete your goal.

    Each win must be done with a different character.
    """

    range_start = 1
    range_end = MAX_REQUIRED_RUN_WINS

    default = 10
    display_name = "Wins Required"


class NumberCharacters(Range):
    """The total number of characters in the world.

    The characters will be randomly selected from the valid characters determined by the "Include Characters" options.

    The actual number of characters may be less if there are not enough included characters in the options.
    """

    range_start = 1
    range_end = TOTAL_NUM_CHARACTERS

    default = 15
    display_name = "Number of Included Characters"


class StartingCharacters(Choice):
    """Determines your set of starting characters.

    Characters omitted from "Include Characters" will not be included regardless of this option.

    If a DLC option is chosen but the DLC is not enabled, an error will be raised during generation.

    * Default All: Start with the default characters from the base game and all enabled DLCs.
    * Random All: Start with random characters chosen from the base game and all enabled DLCs.
    * Default Base Game: Start with Well Rounded, Brawler, Crazy, Ranger and Mage.
    * Random Base Game: Start with random characters from the base game only.
    * Default Abyssal Terrors: Start with Sailor, Curious, Builder, Captain, and Creature.
    * Random Abyssal Terrors: Start with random characters from the Abyssal Terrors DLC.
    """

    option_default_all = 0
    option_random_all = 1
    option_default_base_game = 2
    option_random_base_game = 3
    option_default_abyssal_terrors = 4
    option_random_abyssal_terrors = 5

    default = 0
    display_name = "Starting Characters"


class NumberStartingCharacters(Range):
    """The number of random characters to start with.

    This is ignored if "Starting Characters" is set to any of the "Default <x>" options, and is clamped to the maximum
    number of characters in the enabled DLCs.
    """

    range_start = 1
    range_end = TOTAL_NUM_CHARACTERS

    default = 5
    display_name = "Number of Starting Characters"


class IncludeBaseGameCharacters(OptionSet):
    """Which base game characters to include for checks.

    Characters not listed here will not be available to play. There will be no item to unlock them, and there will be
    no run or wave complete checks associated with them.
    """

    default = frozenset(BASE_GAME_CHARACTERS.characters)
    display_name = "Include Base Game Characters"
    valid_keys = BASE_GAME_CHARACTERS.characters


class WavesPerCheck(Range):
    """How many waves to win to receive a check.

    1 means every wave is a check, 2 means every other wave, etc.
    """

    # We'd make the start 1, but the number of items sent when the game is released is
    # so large that the resulting ReceivedItems command is bigger than Godot 3.5's
    # hard-coded WebSocket buffer can fit, meaning the engine silently drops it.
    range_start = 1
    range_end = NUM_WAVES

    default = 10
    display_name = "Waves Per Check"


class NumWaveCaps(Choice):
    """The number of caps to put on the accessible waves.

    You will not be able to play beyond the maximum wave cap until you find additional
    Progressive Wave Cap items.

    With one cap, all waves are accessible from the start.

    With two caps, waves 1-10 are accessible from the start, and waves 11-20 require one
    Progressive Wave Cap.

    With four caps: waves 1-5 are accessible from the start, waves 6-10 require one
    Progressive Wave Cap, waves 11-15 require two, waves 16-20 require 3.
    """

    option_one = 0
    option_two = 2
    option_four = 4
    option_ten = 10
    option_twenty = 20

    default = 2
    display_name = "Number of Progressive Wave Caps"


class GoldRewardMode(Choice):
    """Chooses how gold rewards are given.

    #. One Time: Gold items are only given once, in either the current run or the next run after receiving the item.
    #. All Every Time: The total amount of gold received is given to the player at the start of every run. Since gold is
       a filler item, this can lead to the game being "won" very easily early on in larger multiworlds.
    """

    option_one_time = 0
    option_all_every_time = 1

    default = 0
    display_name = "Gold Reward Mode"


class XpRewardMode(Choice):
    """Chooses how XP rewards are given.

    #. One Time: XP items are only given once, in either the current run or the next run after receiving the item.
    #. All Every Time: The total amount of XP received is given to the player at the start of every run.
    """

    option_one_time = 0
    option_all_every_time = 1

    default = 0
    display_name = "XP Reward Mode"


class EnableEnemyXp(Toggle):
    """Sets enemies will give XP or not.

    If disabled, enemies will not give XP. The only XP will be from XP items in the multiworld. Upgrades will be from
    leveling up and upgrade items received.
    """

    display_name = "Enable Enemy XP"


class SpawnNormalLootCrates(Toggle):
    """Sets whether loot crates can still spawn when connected to a multiworld.

    If off, then the only consumables that spawn will be the health items and the Archipelago drop item. No regular or
    legendary loot crates will spawn.

    If on, then loot crates will still spawn when there are no available Archipelago drops. See 'Loot Crate Groups' for
    details.
    """

    display_name = "Spawn Normal Loot Crates"


class NumberCommonCrateDropLocations(Range):
    """Replaces the in-game loot crate drops with an Archipelago item which must be picked up to generate a check.

    How the drops are made available and how many are needed to make a check are controlled by the next two settings.
    """

    range_start = 0
    range_end = MAX_NORMAL_CRATE_DROPS

    default = 25
    display_name = "Loot Crate Locations"


class NumberCommonCrateDropsPerCheck(Range):
    """The number of common loot crates which need to be picked up to count as a check.

    1 means every crate is a check, 2 means every other crate, etc.
    """

    range_start = 1
    range_end: int = MAX_NORMAL_CRATE_DROPS

    default = 2
    display_name: str = "Crate Pickup Step"


class NumberCommonCrateDropGroups(Range):
    """The number of groups to separate loot crate locations into.

    Once you check all the locations in a group, the randomizer will not drop more loot crate Archipelago items until
    you win more runs.

    The number of loot crate locations will be evenly split among the groups, and the groups will be evenly spread out
    over the number of wins you choose.

    Set to 1 to make all loot crate locations available from the start.
    """

    range_start = 1
    range_end: int = MAX_NORMAL_CRATE_DROP_GROUPS

    default = 1
    display_name: str = "Loot Crate Groups"


class NumberLegendaryCrateDropLocations(Range):
    """Replaces the in-game legendary loot crate drops with an Archipelago item which must be picked up to generate a
    check.

    How the drops are made available and how many are needed to make a check are controlled by the next two settings.
    """

    range_start = 0
    range_end: int = MAX_LEGENDARY_CRATE_DROPS

    default = 5
    display_name: str = "Legendary Loot Crate Locations"


class NumberLegendaryCrateDropsPerCheck(Range):
    """The number of legendary loot crates which need to be picked up to count as a check.

    1 means every crate is a check, 2 means every other crate, etc.
    """

    range_start = 1
    range_end: int = MAX_NORMAL_CRATE_DROPS

    default = 1
    display_name: str = "Legendary Loot Crate Pickup Step"


class NumberLegendaryCrateDropGroups(Range):
    """The number of groups to separate legendary loot crate locations into.

    Once you check all the locations in a group, the randomizer will not drop more legendary loot crate Archipelago
    items until you win more runs.

    The number of loot crate locations will be evenly split among the groups, and the groups will be evenly spread out
    over the number of wins you choose.

    Set to 1 to make all legendary loot crate locations available from the start.
    """

    range_start = 1
    range_end: int = MAX_LEGENDARY_CRATE_DROP_GROUPS

    default = 1
    display_name: str = "Legendary Loot Crate Groups"


# Item weights
#
# The default values of each weight are meant to give a distribution of items matching:
# - 20% Common Items
# - 12% Uncommon Items
# - 5% Rare Items
# - 3% Legendary Items
# - 20% Common Upgrades
# - 12% Uncommon Upgrades
# - 5% Rare Upgrades
# - 3% Legendary Upgrades
# - 10% Gold
# - 10% XP
#
# Combining the items and upgrades of different rarities is:
# - 40% Items
# - 40% Upgrades
# - 10% Gold
# - 10% XP
#
# This distribution is a wild guess at a good default mix of items, upgrades, gold, and XP, and may be adjusted in the
# future depending on player feedback.
#
# The ratios of common/uncommon/rare/legendary item and upgrades were chosen to roughly match the distribution of
# common/uncommon/rare/legendary values in the game itself. This is determined by looking at the max chance of each
# appearing in the shop as documented here: https://brotato.wiki.spellsandguns.com/Shop#Rarity_of_Shop_Items_and_Luck.
# It's not a perfect approximation, but it "feels" correct.


class CommonItemWeight(Range):
    """The weight of Common/Tier 1/White items in the pool."""

    range_start = 0
    range_end = 100

    default = 50
    display_name = "Common Items"


class UncommonItemWeight(Range):
    """The weight of Uncommon/Tier 2/Blue items in the pool."""

    range_start = 0
    range_end = 100

    default = 30
    display_name = "Uncommon Items"


class RareItemWeight(Range):
    """The weight of Rare/Tier 3/Purple items in the pool."""

    range_start = 0
    range_end = 100

    default = 12
    display_name = "Rare Items"


class LegendaryItemWeight(Range):
    """The weight of Legendary/Tier 4/Red items in the pool.

    Note that this is for common crate drop locations only. An additional number of legendary items is also added for
    each legendary crate drop location.
    """

    range_start = 0
    range_end = 100

    default = 8
    display_name = "Legendary Items"


class CommonUpgradeWeight(Range):
    """The number of Common/Tier 1/White upgrades to include in the item pool."""

    range_start = 0
    range_end: int = 100

    default = 50
    display_name: str = "Common Upgrades"


class UncommonUpgradeWeight(Range):
    """The number of Uncommon/Tier 2/Blue upgrades to include in the item pool."""

    range_start = 0
    range_end: int = 100

    default = 30
    display_name: str = "Uncommon Upgrades"


class RareUpgradeWeight(Range):
    """The number of Rare/Tier 3/Purple upgrades to include in the item pool."""

    range_start = 0
    range_end: int = 100

    default = 12
    display_name: str = "Rare Upgrades"


class LegendaryUpgradeWeight(Range):
    """The number of Legendary/Tier 4/Red upgrades to include in the item pool."""

    range_start = 0
    range_end = 100

    default = 8
    display_name = "Legendary Upgrades"


class GoldWeight(Range):
    """Weight of Gold items in the item pool.

    The actual value of each gold item will we randomly picked from:

    * 10
    * 25
    * 50
    * 100
    * 200
    """

    range_start = 0
    range_end = 100

    default = 10
    display_name = "Gold Weight"


class XpWeight(Range):
    """Weight of XP items in the item pool.

    The actual value of each XP item will we randomly picked from:

    * 5
    * 10
    * 25
    * 50
    * 100
    * 150
    """

    range_start = 0
    range_end = 100

    default = 10
    display_name = "XP Weight"


class StartingShopSlots(Range):
    """How many slot the shop begins with. Missing slots are added as items."""

    range_start = 0
    range_end: int = MAX_SHOP_SLOTS

    default = 4
    display_name: str = "Starting Shop Slots"


class StartingShopLockButtonsMode(Choice):
    """Add the "Lock" buttons in the shop as items.

    Missing buttons will be disabled until they are received as items.

    The button and shop slot are different items, so it's possible to receive the button without the shop.

    * All: Start with all lock buttons enabled (vanilla behavior).
    * None: Start with no lock buttons enabled at start.
    * Match shop slots: Start with the same number of lock buttons as shop slots.
    * Custom: Choose the number to start with using "Number of Lock Buttons".
    """

    option_all = 0
    option_none = 1
    option_match_shop_slots = 2
    option_custom = 3

    default = 2
    display_name = "Starting Shop Lock Buttons"


class NumberStartingShopLockButtons(Range):
    """The number of "Lock" buttons in the shop to start with.

    Missing buttons will not be usable until they are received as items.

    The button and shop slot are different items, so it's possible to receive the button without the shop.
    """

    range_start = 0
    range_end = MAX_SHOP_SLOTS

    default = 0
    display_name = "Number of Lock Buttons"


class EnableAbyssalTerrorsDLC(Toggle):
    """Enable options which require the "Abyssal Terrors" DLC.

    Currently, this only enables adding the checks for all the DLC characters.
    """

    display_name = "Enable Abyssal Terrors DLC"


class IncludeAbyssalTerrorsCharacters(OptionSet):
    """Which characters from the "Abyssal Terrors" DLC to include for checks.

    Characters not listed here will not be available to play. There will be no item to unlock them, and there will be
    no run or wave complete checks associated with them.

    Does nothing if "Enable Abyssal Terrors DLC" is not set.
    """

    default = frozenset(ABYSSAL_TERRORS_CHARACTERS.characters)
    display_name = "Include Abyssal Terrors Characters"
    valid_keys = ABYSSAL_TERRORS_CHARACTERS.characters


@dataclass
class BrotatoOptions(PerGameCommonOptions, DeathLinkMixin):
    num_victories: NumberRequiredWins
    num_characters: NumberCharacters
    num_starting_characters: NumberStartingCharacters
    starting_characters: StartingCharacters
    include_base_game_characters: IncludeBaseGameCharacters
    waves_per_drop: WavesPerCheck
    num_wave_caps: NumWaveCaps
    gold_reward_mode: GoldRewardMode
    xp_reward_mode: XpRewardMode
    enable_enemy_xp: EnableEnemyXp
    spawn_normal_loot_crates: SpawnNormalLootCrates
    num_common_crate_drops: NumberCommonCrateDropLocations
    num_common_crate_drops_per_check: NumberCommonCrateDropsPerCheck
    num_common_crate_drop_groups: NumberCommonCrateDropGroups
    num_legendary_crate_drops: NumberLegendaryCrateDropLocations
    num_legendary_crate_drops_per_check: NumberLegendaryCrateDropsPerCheck
    num_legendary_crate_drop_groups: NumberLegendaryCrateDropGroups
    common_item_weight: CommonItemWeight
    uncommon_item_weight: UncommonItemWeight
    rare_item_weight: RareItemWeight
    legendary_item_weight: LegendaryItemWeight
    common_upgrade_weight: CommonUpgradeWeight
    uncommon_upgrade_weight: UncommonUpgradeWeight
    rare_upgrade_weight: RareUpgradeWeight
    legendary_upgrade_weight: LegendaryUpgradeWeight
    gold_weight: GoldWeight
    xp_weight: XpWeight
    num_starting_shop_slots: StartingShopSlots
    shop_lock_buttons_mode: StartingShopLockButtonsMode
    num_starting_lock_buttons: NumberStartingShopLockButtons
    enable_abyssal_terrors_dlc: EnableAbyssalTerrorsDLC
    include_abyssal_terrors_characters: IncludeAbyssalTerrorsCharacters
