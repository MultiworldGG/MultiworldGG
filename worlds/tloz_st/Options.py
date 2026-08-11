from dataclasses import dataclass


from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility, NamedRange, OptionGroup, OptionSet, PlandoConnections

from .data.Constants import DUNGEON_TO_BOSS_ITEM_LOCATION, directionality_etype_lookup, pool_name_lookup
from.data.Entrances import valid_starts, ENTRANCES

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
    - all (includes lost at sea and teao3)
    Overrides tos_dungeon_options.
    """
    display_name = "Plando Dungeon Pool"
    default = set()
    valid_keys = list(DUNGEON_TO_BOSS_ITEM_LOCATION.keys()) + ["all"]


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
    If false, all dungeons and tos sections (depending on tos_dungeon_options) count towards the dungeon goal.
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
    - glitched: more difficult tricks like bomb boosts and block clips are in logic.
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
    default = 0

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
    - always_open: You can always take the portals, as long as you have the tracks/entrances on both sides
    - open_one_way: You can always take the portals, but you have to unlock them from the side with the gem first.
    Opening a one-way portal opens it's vanilla counterpart, even when shuffled.
    - open_with_items: creates an item for each portal pair, that is required to use each portal. Does not work with shuffle_portals.
    """
    display_name = "Portal Behavior"
    option_open_one_way = 0
    option_always_open = 1
    option_open_with_items = 2
    default = 0

class SpiritTracksPortalLocations(Toggle):
    """
    Creates randomized locations for shooting the gem on each train portal.
    """
    display_name = "Portal Locations"
    default = 0

class SpiritTracksDeathLink(DeathLink):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    Still a bit buggy, the train won't die immediately.
    """

class SpiritTracksStartWithTrain(Toggle):
    """
    Starts you with a forest glyph including track and cannon depending on cannon logic, giving you train access from the start.
    On by default to give people more checks in the beginning.
    If stations are shuffled or randomized start is on, if your starting entrance links to a track it will give you those tracks from your track pool.
    """
    display_name = "Start With Train"
    default = 1

class SpiritTracksRandomizeTears(Choice):
    """
    Randomize Tears of Light
    - vanilla: tears of light are not randomized
    - vanilla_items: tears of light are vanilla, but you don't need to collect them more than once and they count as archipelago locations for hint costs.
    - in_own_section: tears of light are randomized in their own tower sections. progressive and global tears can be in any section
    - in_tos: tears of light are randomized anywhere in Tower of Spirits
    - anywhere: tears of light are randomized anywhere
    - no_tears: you need to find either the lokomo sword or bow of light + bow to possess phantoms, tears are still randomized locations.
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
    alias_big = 1
    default = 0

class SpiritTracksTearGroup(Choice):
    """
    tears_of_light_grouping:
    - unique_sections: tears of light only work in one section
    - all_sections: tears work globally for all sections.
    - progressive: tears fill each section from bottom to top. Works with shuffle_tos_section.
    If ToS entrances are shuffled, the order is decided randomly.
    """
    display_name = "Tears of Light Sectionality"
    option_unique_sections = 0
    option_all_sections = 1
    option_progressive = 2

class SpiritTracksSpiritItems(Choice):
    """
    Lokomo Sword and Bow of Light can be combined with certain tear of light groupings
    - items: Lokomo Sword is the second progressive sword; and Bow of Light is its own item, but requires a progressive bow to use.
    - final_tear: if tear_group is all_sections or progressive, an extra tear item is added and collecting them all unlocks both the Lokomo Sword and the Bow of Light.
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
    If you have access to a higher tower entrance, a ramp will be created, but you can't enter/exit sections on the way without their requirements.
    open: all sections are open from the start
    sources: each source unlocks a new section
    progressive: adds "Progressive Tower Section" items, that unlock sections one at a time.
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
    Currently not compatible with station shuffle
    """
    display_name = "ToS Unlock Base Item"
    default = 0

class SpiritTracksShuffleToSSections(Choice):
    """
    Shuffle Tower of Spirits Sections.
    Also includes the summit as its own section.
    Progressive tears will respect the new ordering if shuffled alone, otherwise sections are assigned randomly.
    Adds 14 (unpaired) entrances.
    """
    display_name = "Shuffle ToS Sections"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    # option_shuffle_with_dungeons = 6  adding them to the dungeon pool requires me being in a better headspace

class SpiritTracksShuffleStations(Choice):
    """
    Shuffle Stations.
    Adds 62 (unpaired) entrances.
    """
    display_name = "Shuffle Stations"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    # 5 can be own station?

class SpiritTracksShuffleTrainTransitions(Choice):
    """
    Shuffle the transitions between different realms, and the entrance to the underwater tracks.
    Adds 24 (unpaired) entrances.
    """
    display_name = "Shuffle Train Transitions"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleHouses(Choice):
    """
    Shuffle entrances to houses. Hyrule castle is shuffled separately.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Adds 66 (unpaired) entrances.
    """
    display_name = "Shuffle Houses"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleCaves(Choice):
    """
    Shuffle cave entrances. Disorientation Station and Ends of the Earth internals are shuffled separately.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Adds 68 (unpaired) entrances.
    """
    display_name = "Shuffle Caves"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleTransitions(Choice):
    """
    Shuffle overworld transitions (for link).
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    """
    display_name = "Shuffle Overworld Transitions"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleHyruleCastle(Choice):
    """
    Shuffle hyrule castle entrances.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Adds 28 (unpaired) entrances.
    """
    display_name = "Shuffle Hyrule Castle"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleDisorientationStation(Choice):
    """
    Shuffle the inside of Disorientation Station.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    The entrance stairs are still in the cave pool.
    Adds 32 (unpaired) entrances.
    """
    display_name = "Shuffle Disorientation Station Interior"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleEotE(Choice):
    """
    Shuffle the inside of Ends of the Earth.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    The entrances to each difficulty are still in the cave pool.
    Always includes the EotE chests, no matter the minigame option.
    Adds 24 (unpaired) entrances.
    """
    display_name = "Shuffle Ends of the Earth Interior"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShufflePortals(Choice):
    """
    Shuffle train portals.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Always disables portal items.
    Other portal options still work!
    Opening a one-way portal unlocks it's vanilla counterpart, even when shuffled.
    Adds 16 (unpaired) entrances.
    """
    display_name = "Shuffle Train Portals"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleLas(Choice):
    """
    Shuffle lost at sea dungeon.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    When shuffled, the two one way entrances are linked to a single entrance in a decoupled manner.
    Puzzles reset after leaving.
    Adds 12 (unpaired) entrances.
    """
    display_name = "Shuffle Lost at Sea Dungeon"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleToSStaircase(Choice):
    """
    Shuffle the single entrance pair between the ToS lobby and staircase.
    All entrance shuffle options allow you to mix and match them in 3 pools.
    Adds 2 (unpaired) entrances.
    """
    display_name = "Shuffle ToS Staircase"
    option_no_shuffle = 0
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4

class SpiritTracksShuffleDungeonRooms(Choice):
    """
    Shuffle the entrances inside dungeons.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Has special option `shuffle in own dungeon`, that doesn't mix rooms from different dungeons.
    Adds 88 (unpaired) entrances.
    """
    display_name = "Shuffle Dungeon Interiors"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    option_shuffle_in_own_dungeon = 5

class SpiritTracksShuffleWarps(Choice):
    """
    Shuffles 2-way blue warps.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    Has special option `shuffle in own dungeon`, that keeps them connecting in their local dungeon.
    Acts as a mixed pool with other options that pick it.
    Opening a blue warp unlocks the vanilla lobby portal, even when shuffled elsewhere.
    If dungeon entrances are shuffled alone, shuffle_in_own_dungeon for warps follow the new dungeon.
    Adds 10 (unpaired) entrances.
    """
    display_name = "Shuffle Blue Warps"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    option_shuffle_in_own_dungeon = 5

class SpiritTracksShuffleDungeonEntrances(Choice):
    """
    Shuffles the entrances between dungeon stations and the start of dungeons.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    - shuffle_in_own_dungeon_vanilla: the dungeon entrance will only shuffle to its own dungeon,
        but to any entrance in that dungeon that's also in the in_own_dungeon pool
    - shuffle_in_own_dungeon_shuffle: the game pre-picks what dungeon goes to what dungeon entrance,
        and that entrance can shuffle to any entrance in that dungeon also in the in_own_dungeon pool.
    Adds 10 (unpaired) entrances.
    """
    display_name = "Shuffle Dungeon Entrances"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    option_shuffle_in_own_dungeon_vanilla = 5
    option_shuffle_in_own_dungeon_shuffle = 6

class SpiritTracksShuffleBosses(Choice):
    """
    Shuffles the entrances to the five main dungeon bosses.
    All entrance shuffle options allow you to mix and match them in 3 pools, or keep them separate.
    - shuffle_in_own_dungeon_vanilla: the boss will only shuffle to its vanilla dungeon,
        but to any entrance in that dungeon that's also in the in_own_dungeon pool
    - shuffle_in_own_dungeon_shuffle: the game pre-picks what boss goes to what dungeon entrance,
        and that entrance can shuffle to any entrance in that dungeon also in the in_own_dungeon pool.
    Adds 10 (unpaired) entrances.
    """
    display_name = "Shuffle Bosses"
    option_no_shuffle = 0
    option_shuffle_alone = 1
    option_shuffle_pool_a = 2
    option_shuffle_pool_b = 3
    option_shuffle_pool_c = 4
    option_shuffle_in_own_dungeon_vanilla = 5
    option_shuffle_in_own_dungeon_shuffle = 6

class SpiritTracksEntranceDirectionality(OptionSet):
    """
    Choose what entrance groups care about directionality (left entrance leads to right, house exterior leads to interior etc.).
    Pool options override individuals, individuals only count for shuffle_alone.
    Valid options are: houses, caves, stations, overworld, train, portals,
      dungeon_entrances, bosses, dungeon_rooms, blue_warps,
      tos_sections, tos_staircase,
      castle, disorientation, eote, las,
      pool_a, pool_b, pool_c, in_own_dungeon, all
    Pools with lots of dead ends have a high chance to cause gen errors.
    Staircases do not have directionality.
    """
    display_name = "Entrance Directionality"
    default = {"houses", "stations", "dungeon_entrances", "tos_sections", "bosses"}
    # supports_weighting = True
    valid_keys = list(directionality_etype_lookup.values()) + list(pool_name_lookup.values()) + ["all"]


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
    The requirements for picking up passengers is determined by the `passenger_pickup` option.
    - no_passengers: passengers are not randomized, and quests that affect future stuff are in their most convenient state.
    - vanilla: passengers are picked up in their vanilla locations, and only a successful delivery is a randomized location.
    You can carry 1 NPC at a time and have to keep them happy.
    - vanilla_abstract: same as above, but NPCs give themselves as items, and you don't need to care about their comfort.
    You can pick up multiple NPCs at the same time.
    - randomize: NPCs are items, and both picking them up and reaching their destinations are randomized locations.
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
    You can carry 1 type of cargo at a time, perishables perish with time and temperature, and taking damage decrements your cargo count.
    - vanilla_abstract: same as above, but buying cargo gives an unlimited cargo item that unlocks all deliveries.
    You can pick up multiple cargo at the same time and don't have to worry about transport complications.
    - randomize: Cargo become items, and buying cargo/delivering cargo are both randomized locations.
    There are multiple cargo items when used in multiple places, and the items are used up on delivery.
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
    Exclude or remove locations from non-required Tower of Spirits Sections.
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

class SpiritTracksMultiworldItemModel(Choice):
    """
    What unknown items from other worlds show up as.
    Known items still change to their closest match if model swaps are enabled.
    Revealed Traps always show up as skulls.
    - force_gems: Foreign items show up as force gems.
    - letters: Foreign items show up as letters.
    - rupees: Foreign items show up as rupees. Gold for progression, blue for useful, green for filler.
    """
    display_name = "Multiworld Item Default Model"
    option_force_gems = 0
    option_letters = 1
    option_rupees = 2
    default = 0

class SpiritTracksToSShortcuts(Toggle):
    """
    If enabled, taking the bottom door of the tower section of Tower of Spirits,
    that usually takes you back to the lobby,
    warps you to the highest unlocked door in the tower.
    To return to lobby as normal use any lift opposite any other exit.
    """
    display_name = "Tower of Spirits Shortcuts"
    default = 0

class SpiritTracksMapWarp(Toggle):
    """
    Enable warping to any previously visited station or realm by opening the rail map and tapping a station.
    You can always warp to start by flipping the collection screen.
    """
    display_name = "Enable Map Warp"
    default = 0

class SpiritTracksEntrancePlando(PlandoConnections):
    """
    Plando entrance connections. Format is a list of dictionaries:
    - entrance: "Entrance Name"
      exit: "Exit Name"
      direction: "Direction"
      percentage: 100
    Direction must be one of 'entrance', 'exit', or 'both', and defaults to 'both' if omitted.
    Percentage is an integer from 1 to 100, and defaults to 100 when omitted.
    Will disconnect entrances for you, and randomize their dangling entrances with each other, even if their entrance pools don't allow it.
    """
    display_name = "Entrance Plando"
    entrances = frozenset(ENTRANCES.keys())
    exits = frozenset(ENTRANCES.keys())

class SpiritTracksUTBlockedEntrances(Choice):
    """
    How UT handles entrances if you check an entrance that is blocked, for example entering the overworld without the right tracks.
    - mark_on_check: checking a blocked entrance will mark it as checked, even if you can't pass it.
    - mark_on_pass: checking a blocked entrance will not mark as checked, you have to actually pass it to mark it.
    - unmark_when_opened: checking a blocked entrance will mark it as checked, but once you unlock the requirements for traversing it the entrance will be unchecked.
    """
    display_name = "UT Blocked Entrances Behaviour"
    option_mark_on_check = 0
    option_mark_on_pass = 1
    option_unmark_when_opened = 2
    default = 0

class SpiritTracksProgressiveEquipment(Toggle):
    """
    Toggle if bow, bombs and sword have progressive items (true) or a main item and capacity upgrades (false).
    You cannot use the lokomo sword without the normal sword.
    """
    display_name = "Progressive Equipment"
    default = 1

class SpiritTracksShields(Toggle):
    """
    Toggle if shields are in the item pool.
    You can always buy shields in shops after buying the randomized item on that slot.
    Shields ruin speedrunning strats so that's why this is an option~
    """
    display_name = "Shields in Pool"
    default = 1

class SpiritTracksOpenBlizzardTemple(Toggle):
    """
    The bell doors in Blizzard Temple are open from the start.
    """
    display_name = "Open Blizzard Temple"
    default = 0

class SpiritTracksOpenBlueWarps(Toggle):
    """
    2-directional blue warps are open from the start.
    Nice if their entrances are shuffled.
    Opening a blue warp opens the matching lobby portal even when entrances are shuffled.
    """
    display_name = "Open Blue Warps"
    default = 0

class SpiritTracksERRetries(Range):
    """
    How many times the entrance shuffle tries again if it fails before giving up.
    Default is 10
    """
    range_start = 0
    range_end = 100
    default = 10
    display_name = "Entrance Shuffle Retries"

class SpiritTracksDecoupleEntrances(Toggle):
    """
    Decouple shuffled entrances, so entrances are no longer bidirectional.
    """
    default = 0
    display_name = "Decouple Shuffled Entrances"

class SpiritTracksRandomizeStart(OptionSet):
    """
    Where you start the game.
    Is a set of entrances it will roll from. You cannot start on the train.
    Special options include:
    - niko: the vanilla start.
    - tos: start in Tower of Spirits
    - towns: start in one of the six major settlements
    - stations: adds all stations to the pool. Note that most stations have zero sphere 0 locations
    """
    default = {'niko'}
    display_name = "Randomize Start"
    valid_keys = frozenset(valid_starts | {"niko", "tos", "stations", "towns"})

class SpiritTracksFreeStartingItems(Range):
    """
    Gives you this many free items on starting the game.
    Useful with random start on solo seeds, to ensure that starting is possible.
    """
    range_start = 0
    range_end = 10
    default = 0
    display_name = "Free Starting Items"

class SpiritTracksPassengerPickupRequirement(Choice):
    """
    What is required to pick up passengers with passenger rando.
    - tracks: you need any tracks that lead to their destination station, even if the tracks are unreachable or the station is shuffled.
    - visit: you need to have visited the passenger's destination to pick them up.
    """
    display_name = "Passenger Pickup Requirement"
    option_tracks = 0
    option_visit = 1

class SpiritTracksExtraEvents(OptionSet):
    """
    Enable/disable extra UT events for certain settings.
    - portals: show events for opening train portals if they open one-way
    - stamps: show events for stamp stations if playing with vanilla stamps
    - visits: show events for visiting stations if playing with that passenger pickup requirement
    - rabbits: shows events for individual rabbits if playing with total rabbits, that all fill out once you get your final total location of that type.
    - warps: shows events for unlocking blue warps in dungeons.
    - passengers: shows picking up and other triggers for vanilla passengers
    - cargo: shows buying vanilla cargo for the first time
    - shortcuts: adds events for unlockable shortcuts, that don't progress logic. these are unlocked for /get_logical_path even if the event is disabled,
    and auto-unlock if save file progress is lost.
    """
    display_name = "Toggle Events"
    default = {"portals", "stamps", "visits", "rabbits", "warps", "passengers", "cargo"}
    valid_keys = ["portals", "stamps", "visits", "rabbits", "warps", "passengers", "cargo", "shortcuts"]

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
    open_blizzard_temple: SpiritTracksOpenBlizzardTemple
    open_blue_warps: SpiritTracksOpenBlueWarps

    progressive_equipment: SpiritTracksProgressiveEquipment
    track_pool: SpiritTracksTrackGroupings
    shields_in_pool: SpiritTracksShields

    randomize_minigames: SpiritTracksRandomizeMinigames
    minigame_hints: SpiritTracksMinigameHints

    randomize_stamps: SpiritTracksStampItems
    stamp_pack_sizes: SpiritTracksStampItemPacks

    randomize_passengers: SpiritTracksRandomizePassengers
    passenger_pickup: SpiritTracksPassengerPickupRequirement
    randomize_cargo: SpiritTracksRandomizeCargo

    # ToS stuff
    tos_section_unlocks: SpiritTracksToSSectionUnlocks
    tos_unlock_base_item: SpiritTracksToSBase
    tos_shortcuts: SpiritTracksToSShortcuts

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

    # Start Options
    randomize_start: SpiritTracksRandomizeStart
    free_starting_items: SpiritTracksFreeStartingItems
    start_with_train: SpiritTracksStartWithTrain

    # Entrance Rando
    shuffle_houses: SpiritTracksShuffleHouses
    shuffle_caves: SpiritTracksShuffleCaves
    shuffle_overworld: SpiritTracksShuffleTransitions
    shuffle_stations: SpiritTracksShuffleStations
    shuffle_train_transitions: SpiritTracksShuffleTrainTransitions
    shuffle_portals: SpiritTracksShufflePortals
    shuffle_dungeon_entrances: SpiritTracksShuffleDungeonEntrances
    shuffle_bosses: SpiritTracksShuffleBosses
    shuffle_dungeon_rooms: SpiritTracksShuffleDungeonRooms
    shuffle_tos_sections: SpiritTracksShuffleToSSections
    shuffle_tos_staircase: SpiritTracksShuffleToSStaircase
    # shuffle_glyph_rooms
    shuffle_warps: SpiritTracksShuffleWarps
    shuffle_hyrule_castle: SpiritTracksShuffleHyruleCastle
    shuffle_disorientation: SpiritTracksShuffleDisorientationStation
    shuffle_eote: SpiritTracksShuffleEotE
    shuffle_las: SpiritTracksShuffleLas

    plando_transitions: SpiritTracksEntrancePlando
    entrance_directionality: SpiritTracksEntranceDirectionality
    decouple_shuffled_entrances: SpiritTracksDecoupleEntrances
    entrance_shuffle_retries: SpiritTracksERRetries

    # QoL
    ut_blocked_entrances_behaviour: SpiritTracksUTBlockedEntrances
    enable_map_warp: SpiritTracksMapWarp
    extra_events: SpiritTracksExtraEvents

    # Cosmetic
    starting_train: SpiritTracksStartingTrain
    multiworld_item_model_swaps: SpiritTracksZeldaModelSwaps
    multiworld_item_default_models: SpiritTracksMultiworldItemModel

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
    OptionGroup("Item Options", [
        SpiritTracksProgressiveEquipment,
        SpiritTracksTrackGroupings,
        SpiritTracksShields
    ]),
    OptionGroup("More Randomization", [
        SpiritTracksRandomizeMinigames,
        SpiritTracksMinigameHints,
        SpiritTracksStampItems,
        SpiritTracksStampItemPacks,
        SpiritTracksRandomizePassengers,
        SpiritTracksPassengerPickupRequirement,
        SpiritTracksRandomizeCargo,
        SpiritTracksPortalLocations,
    ]),
    OptionGroup("ToS Options", [
        SpiritTracksToSSectionUnlocks,
        SpiritTracksToSBase,
        SpiritTracksToSShortcuts,
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
    OptionGroup("World Options", [
        SpiritTracksRandomizePortals,
        SpiritTracksOpenBlueWarps,
        SpiritTracksOpenBlizzardTemple,
    ]),
    OptionGroup("Starting Options", [
       SpiritTracksRandomizeStart,
        SpiritTracksFreeStartingItems,
        SpiritTracksStartWithTrain,
    ]),
    OptionGroup("Entrance Randomizer Options", [
        SpiritTracksShuffleHouses,
        SpiritTracksShuffleCaves,
        SpiritTracksShuffleTransitions,
        SpiritTracksShuffleStations,
        SpiritTracksShuffleTrainTransitions,
        SpiritTracksShufflePortals,

        SpiritTracksShuffleDungeonEntrances,
        SpiritTracksShuffleToSSections,
        SpiritTracksShuffleBosses,
        SpiritTracksShuffleDungeonRooms,
        SpiritTracksShuffleWarps,
        SpiritTracksShuffleToSStaircase,

        SpiritTracksShuffleHyruleCastle,
        SpiritTracksShuffleDisorientationStation,
        SpiritTracksShuffleEotE,
        SpiritTracksShuffleLas,

        SpiritTracksEntrancePlando,
        SpiritTracksEntranceDirectionality,
        SpiritTracksDecoupleEntrances,
        SpiritTracksERRetries,
    ]),
    OptionGroup("QoL Options", [
        SpiritTracksMapWarp,
        SpiritTracksUTBlockedEntrances,
        SpiritTracksExtraEvents
    ]),
    OptionGroup("Cosmetic Options", [
        SpiritTracksStartingTrain,
        SpiritTracksZeldaModelSwaps,
        SpiritTracksMultiworldItemModel
    ]),
    OptionGroup("Item & Location Options", [
        SpiritTracksRemoveItemsFromPool
    ])

]

