from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
   ItemDict, ItemsAccessibility, ItemSet, Visibility, NamedRange, OptionGroup, OptionSet
from worlds.tloz_st.data.Items import ITEMS_DATA
from .data.Constants import DUNGEON_TO_BOSS_ITEM_LOCATION

# YAML options

class SpiritTracksGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - defeat_malladus: enter the dark realm and defeat the demon king.
    - other options: defeat the specified boss/tos section to goal. (Staven is Byrne in US Localization)
    Is not compatible with dark realm unlock options, so you can't set a number of required dungeons or compass shards etc.
    The dungeon/section associated with the goal will never be excluded.
    """

    display_name = "Goal Location"
    option_defeat_malladus = -1
    option_beat_wooded_temple = 0
    option_beat_blizzard_temple = 1
    option_beat_marine_temple = 2
    option_beat_mountain_temple = 3
    option_beat_desert_temple = 4
    option_beat_tos_section_1 = 5
    option_beat_tos_section_2 = 6
    option_beat_tos_section_3 = 7
    option_beat_tos_section_4 = 8
    option_defeat_staven = 9
    option_beat_tos_section_6 = 10
    default = -1

class SpiritTracksDarkRealmUnlock(Choice):
    """
    What unlocks the dark realm?
    - compass_of_light: only the compass of light is required. malladus also requires a sword, bow of light and Spirit Flute.
    - dungeons: find the compass of light and finish a specified number of dungeons to gain access to the dark realm.
    - shattered_compass: McGuffin hunt! find a specified number of compass shards to unlock the dark realm.
    - both: you need to find the shattered compass shards to get the track, and the dungeon goal to enter.
    """
    display_name = "Dark Realm Unlock"
    option_compass_of_light = 0
    option_dungeons = 1
    option_shattered_compass = 2
    option_both = 3
    default = 1

class SpiritTracksCompassShardCount(Range):
    """
    How many compass shards you need to unlock the tracks to the dark realm.
    """
    display_name = "Required Compass Shards"
    range_start = 1
    range_end = 30
    default = 5

class SpiritTracksTotalCompassShards(Range):
    """
    Total number of compass shards in pool.
    """
    display_name = "Total Compass Shards"
    range_start = 1
    range_end = 30
    default = 8

class SpiritTracksDungeonCount(Range):
    """
    How many dungeons/ToS sections are required to unlock the dark realm?
    Will not go higher than the number of valid locations in dungeon pool.
    Is also the number of included dungeons if not using a dungeon goal.
    """
    display_name = "Required Dungeon Count"
    range_start = 0
    range_end = 13
    default = 5

class SpiritTracksTowerOfSpiritsDungeonOptions(Choice):
    """
    How does Tower of Spirits count towards the dungeon pool?
    - not_in_dungeon_pool: Tower of Spirits is not rolled for required or included dungeons.
    - final_section: Legacy option, currently adds section 5 and Staven (Byrne) as the tower's goal location
    - all_sections: all ToS sections are added to the dungeon pool.
    """
    display_name = "Tower of Spirits Dungeon Reward Options"
    option_not_in_dungeon_pool = 0
    option_final_section = 1
    option_all_sections = 2

class SpiritTracksDungeonPoolPlando(OptionSet):
    """
    Choose what dungeons appear in the required dungeon pool.
    Leave blank to ignore.
    Valid options are: 'Wooded Temple', 'Blizzard Temple', 'Marine Temple', 'Mountain Temple', 'Desert Temple', 'ToS 1'...'ToS 6'
    Special Options include:
    - Lost At Sea
    - Take 'em All On 3
    Overrides tos_dungeon_options.
    """
    display_name = "Plando Dungeon Pool"
    default = set()
    valid_keys = list(DUNGEON_TO_BOSS_ITEM_LOCATION.keys())


class SpiritTracksEndgameScope(Choice):
    """
    How much of the dark realm do you get to play?
    - full_dark_realm: everything!
    - skip_dark_trains: skip the first phase with the dark trains
    - skip_demon_train: only fight cole and malladus, skipping the demon train fight
    - malladus_only: only fight the final boss
    - malladus_p2: skip the boulder phase and the spirit duet, and go straight to the final phase
    - enter_dark_realm: Goal is sent on entering the dark realm, but you can still fight the bosses if you like.
    """
    display_name = "Endgame Scope"
    option_full_dark_realm = 0
    option_skip_dark_trains = 1
    option_skip_demon_train = 2
    option_malladus_only = 3
    option_malladus_p2 = 4
    option_enter_dark_realm = 5
    default = 0

class SpiritTracksRequireSpecificDungeons(Toggle):
    """
    Specific dungeons are required to enter the dark realm.
    """
    display_name = "Require Specific Dungeons"
    default = 1

class SpiritTracksRequiredDungeonHints(Toggle):
    """
    Get hints for what dungeons are required.
    """
    display_name = "Dungeon Hints"
    default = 1

class SpiritTracksRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "Remove Items From Pool"
    verify_item_name = False


class SpiritTracksLogic(Choice):
    """
    Logic Difficulty.
    - normal: Glitches and tricky tricks are not in logic.
    - hard: More difficult combat, obscure strategies, certain puzzles without their solutions and slow cycles are in logic.
    - glitched: not implemented.
    """
    display_name = "Logic Difficulty"
    option_normal = 0
    option_hard = 1
    option_glitched = 2
    default = 0


class SpiritTracksKeyRandomization(Choice):
    """
    Small Key Logic options:
    - vanilla: Keys are not randomized
    - in_own_section: Keys can be found in their own dungeon or Tower of Spirits section
    - in_own_dungeon: Keys can be found in their own dungeon
    - anywhere: Keysanity. Keys can be found anywhere
    """
    display_name = "Randomize Small Keys"
    option_vanilla = 0
    option_in_own_section = 3
    option_in_own_dungeon = 1
    option_anywhere = 2
    default = 3

class SpiritTracksKeyrings(Choice):
    """
    Replaces small keys with keyrings, containing all small keys for that dungeon/ToS section.
    There's a separate option to also include boss keys.
    Does not work with vanilla key locations.
    - no_keyrings: all keys are singular, like vanilla
    - snurglar_only: only the 3 Snurglar Keys required to enter the Mountain Temple are keyrings.
    - all: All small keys are turned into keyrings
    - random_mixed: will roll a number of dungeons/sections to use keyrings for, and have single keys for the rest.
    """
    display_name = "Keyrings"
    option_no_keyrings = 0
    option_snurglar_only = 1
    option_all = 2
    option_random_mixed = 3
    default = 1

class SpiritTracksBigKeyrings(Toggle):
    """
    Boss Keys are included in keyrings.
    Does not work with vanilla boss key locations.
    Boss Key randomization will switch to whatever the keysanity option is when boss key rando is not vanilla.
    """
    display_name = "Boss Keys in Keyrings"
    default = 0

class SpiritTracksRabbitsanity(Choice):
    """
    Randomize catching rabbits. There are 10 rabbits for each realm, for a total of 50.
    Also includes Bunnio's rewards for 5 total rabbits, 1 of each rabbit, 10 rabbits of each type and 10 rabbits of all types.
    - no_rabbits: rabbits are not randomized
    - vanilla: rabbit locations always give rabbit items of their rabbit type.
    They still count as locations in archipelago for hint cost purposes, and the number of rabbits received scales based on how many locations you include.
    - unique_checks: each rabbit in the overworld is a unique location.
    - on_total: the total number of rabbits caught of each type gives a check, ex. "Catch 3 Snow Rabbits".
    - both: get locations both on specific rabbits and total rabbits.
    """
    display_name = "Rabbitsanity"
    default = 0
    option_no_rabbits = 0
    option_vanilla = 1
    option_unique_checks = 2
    option_on_total = 3
    option_both = 4

class SpiritTracksMaxRabbitLocationCount(Range):
    """
    The maximum number of rabbit locations for each type if rabbitsanity is enabled.
    Also affects rabbit_location_count_distribution.
    If rabbitsanity option is unique_checks or vanilla, it will pick this many unique locations of each type at random.
    If rabbitsanity is vanilla, rabbit pack size gets assigned automatically to make everything work.
    """
    display_name = "Rabbitsanity Max Location Count"
    range_start = 1
    range_end = 10
    default = 10

class SpiritTracksRabbitCountDistribution(Choice):
    """
    How to distribute rabbit count with the on_total rabbitsanity option, for a maximum defined in rabbit_max_location_count.
    - for_each: creates one location per rabbit.
    - on_twos: creates a location for every 2 rabbits.
    - on_threes: creates a location for every 3 rabbits.
    - random_uniform: will roll an interval between 1 and 3 for each rabbit type
    - random_mixed: will first roll how many locations to create for each rabbit type, from 1 to rabbit_max_location_count, and then randomly pick from available rabbit locations.
    If rabbitsanity is vanilla or unique_checks, it defaults to for_each, but if combined with random_mixed it will randomize unique location count between 1 and rabbit_max_location_count for each rabbit type individually.
    """
    display_name = "Rabbitsanity Location Count Distribution"
    option_for_each = 1
    option_on_twos = 2
    option_on_threes = 3
    option_random_uniform = 0
    option_random_mixed = -1
    default = 1

class SpiritTracksRabbitHints(Toggle):
    """
    Get hints for Bunnio's locations on entering rabbit haven.
    """
    display_name = "Rabbit Hints"
    default = 0

class SpiritTracksRabbitPackSize(NamedRange):
    """
    Number of rabbits received per rabbit item for each rabbit type with rabbitsanity.
    Setting it to 0 or random_uniform will randomize between 1 and 5 for each rabbit type.
    Setting it to -1 or random_mixed will keep rolling random pack size items for each rabbit type until you have enough. It rolls a discrete triangular distribution between 1 and 5 with mode 2.
    If rabbitsanity is vanilla, this is ignored as vanilla assigns its own pack sizes.
    """
    display_name = "Rabbit Pack Size"
    range_end = 5
    range_start = 1
    option_random_uniform = 0
    option_random_mixed = -1
    default = 1
    special_range_names = {
        "random_uniform": 0,
        "random_mixed": -1
    }

class SpiritTracksExtraRabbits(Range):
    """
    How many extra rabbit items to create for each rabbit type.
    Is affected by rabbit_pack_size
    If rabbitsanity is vanilla, this will add extra rabbit items to the normal item pool.
    """
    display_name = "Extra Rabbit Items"
    default = 0
    range_start = 0
    range_end = 5

class SpiritTracksRandomizePortals(Choice):
    """
    How to handle the train portals.
    - always_open: You can always take the portals, as long as you have the tracks on both sides
    - open_one_way: You can always take the portals, but you have to unlock them from the side with the gem first
    - open_with_items: creates an item for each portal pair, that is required to use each portal.
    """
    display_name = "Portal Behavior"
    option_open_one_way = 0
    option_always_open = 1
    option_open_with_items = 2
    default = 0

class SpiritTracksPortalLocations(Toggle):
    """
    Creates locations for shooting the gem on each portal.
    """
    display_name = "Portal Checks"
    default = 0

class SpiritTracksDeathLink(DeathLink):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    Still a bit buggy, the train won't die immediately.
    """

class SpiritTracksStartWithTrain(Toggle):
    """
    Starts you with a forest glyph including track and cannon depending on cannon logic, giving you train access from the start.
    On by default to give people more checks in the beginning
    """
    display_name = "Start With Train"
    default = 1

class SpiritTracksRandomizeTears(Choice):
    """
    Randomize Tears of Light
    - vanilla: tears of light are not randomized
    - vanilla_items: tears of light are vanilla, but you don't need to collect them more than once and they count as archipelago locations for hint costs.
    - in_own_section: tears of light are randomized in their own tower sections. progressive and global tears count towards all sections
    - in_tos: tears of light are randomized anywhere in Tower of Spirits
    - anywhere: tears of light are randomized anywhere
    - no_tears: you need to find either two swords or bow of light + bow to possess phantoms, tears are still randomized locations.
    """
    display_name = "Randomize Tears of Light"
    option_vanilla = -1
    option_vanilla_items = -2
    option_in_own_section = 1
    option_in_tos = 2
    option_anywhere = 3
    option_no_tears = 0
    default = -1

class SpiritTracksTearSize(Choice):
    """
    Tears of light size
    - small: you need 3 tears for each tower section
    - large: you need one big tear per section
    """
    display_name = "Tears of Light Size"
    option_small = 0
    option_large = 1
    default = 0

class SpiritTracksTearGroup(Choice):
    """
    tears_of_light_grouping:
    - unique_sections: tears of light only work in one section
    - all_sections: tears work globally for all sections.
    - progressive: tears fill each section from bottom to top. Works with shuffle_tos_section.
    """
    display_name = "Tears of Light Sectionality"
    option_unique_sections = 0
    option_all_sections = 1
    option_progressive = 2

class SpiritTracksSpiritItems(Choice):
    """
    Lokomo Sword and Bow of Light can be combined with certain tear of light groupings
    - items: Lokomo Sword is the second progressive sword; and Bow of Light is its own item, but requires a progressive bow to use.
    - final_tear: if tear_group is all_sections or progressive, an extra final tear item is added that unlocks both the Lokomo Sword and the Bow of Light.
    """
    display_name = "Spirit Item Options"
    option_items = 0
    option_final_tear = 1

class SpiritTracksStartingTrain(Choice):
    """
    What train to start with. Train parts will be randomized later.
    Different trains have different health, but see this to more be a fun cosmetic thing.
    - all_parts: start with all parts, and customize freely in Alfonzo's Workshop on outset.
    - random_train: picks 1 random train to start with
    """
    display_name = "Starting Train"
    option_all_parts = -1
    option_random_train = -2
    option_spirit_train = 0
    option_wooden_train = 1
    option_refined_train = 2
    option_demon_train = 3
    option_stagecoach = 4
    option_dragon_train = 5
    option_sweet_train = 6
    option_golden_train = 7
    default = 0

class SpiritTracksRandomizeMinigames(Choice):
    """
    Randomize Minigames.
    All difficulties include Restoration Duets, Hyrule Castle Sword Training and Goron Target Range.
    Easy+ includes Mayscore Whip game, Take 'em All On, Pirate Hideout, Slippery Station and Ends of the Earth.
    - no_minigames: minigames are not randomized
    - restoration_duets: include only restoration duets. Are they really minigames?
    - easy: only the easiest difficulty of each minigame is randomized.
    - hard: only the second difficulty of each minigame is randomized.
    - expert: only the hardest difficulty of each minigame is randomized. Includes Take 'em all On 3.
    - all_reasonable: the easy and hard difficulties are randomized.
    - everything: all minigame rewards are randomized.
    """
    display_name = "Randomize Minigames"
    option_no_minigames = 0
    option_restoration_duets = 6
    option_easy = 1
    option_hard = 2
    option_expert = 5
    option_all_reasonable = 3
    option_everything = 4

    default = 1

class SpiritTracksMinigameHints(Toggle):
    """
    Hint for minigames
    """
    display_name = "Minigame Hints"
    default = 0

class SpiritTracksToSSectionUnlocks(Choice):
    """
    What unlocks Tower of Spirits sections?
    open: all sections are open from the start
    sources: each source unlocks a new section
    progressive: adds "Progressive Tower Section" items, that unlock sections one at a time. ToS 1 is always available.
    """
    display_name = "ToS Section Unlocks"
    option_open = 0
    option_sources = 1
    option_progressive = 2
    default = 1

class SpiritTracksToSBase(Toggle):
    """
    If True, Prevents Tower of Spirit access until you have the `Tower of Spirits Base` item
    Creates an additional progressive tower section item instead if you play with progressive tower sections.
    """
    display_name = "ToS Unlock Base Item"
    default = 0

class SpiritTracksShuffleToSSections(Choice):
    """
    Shuffle Tower of Spirits Sections.
    Also includes the summit as its own section.
    Progressive tears will respect the new ordering.
    """
    display_name = "Shuffle ToS Sections"
    option_no_shuffle = 0
    option_shuffle = 1

class SpiritTracksShopsanity(OptionSet):
    """
    Randomize Shops.
    Gives vanilla items after buying the randomized one.
    Add the following to the list to randomize that type of shop location:
    - uniques: 3 locations, 4500 rupees
    - treasure: 7 locations, 2400 rupees
    - potions: 10 locations, 1400 rupees
    - shields: 5 locations, 610 rupees
    - postcards: 4 locations 400 rupees
    - ammo: 4 locations 500 rupees
    - all: same as adding all above
    """
    display_name = "Shopsanity"
    default = set()
    # supports_weighting = True
    valid_keys = ["uniques", "treasure", "potions", "shields", "postcards", "ammo", "all"]

class SpiritTracksShopHints(Toggle):
    """
    Know what you're buying before you buy
    """
    display_name = "Shop Hints"
    default = 1

class SpiritTracksCannonLogic(Choice):
    """
    When is cannon required?
    - train_requires_cannon: you cannot board the train without the cannon
    - open_train: cannonless train is not in logic, but you can use the train without cannon if you want to
    - hard_logic: cannonless train is in logic, often requiring clever routing, damage tanking or dodging cannonballs by braking with good timing. Should always be possible with vanilla train speed settings and a four heart spirit train.
    - no_logic: ignores train enemies in logic. Cheesing enemies with train speed is usually necessary.
    """
    display_name = "Cannon Logic"
    option_train_requires_cannon = 0
    option_open_train = 1
    option_hard_logic = 2
    option_no_logic = 3

class SpiritTracksRupeeFarming(Choice):
    """
    What is required for rupee farming?
    - no_farming: All rupees are accounted for in the item pool.
    - unlimited_farming: Once you have access to Linebeck, or rupees from excess treasures, you are logically expected to farm for rupees.
    """
    # - capped_farming: The amount of rupees you're expected to farm depends on how many farming hotspots you have in logic. Not Implemented.
    display_name = "Rupee Farming Logic"
    option_no_farming = 0
    option_unlimited_farming = 1
    # option_capped_farming = 2
    default = 0

class SpiritTracksExcessTreasures(Choice):
    """
    There are random treasures everywhere, in pots, leaves, from minigames, shops and prize postcards.
    What happens when you get them?
    - nothing: random treasures give you nothing.
    - vanilla: You get what you get
    - convert_to_rupees: Instantly converts to Linebeck's sell price.
    """
    display_name = "Excess Random Treasure"
    option_nothing = 0
    option_vanilla = 1
    option_convert_to_rupees = 2
    default = 1

class SpiritTracksRandomizePassengers(Choice):
    """
    Randomize the sidequests involving moving passengers from one station to another.
    NPCs can be picked up if you have access to their destination station.
    - no_passengers: passengers are not randomized, and quests that affect future stuff are in their most convenient state.
    - vanilla: passengers are picked up in their vanilla locations, and only a successful delivery is a randomized location.
    You can carry 1 NPC at a time and have to keep them happy.
    - vanilla_abstract: same as above, but NPCs give themselves as items, and you don't need to care about their comfort.
    You can pick up multiple NPCs at the same time.
    - randomize: NPCs are items, and both picking them up and reaching their destinations are locations.
    """
    display_name = "Randomize Passengers"
    option_no_passengers = 0
    option_vanilla = 1
    option_vanilla_abstract = 2
    option_randomize = 3
    default = 0

class SpiritTracksRandomizeCargo(Choice):
    """
    Randomize transporting cargo from one station to another. You need the wagon to buy cargo.
    - no_cargo: Cargo deliveries are not randomized, and places affected are in their most convenient state, ex. Goron lava geyser are down.
    - vanilla: cargo can be bought at their vanilla locations, and only a successful delivery is a randomized location.
    You can carry 1 type of cargo at a time, perishables perish with time and taking damage decrements your cargo count.
    - vanilla_abstract: same as above, but buying cargo gives an unlimited cargo item that unlocks all deliveries.
    You can pick up multiple cargo at the same time and don't have to worry about transport complications.
    - randomize: Cargo become items, and buying cargo/delivering cargo are both randomized locations.
    There are multiple cargo items when used in multiple places, and the items are used up on getting the locations.
    """
    display_name = "Randomize Cargo"
    option_no_cargo = 0
    option_vanilla = 1
    option_vanilla_abstract = 2
    option_randomize = 3
    default = 0

class SpiritTracksRandomizeBossKeys(Choice):
    """
    Randomize Boss Keys.
    Most boss key locations trigger on picking up or moving the key, but for Mountain Temple you need to finish the minecart puzzle.
    - vanilla: boss keys are normal, you need to carry them to their door
    - vanilla_abstract: picking up boss keys gives you an abstract boss key item, so you don't have to carry the key
    - in_own_section: boss keys are randomized in their own dungeon/Tower of Spirits section
    - in_own_dungeon: boss keys are randomized in their own dungeon
    - anywhere: boss keys are randomized anywhere
    """
    display_name = "Randomize Boss Keys"
    option_vanilla = 0
    option_vanilla_abstract = -1
    option_in_own_section = 3
    option_in_own_dungeon = 1
    option_anywhere = 2
    default = 0

class SpiritTracksStampItems(Choice):
    """
    What to do with stamps.
    - no_stamp_stands: don't randomize stamp book, stamps stands or stamp rewards from Niko
    - vanilla: Stamp stands give stamps, that are neither archipelago items nor randomized locations, that count towards Niko rewards, that are randomized.
    - vanilla_with_location: stamp stands are randomized locations, but also give non-archipelago-item stamps that count towards Niko rewards.
    - vanilla_items: stamp stands are locations, that give their vanilla stamp items.
    - randomized: stamp stands are randomized locations, and stamps are randomized items that you need to find.
    """
    display_name = "Randomize Stamps"
    option_no_stamp_stands = 0
    option_vanilla = 4
    option_vanilla_with_location = 1
    option_vanilla_items = 2
    option_randomize = 3
    default = 1

class SpiritTracksStampItemPacks(NamedRange):
    """
    Change the size of your stamp packs.
    Only used when stamps are randomized.
    - random_mixed (-1): chooses a mix of different pack sizes at random
    """
    display_name = "Stamp Pack Size"
    range_start = 1
    range_end = 5
    option_random_mixed = -1
    default = -1
    special_range_names = {
        "random_mixed": -1
    }

class SpiritTracksExcludeDungeons(Choice):
    """
    Exclude or remove locations from non-required dungeons.
    Does not count Tower of Spirits, that has its own option.
    If using shattered compass goal, the game will still pick dungeons based on required dungeon settings for inclusion/exclusion.
    Does not work with require_specific_dungeons=False, that sets all dungeons to included.
    - include: non-required dungeons are included
    - exclude: non-required dungeon locations are excluded, and can't have useful or progression items.
    - remove: non-required dungeon locations are removed from generation, and don't count towards hint cost etc.
    """
    display_name = "Exclude non-required Dungeons"
    option_include = 0
    option_exclude = 1
    option_remove = 2
    default = 0

class SpiritTracksExcludeSections(Choice):
    """
    Exclude or remove locations from non-required Tower of Spirits Section.
    Will spawn the blue warp in the tower early if section 5 is excluded, you'll still need to defeat Staven (Byrne) to reach the room behind it.
    The Stamp Stand is active as long as stamps are.
    - include: non-required sections are included
    - exclude: non-required sections locations are excluded, and can't have useful or progression items.
    - remove: non-required section locations are removed from generation, and don't count towards hint cost etc.
    """
    display_name = "Exclude non-required ToS Sections"
    option_include = 0
    option_exclude = 1
    option_remove = 2
    default = 0

class SpiritTracksTrackGroupings(Choice):
    """
    What does your rail item pool look like?
    Includes different custom combined rail items sorted into different pools you can choose from.
    Many of the combined items overlap.
    Combinations that contain sources unlock what the source unlocks, like tower sections if you choose that option.
    - vanilla: Your rail pool consists of the 34 vanilla glyph, source, restoration and force gem tracks.
    - completed_glyphs: Each glyph comes pre-completed. Sand realm counts separately. 5 rail items.
    - major_minor: creates a major and minor rail combination for each realm, where the major contains the source, restoration and glyph. 10 rail items.
    - thematic: Adds 16 custom groups containing 3-5 rail items to the pool, based on locale.
    - mixed: Rolls a complete set of rail items from all rail pools.
    - mixed_large: rolls as mixed but does not include single rail items
    - mixed_small: rolls as mixed but does not include completed glyph items.
    """
    # - off: In case you want to create your own pool. Defaults to vanilla if add_items_to_pool is empty.
    display_name = "Track Item Pool"
    option_vanilla = 0
    option_completed_glyphs = 1
    option_major_minor = 2
    option_thematic = 3
    option_mixed = -1
    option_mixed_large = -2
    option_mixed_small = -3

class SpiritTracksZeldaModelSwaps(Toggle):
    """
    Change the item models for items found belonging to other players to their nearest spirit-tracks equivalent.
    Currently, all Zelda Games are implemented except the Oracle games.
    Other copies of Spirit Tracks always swap their items.
    """
    display_name = "Multiworld Item Model Swaps"
    default = 1

@dataclass
class SpiritTracksOptions(PerGameCommonOptions):
    # Accessibility
    accessibility: ItemsAccessibility

    # Goal options
    goal: SpiritTracksGoal
    dark_realm_access: SpiritTracksDarkRealmUnlock
    endgame_scope: SpiritTracksEndgameScope
    dungeons_required: SpiritTracksDungeonCount
    tos_dungeon_options: SpiritTracksTowerOfSpiritsDungeonOptions
    plando_dungeon_pool: SpiritTracksDungeonPoolPlando
    require_specific_dungeons: SpiritTracksRequireSpecificDungeons
    dungeon_hints: SpiritTracksRequiredDungeonHints
    exclude_dungeons: SpiritTracksExcludeDungeons
    exclude_sections: SpiritTracksExcludeSections
    compass_shard_count: SpiritTracksCompassShardCount
    compass_shard_total: SpiritTracksTotalCompassShards

    # Logic options
    logic: SpiritTracksLogic
    cannon_logic: SpiritTracksCannonLogic

    # Item Randomization
    keysanity: SpiritTracksKeyRandomization
    randomize_boss_keys: SpiritTracksRandomizeBossKeys
    keyrings: SpiritTracksKeyrings
    big_keyrings: SpiritTracksBigKeyrings

    track_pool: SpiritTracksTrackGroupings

    randomize_minigames: SpiritTracksRandomizeMinigames
    minigame_hints: SpiritTracksMinigameHints

    start_with_train: SpiritTracksStartWithTrain

    randomize_stamps: SpiritTracksStampItems
    stamp_pack_sizes: SpiritTracksStampItemPacks

    randomize_passengers: SpiritTracksRandomizePassengers
    randomize_cargo: SpiritTracksRandomizeCargo

    # ToS stuff
    tos_section_unlocks: SpiritTracksToSSectionUnlocks
    tos_unlock_base_item: SpiritTracksToSBase
    shuffle_tos_sections: SpiritTracksShuffleToSSections

    randomize_tears: SpiritTracksRandomizeTears
    tear_size: SpiritTracksTearSize
    tear_sections: SpiritTracksTearGroup
    spirit_weapons: SpiritTracksSpiritItems

    # Portals
    portal_behavior: SpiritTracksRandomizePortals
    portal_checks: SpiritTracksPortalLocations

    # World Options

    # Shops, treasure and rupees
    shopsanity: SpiritTracksShopsanity
    shop_hints: SpiritTracksShopHints
    rupee_farming_logic: SpiritTracksRupeeFarming
    excess_random_treasure: SpiritTracksExcessTreasures

    # Rabbit Options
    rabbitsanity: SpiritTracksRabbitsanity
    rabbit_max_location_count: SpiritTracksMaxRabbitLocationCount
    rabbit_location_count_distribution: SpiritTracksRabbitCountDistribution
    rabbit_pack_size: SpiritTracksRabbitPackSize
    rabbit_extra_items: SpiritTracksExtraRabbits
    # rabbit_hints: SpiritTracksRabbitHints

    # Cosmetic
    starting_train: SpiritTracksStartingTrain
    multiworld_item_model_swaps: SpiritTracksZeldaModelSwaps

    # Generic
    start_inventory_from_pool: StartInventoryPool
    remove_items_from_pool: SpiritTracksRemoveItemsFromPool
    death_link: SpiritTracksDeathLink

st_option_groups = [
    OptionGroup("Goal Options", [
        SpiritTracksGoal,
        SpiritTracksDarkRealmUnlock,
        SpiritTracksDungeonCount,
        SpiritTracksRequireSpecificDungeons,
        SpiritTracksEndgameScope,
        SpiritTracksTowerOfSpiritsDungeonOptions,
        SpiritTracksDungeonPoolPlando,
        SpiritTracksExcludeSections,
        SpiritTracksExcludeDungeons,
        SpiritTracksRequiredDungeonHints,
        SpiritTracksCompassShardCount,
        SpiritTracksTotalCompassShards
    ]),
    OptionGroup("Logic Options", [
        SpiritTracksLogic,
        SpiritTracksCannonLogic,
    ]),
    OptionGroup("Key Options", [
        SpiritTracksKeyRandomization,
        SpiritTracksRandomizeBossKeys,
        SpiritTracksKeyrings,
        SpiritTracksBigKeyrings,
    ]),
    OptionGroup("Randomization Options", [
        SpiritTracksTrackGroupings,
        SpiritTracksRandomizeMinigames,
        SpiritTracksMinigameHints,
        SpiritTracksStampItems,
        SpiritTracksStampItemPacks,
        SpiritTracksRandomizePortals,
        SpiritTracksPortalLocations,
        SpiritTracksRandomizePassengers,
        SpiritTracksRandomizeCargo,
        SpiritTracksStartWithTrain,
    ]),
    OptionGroup("ToS Options", [
        SpiritTracksToSSectionUnlocks,
        SpiritTracksToSBase,
        SpiritTracksShuffleToSSections,
        SpiritTracksRandomizeTears,
        SpiritTracksTearSize,
        SpiritTracksTearGroup,
        SpiritTracksSpiritItems
    ]),
    OptionGroup("Shops, Treasure and Rupees", [
        SpiritTracksShopsanity,
        SpiritTracksShopHints,
        SpiritTracksRupeeFarming,
        SpiritTracksExcessTreasures
    ]),
    OptionGroup("Rabbit Options", [
        SpiritTracksRabbitsanity,
        SpiritTracksMaxRabbitLocationCount,
        SpiritTracksRabbitCountDistribution,
        SpiritTracksRabbitPackSize,
        SpiritTracksExtraRabbits,
        SpiritTracksRabbitHints
    ]),
    OptionGroup("Cosmetic Options", [
        SpiritTracksStartingTrain,
        SpiritTracksZeldaModelSwaps
    ]),
    OptionGroup("Item & Location Options", [
        SpiritTracksRemoveItemsFromPool
    ])

]

