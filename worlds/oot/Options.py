import typing
import random
from dataclasses import dataclass
from Options import Option, OptionDict, DefaultOnToggle, Toggle, Range, OptionSet, DeathLink, PlandoConnections, \
    PerGameCommonOptions, OptionGroup
from .EntranceShuffle import entrance_shuffle_table
from .LogicTricks import normalized_name_tricks, normalized_name_advanced_tricks
from .ColorSFXOptions import *


class TrackRandomRange(Range):
    """Overrides normal from_any behavior to track whether the option was randomized at generation time."""
    supports_weighting = False
    randomized: bool = False

    @classmethod
    def from_any(cls, data: typing.Any) -> Range:
        if type(data) is list:
            val = random.choices(data)[0]
            ret = super().from_any(val)
            if not isinstance(val, int) or len(data) > 1:
                ret.randomized = True
            return ret
        if type(data) is not dict:
            return super().from_any(data)
        if any(data.values()):
            val = random.choices(list(data.keys()), weights=list(map(int, data.values())))[0]
            ret = super().from_any(val)
            if not isinstance(val, int) or len(list(filter(bool, map(int, data.values())))) > 1:
                ret.randomized = True
            return ret
        raise RuntimeError(f"All options specified in \"{cls.display_name}\" are weighted as zero.")


class OoTPlandoConnections(PlandoConnections):
    entrances = set([connection[1][0] for connection in entrance_shuffle_table])
    exits = set([connection[2][0] for connection in entrance_shuffle_table if len(connection) > 2])


class PlandomizedLocations(OptionDict):
    """Compatibility-only field for importing upstream settings/presets."""
    display_name = "Plandomized Locations"
    default = {}


class Logic(Choice): 
    """Set the logic used for the generator.
    Glitchless: Normal gameplay. Can enable more difficult logical paths using the Logic Tricks option.
    Advanced: Many powerful glitches expected, such as bomb hovering and clipping.
    Advanced is incompatible with the following settings:
    - All forms of entrance randomizer
    - MQ dungeons
    - Pot shuffle
    - Freestanding item shuffle
    - Crate shuffle
    - Beehive shuffle
    No Logic: No logic is used when placing items. Not recommended for most players."""
    display_name = "Logic Rules"
    option_glitchless = 0
    option_advanced = 1
    option_no_logic = 2


class NightTokens(Toggle):
    """When enabled, nighttime skulltulas logically require Sun's Song."""
    display_name = "Nighttime Skulltulas Expect Sun's Song"


class Forest(Choice): 
    """Set the state of Kokiri Forest and the path to Deku Tree.
    Open: Neither the forest exit nor the path to Deku Tree is blocked.
    Closed Deku: The forest exit is not blocked; the path to Deku Tree requires Kokiri Sword and Deku Shield.
    Closed: Path to Deku Tree requires sword and shield. The forest exit is blocked until Deku Tree is beaten.
    Closed forest will force child start, and becomes Closed Deku if interior entrances, overworld entrances, warp songs, or random spawn positions are enabled."""
    display_name = "Forest"
    option_open = 0
    option_closed_deku = 1
    option_closed = 2
    alias_open_forest = 0
    alias_closed_forest = 2


class Gate(Choice): 
    """Set the state of the Kakariko Village gate for child. The gate is always open as adult.
    Open: The gate starts open. Happy Mask Shop opens upon receiving Zelda's Letter.
    Zelda: The gate and Mask Shop open upon receiving Zelda's Letter, without needing to show it to the guard.
    Closed: Vanilla behavior; the gate and Mask Shop open upon showing Zelda's Letter to the gate guard."""
    display_name = "Kakariko Gate"
    option_open = 0
    option_zelda = 1
    option_closed = 2


class DoorOfTime(Choice):
    """Set how the Door of Time is opened.
    Open: The Door of Time starts opened.
    Song of Time: Requires Song of Time.
    OoT + Song of Time: Requires Song of Time and level 2 Ocarina progression.
    3 Stones: Requires all 3 Spiritual Stones.
    3 Stones + Song of Time: Requires Stones and Song of Time.
    3 Stones + OoT + SoT: Requires Stones, Song of Time, and level 2 Ocarina progression."""
    display_name = "Door of Time"
    option_open = 0
    option_sot = 1
    option_oot_sot = 2
    option_stones = 3
    option_stones_sot = 4
    option_stones_oot_sot = 5
    default = 1
    alias_true = 0
    alias_false = 1


class Fountain(Choice): 
    """Set the state of King Zora, blocking the way to Zora's Fountain.
    Open: King Zora starts moved as both ages. Ruto's Letter is removed.
    Adult: King Zora must be moved as child, but is always moved for adult.
    Closed: Vanilla behavior; King Zora must be shown Ruto's Letter as child to move him as both ages."""
    display_name = "Zora's Fountain"
    option_open = 0
    option_adult = 1
    option_closed = 2
    default = 2


class Fortress(Choice): 
    """Set the requirements for access to Gerudo Fortress.
    Normal: Vanilla behavior; all four carpenters must be rescued.
    Fast: Only one carpenter must be rescued, which is the one in the bottom-left of the fortress.
    Open: The Gerudo Valley bridge starts repaired. Gerudo Membership Card is given to start if not shuffled."""
    display_name = "Gerudo Fortress"
    option_normal = 0
    option_fast = 1
    option_open = 2
    default = 1


class Bridge(Choice): 
    """Set the requirements for the Rainbow Bridge.
    Open: The bridge is always present.
    Vanilla: Bridge requires Shadow Medallion, Spirit Medallion, and Light Arrows.
    Stones: Bridge requires a configurable amount of Spiritual Stones.
    Medallions: Bridge requires a configurable amount of medallions.
    Dungeons: Bridge requires a configurable amount of rewards (stones + medallions).
    Tokens: Bridge requires a configurable amount of gold skulltula tokens.
    Hearts: Bridge requires a configurable amount of hearts."""
    display_name = "Rainbow Bridge Requirement"
    option_open = 0
    option_vanilla = 1
    option_stones = 2
    option_medallions = 3
    option_dungeons = 4
    option_tokens = 5
    option_hearts = 6
    default = 3


class Trials(TrackRandomRange):
    """Set the number of required trials in Ganon's Castle."""
    display_name = "Ganon's Trials Count"
    range_start = 0
    range_end = 6


open_options: typing.Dict[str, type(Option)] = {
    "open_forest": Forest,
    "open_kakariko": Gate,
    "open_door_of_time": DoorOfTime,
    "zora_fountain": Fountain,
    "gerudo_fortress": Fortress, 
    "bridge": Bridge,
    "trials": Trials,
}


class StartingAge(Choice): 
    """Choose which age Link will start as."""
    display_name = "Starting Age"
    option_child = 0
    option_adult = 1


class InteriorEntrances(Choice): 
    """Shuffles interior entrances.
    Simple: Houses and Great Fairies are shuffled.
    All: In addition to Simple, includes Windmill, Link's House, Temple of Time, and the Kakariko potion shop."""
    display_name = "Shuffle Interior Entrances"
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_true = 2


class GrottoEntrances(Toggle):
    """Shuffles grotto and grave entrances."""
    display_name = "Shuffle Grotto/Grave Entrances"


class DungeonEntrances(Choice):
    """Shuffles dungeon entrances. When enabled, both ages will have access to Fire Temple, Bottom of the Well, and Deku Tree.
    Simple: Shuffle dungeon entrances except for Ganon's Castle.
    All: Include Ganon's Castle as well."""
    display_name = "Shuffle Dungeon Entrances"
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_true = 1


class BossEntrances(Choice):
    """Shuffles boss entrances.
    Limited: Bosses will be limited to the ages that typically fight them.
    Full: Bosses may be fought as different ages than usual. Child can defeat Phantom Ganon and Bongo Bongo."""
    display_name = "Shuffle Boss Entrances"
    option_off = 0
    option_limited = 1
    option_full = 2


class ShuffleGanonTower(Toggle):
    """Shuffle the entrance from Ganon's Castle Main to Ganon's Tower into the boss entrance pool."""
    display_name = "Shuffle Ganon's Tower Entrance"


class OverworldEntrances(Toggle):
    """Shuffles overworld loading zones."""
    display_name = "Shuffle Overworld Entrances"


class ShuffleHideoutEntrances(Toggle):
    """Shuffles the 4 interior entrances to different rooms within Gerudo Fortress."""
    display_name = "Shuffle Hideout Entrances"


class ShuffleGerudoFortressHeartPiece(Choice):
    """Controls the child-only Heart Piece in Gerudo Fortress when Thieves' Hideout entrances are shuffled.
    Remove: exclude it. Vanilla: leave it in place. Shuffle: add it to the item pool."""
    display_name = "Shuffle Gerudo Fortress Heart Piece"
    option_remove = 0
    option_vanilla = 1
    option_shuffle = 2
    default = 1


class ShuffleGerudoValleyRiverExit(Toggle):
    """Shuffles the river exit from Gerudo Valley that drops you at Lake Hylia."""
    display_name = "Shuffle Gerudo Valley River Exit"


class OwlDrops(Toggle):
    """Randomizes owl drops from Lake Hylia or Death Mountain Trail as child."""
    display_name = "Randomize Owl Drops"


class WarpSongs(Toggle):
    """Randomizes warp song destinations."""
    display_name = "Randomize Warp Songs"


class SpawnPositions(Choice):
    """Randomizes the starting position on loading a save. Consistent between savewarps."""
    display_name = "Randomize Spawn Positions"
    option_off = 0
    option_child = 1
    option_adult = 2
    option_both = 3
    alias_true = 3


# class MixEntrancePools(Choice):
#     """Shuffles entrances into a mixed pool instead of separate ones. "indoor" keeps overworld entrances separate; "all"
#      mixes them in."""
#     display_name = "Mix Entrance Pools"
#     option_off = 0
#     option_indoor = 1
#     option_all = 2


# class DecoupleEntrances(Toggle):
#     """Decouple entrances when shuffling them. Also adds the one-way entrance from Gerudo Valley to Lake Hylia if
#     overworld is shuffled."""
#     display_name = "Decouple Entrances"


class TriforceHunt(Toggle):
    """Gather pieces of the Triforce scattered around the world to complete the game."""
    display_name = "Triforce Hunt"


class TriforceGoal(Range):
    """Number of Triforce pieces required to complete the game."""
    display_name = "Required Triforce Pieces"
    range_start = 1
    range_end = 80
    default = 20


class ExtraTriforces(Range):
    """Percentage of additional Triforce pieces in the pool. With high numbers, you may need to randomize additional
    locations to have enough items."""
    display_name = "Percentage of Extra Triforce Pieces"
    range_start = 0
    range_end = 100
    default = 50


class FreeBombchuDrops(Toggle):
    """The first Bombchu pack found becomes a Bombchu Bag, giving the same amount of bombchus
    as the original pack (e.g., finding Bombchus (5) first gives Bombchu Bag with 5 bombchus).

    After finding the bag, bombchu refills drop from grass, pots, crates, and enemies.
    Bombchus can be purchased from shops for 60/99/180 rupees.
    Bombchus open Bombchu Bowling."""
    display_name = "Add Bombchu Bag and Drops"


class DungeonShortcuts(Choice):
    """Shortcuts to dungeon bosses are available without any requirements.
    If enabled, this will impact the logic of dungeons where shortcuts are available.
    Choice: Use the option "dungeon_shortcuts_list" to choose shortcuts."""
    display_name = "Dungeon Boss Shortcuts Mode"
    option_off = 0
    option_choice = 1
    option_all = 2
    option_random_dungeons = 3


class DungeonShortcutsList(OptionSet):
    """Chosen dungeons to have shortcuts."""
    display_name = "Shortcut Dungeons"
    valid_keys = {
        "Deku Tree",
        "Dodongo's Cavern",
        "Jabu Jabu's Belly",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
    }


class MQDungeons(Choice):
    """Choose between vanilla and Master Quest dungeon layouts.
    Vanilla: All layouts are vanilla.
    MQ: All layouts are Master Quest.
    Specific: Use the option "mq_dungeons_list" to choose which dungeons are MQ.
    Count: Use the option "mq_dungeons_count" to choose a number of random dungeons as MQ."""
    display_name = "MQ Dungeon Mode"
    option_vanilla = 0
    option_mq = 1
    option_specific = 2
    option_count = 3


class MQDungeonList(OptionSet):
    """With MQ dungeons as Specific: chosen dungeons to be MQ layout."""
    display_name = "MQ Dungeon List"
    valid_keys = {
        "Deku Tree",
        "Dodongo's Cavern",
        "Jabu Jabu's Belly",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
        "Bottom of the Well",
        "Ice Cavern",
        "Gerudo Training Ground",
        "Ganon's Castle",
    }


class MQDungeonCount(TrackRandomRange):
    """With MQ dungeons as Count: number of randomly-selected dungeons to be MQ layout."""
    display_name = "MQ Dungeon Count"
    range_start = 0
    range_end = 12
    default = 0


# class EmptyDungeons(Choice):
#     """Pre-completed dungeons are barren and rewards are given for free."""
#     display_name = "Pre-completed Dungeons Mode"
#     option_none = 0
#     option_specific = 1
#     option_count = 2


# class EmptyDungeonList(OptionSet):
#     """Chosen dungeons to be pre-completed."""
#     display_name = "Pre-completed Dungeon List"
#     valid_keys = {
#         "Deku Tree",
#         "Dodongo's Cavern",
#         "Jabu Jabu's Belly",
#         "Forest Temple",
#         "Fire Temple",
#         "Water Temple",
#         "Shadow Temple",
#         "Spirit Temple",
#     }


# class EmptyDungeonCount(Range):
#     display_name = "Pre-completed Dungeon Count"
#     range_start = 1
#     range_end = 8
#     default = 2


world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    "shuffle_interior_entrances": InteriorEntrances,
    "shuffle_grotto_entrances": GrottoEntrances,
    "shuffle_dungeon_entrances": DungeonEntrances,
    "shuffle_overworld_entrances": OverworldEntrances,
    "shuffle_hideout_entrances": ShuffleHideoutEntrances,
    "shuffle_gerudo_fortress_heart_piece": ShuffleGerudoFortressHeartPiece,
    "shuffle_gerudo_valley_river_exit": ShuffleGerudoValleyRiverExit,
    "owl_drops": OwlDrops,
    "warp_songs": WarpSongs,
    "spawn_positions": SpawnPositions,
    "shuffle_bosses": BossEntrances,
    "shuffle_ganon_tower": ShuffleGanonTower,
    # "mix_entrance_pools": MixEntrancePools,
    # "decouple_entrances": DecoupleEntrances,
    "triforce_hunt": TriforceHunt, 
    "triforce_goal": TriforceGoal,
    "extra_triforce_percentage": ExtraTriforces,
    "free_bombchu_drops": FreeBombchuDrops,

    "dungeon_shortcuts": DungeonShortcuts,
    "dungeon_shortcuts_list": DungeonShortcutsList,

    "mq_dungeons_mode": MQDungeons,
    "mq_dungeons_list": MQDungeonList,
    "mq_dungeons_count": MQDungeonCount,

    # "empty_dungeons_mode": EmptyDungeons,
    # "empty_dungeons_list": EmptyDungeonList,
    # "empty_dungeon_count": EmptyDungeonCount,
}


class BridgeStones(Range):
    """With Stones bridge: set the number of Spiritual Stones required."""
    display_name = "Spiritual Stones Required for Bridge"
    range_start = 0
    range_end = 3
    default = 3


class BridgeMedallions(Range):
    """With Medallions bridge: set the number of medallions required."""
    display_name = "Medallions Required for Bridge"
    range_start = 0
    range_end = 6
    default = 6


class BridgeRewards(Range):
    """With Dungeons bridge: set the number of dungeon rewards required."""
    display_name = "Dungeon Rewards Required for Bridge"
    range_start = 0
    range_end = 9
    default = 9


class BridgeTokens(Range):
    """With Tokens bridge: set the number of Gold Skulltula Tokens required."""
    display_name = "Tokens Required for Bridge"
    range_start = 0
    range_end = 100
    default = 40


class BridgeHearts(Range):
    """With Hearts bridge: set the number of hearts required."""
    display_name = "Hearts Required for Bridge"
    range_start = 4
    range_end = 20
    default = 20


bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": BridgeStones,
    "bridge_medallions": BridgeMedallions,
    "bridge_rewards": BridgeRewards, 
    "bridge_tokens": BridgeTokens,
    "bridge_hearts": BridgeHearts,
}


class SongShuffle(Choice):
    """Set where songs can appear.
    Song: Songs are shuffled into other song locations.
    Dungeon: Songs are placed into end-of-dungeon locations:
    - The 8 boss heart containers
    - Sheik in Ice Cavern
    - Lens of Truth chest in Bottom of the Well
    - Ice Arrows chest in Gerudo Training Ground
    - Impa at Hyrule Castle
    Any: Songs can appear anywhere in the multiworld."""
    display_name = "Shuffle Songs"
    option_song = 0
    option_dungeon = 1
    option_any = 2
    default = 0


class OcarinaSongs(OptionSet):
    """Randomize ocarina melody assignments.
    frog: Randomize the six standard songs.
    warp: Randomize the six warp songs.
    frogs2: Randomize the Zora's River Frogs Ocarina Game melody.

    Backward compatibility:
    all -> {'frog', 'warp'}
    """
    display_name = "Randomize Ocarina Melodies"
    valid_keys = {"frog", "warp", "frogs2"}
    default = set()

    @classmethod
    def from_any(cls, data):
        if isinstance(data, bool):
            return cls({"frog", "warp"} if data else set())
        if isinstance(data, str):
            lowered = data.strip().lower()
            if lowered in {"all", "true", "on", "yes", "1"}:
                return cls({"frog", "warp"})
            if lowered in {"frog", "warp", "frogs2"}:
                return cls({lowered})
            if lowered in {"false", "off", "no", "0", "none"}:
                return cls(set())
        return super().from_any(data)


class ShopShuffle(Choice): 
    """Randomizes shop contents.
    Off: Shops are not randomized at all.
    Fixed Number: Shop contents are shuffled, and a specific number of multiworld locations exist in each shop, controlled by the "shop_slots" option.
    Random Number: Same as Fixed Number, but the number of locations per shop is random and may differ between shops."""
    display_name = "Shopsanity"
    option_off = 0
    option_fixed_number = 1
    option_random_number = 2


class ShopSlots(Range):
    """With Shopsanity fixed number: quantity of multiworld locations per shop to be randomized."""
    display_name = "Shuffled Shop Slots"
    range_start = 0
    range_end = 4


class SpecialDealPriceDistribution(Choice):
    """Controls how prices are selected for shuffled shop special deal slots.
    Vanilla: Use the vanilla price tied to each shop slot.
    Betavariate: Weighted distribution across the min/max range.
    Uniform: Uniform distribution across the min/max range."""
    display_name = "Special Deal Prices"
    option_vanilla = 0
    option_betavariate = 1
    option_uniform = 2
    default = 1


class SpecialDealPriceMin(Range):
    """Minimum rupee price for shuffled shop special deal slots."""
    display_name = "Minimum Special Deal Price"
    range_start = 0
    range_end = 995
    default = 0


class SpecialDealPriceMax(Range):
    """Maximum rupee price for shuffled shop special deal slots."""
    display_name = "Maximum Special Deal Price"
    range_start = 0
    range_end = 995
    default = 300


class TokenShuffle(Choice): 
    """Token rewards from Gold Skulltulas can be shuffled into the pool.
    Dungeons: Only skulltulas in dungeons are shuffled.
    Overworld: Only skulltulas on the overworld (all skulltulas not in dungeons) are shuffled.
    All: Every skulltula is shuffled."""
    display_name = "Tokensanity"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ScrubShuffle(Choice): 
    """Shuffle the items sold by Business Scrubs, and set the prices.
    Off: Only the three business scrubs that sell one-time upgrades in vanilla will have items at their vanilla prices.
    Low/"Affordable": All scrub prices are 10 rupees.
    Regular/"Expensive": All scrub prices are vanilla.
    Random Prices: All scrub prices are randomized between 0 and 99 rupees."""
    display_name = "Scrub Shuffle"
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random_prices = 3
    alias_affordable = 1
    alias_expensive = 2


class ShuffleCows(Toggle):
    """Cows give items when Epona's Song is played."""
    display_name = "Shuffle Cows"


class ShuffleSword(Toggle):
    """Shuffle Kokiri Sword into the item pool."""
    display_name = "Shuffle Kokiri Sword"


class ShuffleOcarinas(Toggle):
    """Shuffle the Fairy Ocarina and Ocarina of Time into the item pool."""
    display_name = "Shuffle Ocarinas"


class ShuffleChildTrade(Choice):
    """Controls the behavior of the start of the child trade quest.
    Vanilla: Malon will give you the Weird Egg at Hyrule Castle.
    Shuffle: Malon will give you a random item, and the Weird Egg is shuffled.
    Skip Child Zelda: The game starts with Zelda already met, Zelda's Letter obtained, and the item from Impa obtained.
    """
    display_name = "Shuffle Child Trade Item"
    option_vanilla = 0
    option_shuffle = 1
    option_skip_child_zelda = 2
    alias_false = 0
    alias_true = 1


class ShuffleCard(Toggle):
    """Shuffle the Gerudo Membership Card into the item pool."""
    display_name = "Shuffle Gerudo Card"


class ShuffleBeans(Toggle):
    """Adds a pack of 10 beans to the item pool and changes the bean salesman to sell one item for 60 rupees."""
    display_name = "Shuffle Magic Beans"


class ShuffleMedigoronCarpet(Toggle):
    """Shuffle the items sold by Medigoron and the Haunted Wasteland Carpet Salesman."""
    display_name = "Shuffle Medigoron & Carpet Salesman"


class ShuffleFreestanding(Choice):
    """Shuffles freestanding rupees, recovery hearts, Shadow Temple Spinning Pots, and Goron Pot drops.
    Dungeons: Only freestanding items in dungeons are shuffled.
    Overworld: Only freestanding items in the overworld are shuffled.
    All: All freestanding items are shuffled."""
    display_name = "Shuffle Rupees & Hearts"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShufflePots(Choice):
    """Shuffles pots and flying pots which normally contain an item.
    Dungeons: Only pots in dungeons are shuffled.
    Overworld: Only pots in the overworld are shuffled.
    All: All pots are shuffled."""
    display_name = "Shuffle Pots"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShuffleCrates(Choice):
    """Shuffles large and small crates containing an item.
    Dungeons: Only crates in dungeons are shuffled.
    Overworld: Only crates in the overworld are shuffled.
    All: All crates are shuffled."""
    display_name = "Shuffle Crates"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShuffleBeehives(Toggle):
    """Beehives drop an item when destroyed by an explosion, the Hookshot, or the Boomerang."""
    display_name = "Shuffle Beehives"


class ShuffleWonderitems(Toggle):
    """Shuffles Wonderitems into the item pool."""
    display_name = "Shuffle Wonderitems"


class ShuffleFrogRupees(Toggle):
    """Shuffles the purple rupees received from the Zora's River frogs."""
    display_name = "Shuffle Frog Song Rupees"


class Shuffle100SkulltulaRupee(Toggle):
    """Shuffle the repeatable 200-rupee reward for collecting all 100 Gold Skulltulas."""
    display_name = "Shuffle 100 Skulltula Rupee Reward"


class ShuffleSilverRupees(Choice):
    """Shuffles the Silver Rupee puzzles into the item pool.
    Remove: Silver rupees are removed and puzzles are pre-solved.
    Vanilla: Silver rupees remain in their vanilla locations.
    Dungeon: Silver rupees are shuffled within their own dungeon.
    Overworld: Silver rupees are shuffled to overworld locations only.
    Any Dungeon: Silver rupees are shuffled across any dungeon.
    Regional: Silver rupees are shuffled within their region.
    Anywhere: Silver rupees can be anywhere in the multiworld."""
    display_name = "Shuffle Silver Rupees"
    option_vanilla = 0
    option_remove = 1
    option_dungeon = 2
    option_overworld = 3
    option_any_dungeon = 4
    option_regional = 5
    option_anywhere = 6
    default = 0


class ShuffleTCGKeys(Choice):
    """Shuffle Treasure Chest Game keys outside the minigame.
    Vanilla: Keys remain in the Treasure Chest Game.
    Shuffle: Keys are shuffled into the item pool.
    Remove: Keys are removed and chests are unlocked."""
    display_name = "Shuffle TCG Keys"
    option_vanilla = 0
    option_shuffle = 1
    option_remove = 2
    default = 0


class ShuffleIndividualOcarinaNotes(Toggle):
    """Locks all Ocarina inputs and adds 5 new items (A, C-up, C-down, C-left, C-right)
    that each unlock one of the 5 Ocarina notes."""
    display_name = "Shuffle Individual Ocarina Notes"


class TCGRequiresLens(Toggle):
    """Treasure Chest Game requires Lens of Truth to see which chests contain keys."""
    display_name = "TCG Requires Lens of Truth"


class ShuffleLoachReward(Toggle):
    """Shuffle the Hyrule Loach reward from the Fishing Pond."""
    display_name = "Shuffle Loach Reward"


class KeyRingsGiveBossKeys(Toggle):
    """When enabled, obtaining a key ring also grants the corresponding boss key."""
    display_name = "Key Rings Give Boss Keys"


class KeyAppearanceMatchesDungeon(Toggle):
    """Small key models match their dungeon. Requires keysanity or key ring shuffle."""
    display_name = "Key Appearance Matches Dungeon"


class RutoAlreadyAtF1(Toggle):
    """Ruto starts at the first switch in Jabu instead of needing to be carried."""
    display_name = "Ruto Already at F1"


class MaintainMaskEquips(Toggle):
    """Equipped masks stay equipped when using ocarina or picking up items."""
    display_name = "Maintain Mask Equips"


shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "ocarina_songs": OcarinaSongs,
    "shopsanity": ShopShuffle,
    "shop_slots": ShopSlots,
    "special_deal_price_distribution": SpecialDealPriceDistribution,
    "special_deal_price_min": SpecialDealPriceMin,
    "special_deal_price_max": SpecialDealPriceMax,
    "tokensanity": TokenShuffle,
    "shuffle_scrubs": ScrubShuffle,
    "shuffle_child_trade": ShuffleChildTrade,
    "shuffle_freestanding_items": ShuffleFreestanding,
    "shuffle_pots": ShufflePots,
    "shuffle_crates": ShuffleCrates,
    "shuffle_cows": ShuffleCows,
    "shuffle_beehives": ShuffleBeehives,
    "shuffle_wonderitems": ShuffleWonderitems,
    "shuffle_kokiri_sword": ShuffleSword,
    "shuffle_ocarinas": ShuffleOcarinas,
    "shuffle_gerudo_card": ShuffleCard,
    "shuffle_beans": ShuffleBeans,
    "shuffle_medigoron_carpet_salesman": ShuffleMedigoronCarpet,
    "shuffle_frog_song_rupees": ShuffleFrogRupees,
    "shuffle_100_skulltula_rupee": Shuffle100SkulltulaRupee,
    "shuffle_silver_rupees": ShuffleSilverRupees,
    "shuffle_tcgkeys": ShuffleTCGKeys,
    "shuffle_individual_ocarina_notes": ShuffleIndividualOcarinaNotes,
    "tcg_requires_lens": TCGRequiresLens,
    "shuffle_loach_reward": ShuffleLoachReward,
}


class ShuffleDungeonRewards(Choice):
    """Control where Medallions and Spiritual Stones can be placed.
    Vanilla: Rewards appear at their vanilla locations (blue warps in their respective dungeons).
    Reward: Rewards are shuffled among all nine blue-warp reward locations.
    Dungeon: Each reward is shuffled within its own dungeon.
    Regional: Rewards are shuffled within their region.
    Overworld: Rewards are shuffled into overworld locations only.
    Any Dungeon: Rewards are shuffled into any dungeon location.
    Anywhere: Rewards are shuffled into any location in the pool."""
    display_name = "Shuffle Dungeon Rewards"
    option_vanilla = 0
    option_reward = 1
    option_dungeon = 2
    option_regional = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_anywhere = 6
    default = 1


class ShuffleMap(Choice):
    """Control where to shuffle dungeon maps.
    Remove: There will be no maps in the itempool.
    Startwith: You start with all maps.
    Vanilla: Maps remain vanilla.
    Dungeon: Maps are shuffled within their original dungeon.
    Regional: Maps are shuffled only in regions near the original dungeon.
    Overworld: Maps are shuffled locally outside of dungeons.
    Any Dungeon: Maps are shuffled locally in any dungeon.
    Keysanity: Maps can be anywhere in the multiworld."""
    display_name = "Maps"
    option_remove = 0
    option_startwith = 1
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 1
    alias_anywhere = 7


class ShuffleCompass(Choice):
    """Control where to shuffle dungeon compasses.
    Remove: There will be no compasses in the itempool.
    Startwith: You start with all compasses.
    Vanilla: Compasses remain vanilla.
    Dungeon: Compasses are shuffled within their original dungeon.
    Regional: Compasses are shuffled only in regions near the original dungeon.
    Overworld: Compasses are shuffled locally outside of dungeons.
    Any Dungeon: Compasses are shuffled locally in any dungeon.
    Keysanity: Compasses can be anywhere in the multiworld."""
    display_name = "Compasses"
    option_remove = 0
    option_startwith = 1
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 1
    alias_anywhere = 7


class ShuffleKeys(Choice): 
    """Control where to shuffle dungeon small keys.
    Remove/"Keysy": There will be no small keys in the itempool. All small key doors are automatically unlocked.
    Vanilla: Small keys remain vanilla. You may start with extra small keys in some dungeons to prevent softlocks.
    Dungeon: Small keys are shuffled within their original dungeon.
    Regional: Small keys are shuffled only in regions near the original dungeon.
    Overworld: Small keys are shuffled locally outside of dungeons.
    Any Dungeon: Small keys are shuffled locally in any dungeon.
    Keysanity: Small keys can be anywhere in the multiworld."""
    display_name = "Small Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 3
    alias_keysy = 0
    alias_anywhere = 7


class ShuffleGerudoKeys(Choice): 
    """Control where to shuffle the Thieves' Hideout small keys.
    Vanilla: Hideout keys remain vanilla.
    Regional: Hideout keys are shuffled only in the Gerudo Valley/Desert Colossus area.
    Overworld: Hideout keys are shuffled locally outside of dungeons.
    Any Dungeon: Hideout keys are shuffled locally in any dungeon.
    Keysanity: Hideout keys can be anywhere in the multiworld."""
    display_name = "Thieves' Hideout Keys"
    option_vanilla = 0
    option_regional = 1
    option_overworld = 2
    option_any_dungeon = 3
    option_keysanity = 4
    alias_anywhere = 4


class ShuffleBossKeys(Choice): 
    """Control where to shuffle boss keys, except the Ganon's Castle Boss Key.
    Remove/"Keysy": There will be no boss keys in the itempool. All boss key doors are automatically unlocked.
    Vanilla: Boss keys remain vanilla. You may start with extra small keys in some dungeons to prevent softlocks.
    Dungeon: Boss keys are shuffled within their original dungeon.
    Regional: Boss keys are shuffled only in regions near the original dungeon.
    Overworld: Boss keys are shuffled locally outside of dungeons.
    Any Dungeon: Boss keys are shuffled locally in any dungeon.
    Keysanity: Boss keys can be anywhere in the multiworld."""
    display_name = "Boss Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 3
    alias_keysy = 0
    alias_anywhere = 7


class ShuffleGanonBK(Choice):
    """Control how to shuffle the Ganon's Castle Boss Key (GCBK).
    Remove: GCBK is removed, and the boss key door is automatically unlocked.
    Vanilla: GCBK remains vanilla.
    Dungeon: GCBK is shuffled within its original dungeon.
    Regional: GCBK is shuffled only in Hyrule Field, Market, and Hyrule Castle areas.
    Overworld: GCBK is shuffled locally outside of dungeons.
    Any Dungeon: GCBK is shuffled locally in any dungeon.
    Keysanity: GCBK can be anywhere in the multiworld.
    On LACS: GCBK is on the Light Arrow Cutscene, which requires Shadow and Spirit Medallions.
    Stones: GCBK will be awarded when reaching the target number of Spiritual Stones.
    Medallions: GCBK will be awarded when reaching the target number of medallions.
    Dungeons: GCBK will be awarded when reaching the target number of dungeon rewards.
    Tokens: GCBK will be awarded when reaching the target number of Gold Skulltula Tokens.
    Hearts: GCBK will be awarded when reaching the target number of hearts.
    """
    display_name = "Ganon's Boss Key"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    option_on_lacs = 8
    option_stones = 9
    option_medallions = 10
    option_dungeons = 11
    option_tokens = 12
    option_hearts = 13
    default = 0
    alias_keysy = 0
    alias_anywhere = 7


class EnhanceMC(OptionSet):
    """Gives maps/compasses extra functionality.
    map_mq: Map tells if a dungeon is vanilla or MQ.
    map_dungeon_location: Map tells where a dungeon entrance leads.
    compass_boss_location: Compass tells which boss is in the dungeon.
    compass_reward: Compass tells what dungeon reward is in the dungeon.

    Backward compatibility:
    true -> {'map_mq', 'compass_reward'}
    false -> {}
    """
    display_name = "Maps and Compasses Give Information"
    valid_keys = {"map_mq", "map_dungeon_location", "compass_boss_location", "compass_reward"}
    default = set()

    @classmethod
    def from_any(cls, data):
        if isinstance(data, bool):
            return cls({"map_mq", "compass_reward"} if data else set())
        if isinstance(data, str):
            lowered = data.strip().lower()
            if lowered in {"true", "on", "yes", "1"}:
                return cls({"map_mq", "compass_reward"})
            if lowered in {"false", "off", "no", "0"}:
                return cls(set())
        return super().from_any(data)


class GanonBKMedallions(Range):
    """With medallions GCBK: set how many medallions are required to receive GCBK."""
    display_name = "Medallions Required for Ganon's BK"
    range_start = 1
    range_end = 6
    default = 6


class GanonBKStones(Range):
    """With stones GCBK: set how many Spiritual Stones are required to receive GCBK."""
    display_name = "Spiritual Stones Required for Ganon's BK"
    range_start = 1
    range_end = 3
    default = 3


class GanonBKRewards(Range):
    """With dungeons GCBK: set how many dungeon rewards are required to receive GCBK."""
    display_name = "Dungeon Rewards Required for Ganon's BK"
    range_start = 1
    range_end = 9
    default = 9


class GanonBKTokens(Range):
    """With tokens GCBK: set how many Gold Skulltula Tokens are required to receive GCBK."""
    display_name = "Tokens Required for Ganon's BK"
    range_start = 1
    range_end = 100
    default = 40


class GanonBKHearts(Range):
    """With hearts GCBK: set how many hearts are required to receive GCBK."""
    display_name = "Hearts Required for Ganon's BK"
    range_start = 4
    range_end = 20
    default = 20


class KeyRings(Choice):
    """A key ring grants all dungeon small keys at once, rather than individually.
    Choose: Use the option "key_rings_list" to choose which dungeons have key rings.
    All: All dungeons have key rings instead of small keys."""
    display_name = "Key Rings Mode"
    option_off = 0
    option_choose = 1
    option_all = 2
    option_random_dungeons = 3


class KeyRingList(OptionSet):
    """With key rings as Choose: select areas with key rings rather than individual small keys."""
    display_name = "Key Ring Areas"
    valid_keys = {
        "Thieves' Hideout",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
        "Bottom of the Well",
        "Gerudo Training Ground",
        "Ganon's Castle",
        "Treasure Chest Game"
    }


dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_dungeon_rewards": ShuffleDungeonRewards,
    "shuffle_map": ShuffleMap,
    "shuffle_compass": ShuffleCompass,
    "shuffle_smallkeys": ShuffleKeys,
    "shuffle_hideoutkeys": ShuffleGerudoKeys,
    "shuffle_bosskeys": ShuffleBossKeys,
    "enhance_map_compass": EnhanceMC,
    "shuffle_ganon_bosskey": ShuffleGanonBK,
    "ganon_bosskey_medallions": GanonBKMedallions,
    "ganon_bosskey_stones": GanonBKStones,
    "ganon_bosskey_rewards": GanonBKRewards,
    "ganon_bosskey_tokens": GanonBKTokens,
    "ganon_bosskey_hearts": GanonBKHearts,
    "key_rings": KeyRings,
    "key_rings_list": KeyRingList,
    "key_rings_give_bosskeys": KeyRingsGiveBossKeys
}


class SkipEscape(DefaultOnToggle):
    """Skips the tower collapse sequence between the Ganondorf and Ganon fights."""
    display_name = "Skip Tower Escape Sequence"


class SkipStealth(DefaultOnToggle):
    """The crawlspace into Hyrule Castle skips straight to Zelda."""
    display_name = "Skip Child Stealth"


class SkipEponaRace(DefaultOnToggle):
    """Epona can always be summoned with Epona's Song."""
    display_name = "Skip Epona Race"


class SkipMinigamePhases(DefaultOnToggle):
    """Dampe Race and Horseback Archery give both rewards if the second condition is met on the first attempt."""
    display_name = "Skip Some Minigame Phases"


class CompleteMaskQuest(Toggle):
    """All masks are immediately available to borrow from the Happy Mask Shop."""
    display_name = "Complete Mask Quest"


class UsefulCutscenes(Toggle):
    """Reenables the Poe cutscene in Forest Temple, Darunia in Fire Temple, and Twinrova introduction. Mostly useful for
     advanced logic."""
    display_name = "Enable Useful Cutscenes"


class FastChests(DefaultOnToggle):
    """All chest animations are fast. If disabled, major items have a slow animation."""
    display_name = "Fast Chest Cutscenes"


class ScarecrowBehavior(Choice):
    """Set scarecrow song behavior.
    Vanilla: Standard game behavior.
    Fast: Shared scarecrow song behavior is simplified.
    Free: Pierre can be summoned without setting the song."""
    display_name = "Scarecrow Song"
    option_vanilla = 0
    option_fast = 1
    option_free = 2
    default = 0
    alias_false = 0
    alias_true = 2


class FastBunny(Toggle):
    """Bunny Hood lets you move 1.5x faster like in Majora's Mask."""
    display_name = "Fast Bunny Hood"


class PlantBeans(Toggle):
    """Pre-plants all 10 magic beans in the soft soil spots."""
    display_name = "Plant Magic Beans"


class ChickenCount(Range):
    """Controls the number of Cuccos for Anju to give an item as child."""
    display_name = "Cucco Count"
    range_start = 0
    range_end = 7
    default = 7


class BigPoeCount(Range):
    """Number of Big Poes required for the Poe Collector's item."""
    display_name = "Big Poe Count"
    range_start = 1
    range_end = 10
    default = 1


class FAETorchCount(Range):
    """Number of lit torches required to open Shadow Temple.
    Does not affect logic; use the trick Shadow Temple Entry with Fire Arrows if desired."""
    display_name = "Fire Arrow Entry Torch Count"
    range_start = 1
    range_end = 23
    default = 3


class EasierFireArrowEntry(Toggle):
    """Allow reducing the number of lit torches required to open Shadow Temple with Fire Arrows."""
    display_name = "Easier Fire Arrow Entry"


class FastShadowBoat(Toggle):
    """Speed up the boat ride in the Shadow Temple."""
    display_name = "Fast Shadow Temple Boat"


class SkipRewardFromRauru(Choice):
    """Control whether the item Rauru gives beyond the Door of Time is given as a starting item.
    Not Free: Rauru gives the reward when you go beyond the Door of Time.
    Free: You begin the game with the reward Rauru normally gives. If dungeon rewards are shuffled
    elsewhere, the Rauru reward is shuffled along with them.
    Free Forced: You begin the game with the reward Rauru normally gives, and the ToT Reward
    location is forced to contain a dungeon reward even when rewards are shuffled to other pools."""
    display_name = "Free Reward from Rauru"
    option_not_free = 0
    option_free = 1
    option_free_forced = 2
    default = 0
    alias_false = 0
    alias_true = 1


timesavers_options: typing.Dict[str, type(Option)] = {
    "no_escape_sequence": SkipEscape,
    "no_guard_stealth": SkipStealth,
    "no_epona_race": SkipEponaRace,
    "skip_some_minigame_phases": SkipMinigamePhases,
    "complete_mask_quest": CompleteMaskQuest,
    "useful_cutscenes": UsefulCutscenes,
    "fast_chests": FastChests,
    "scarecrow_behavior": ScarecrowBehavior,
    "fast_bunny_hood": FastBunny,
    "plant_beans": PlantBeans,
    "easier_fire_arrow_entry": EasierFireArrowEntry,
    "chicken_count": ChickenCount,
    "big_poe_count": BigPoeCount,
    "fae_torch_count": FAETorchCount,
    "fast_shadow_boat": FastShadowBoat,
    "skip_reward_from_rauru": SkipRewardFromRauru,
}


class CorrectChestAppearance(Choice):
    """Changes chest textures and/or sizes to match their contents.
    Off: All chests have their vanilla size/appearance.
    Textures: Chest textures reflect their contents.
    Both: Like Textures, but progression items and boss keys get big chests, and other items get small chests.
    Classic: Old behavior of CSMC; textures distinguish keys from non-keys, and size distinguishes importance."""
    display_name = "Chest Appearance Matches Contents"
    option_off = 0
    option_textures = 1
    option_both = 2
    option_classic = 3


class MinorInMajor(OptionSet):
    """Minor items appear in big/gold chests.
    bombchus: Bombchus appear in big/gold chests.
    shields: Hylian Shield and Deku Shield appear in big/gold chests.
    capacity: Deku Stick and Deku Nut capacity upgrades appear in big/gold chests."""
    display_name = "Minor Items in Big/Gold Chests"
    valid_keys = {"bombchus", "shields", "capacity"}

    @classmethod
    def from_any(cls, data) -> "MinorInMajor":
        if data is True or data == 1:
            return cls.from_any({"bombchus", "shields", "capacity"})
        if data is False or data == 0:
            return cls.from_any(set())
        return super().from_any(data)


class InvisibleChests(Toggle):
    """Chests visible only with Lens of Truth. Logic is not changed."""
    display_name = "Invisible Chests"


class CorrectPotCrateAppearance(Choice):
    """Changes the appearance of pots, crates, and beehives that contain items.
    Off: Vanilla appearance for all containers.
    Textures (Content): Unchecked pots and crates have a texture reflecting their contents. Unchecked beehives with progression items will wiggle.
    Textures (Unchecked): Unchecked pots and crates are golden. Unchecked beehives will wiggle.
    """
    display_name = "Pot, Crate, and Beehive Appearance"
    option_off = 0
    option_textures_content = 1
    option_textures_unchecked = 2
    default = 2


class Hints(Choice): 
    """Gossip Stones can give hints about item locations.
    None: Gossip Stones do not give hints.
    Mask: Gossip Stones give hints with Mask of Truth.
    Agony: Gossip Stones give hints wtih Stone of Agony.
    Always: Gossip Stones always give hints."""
    display_name = "Gossip Stones"
    option_none = 0
    option_mask = 1
    option_agony = 2
    option_always = 3
    default = 3


class MiscHints(OptionSet):
    """Choose which miscellaneous hints are enabled.

    Temple of Time Altar hints dungeon rewards, bridge info, and Ganon BK info.
    Ganondorf hints the Light Arrows.
    Dampe's Diary hints a local Hookshot if one exists.
    Skulltula House locations hint their item at various token counts.
    Frogs Ocarina Game hints the final reward."""
    display_name = "Misc Hints"
    valid_keys = {
        "altar",
        "dampe_diary",
        "ganondorf",
        "warp_songs_and_owls",
        "10_skulltulas",
        "20_skulltulas",
        "30_skulltulas",
        "40_skulltulas",
        "50_skulltulas",
        "100_skulltulas",
        "frogs2",
        "skull_mask",
        "mask_of_truth",
        "mask_shop",
        "unique_merchants",
        "big_poes",
    }
    default = {
        "altar",
        "dampe_diary",
        "ganondorf",
        "warp_songs_and_owls",
        "10_skulltulas",
        "20_skulltulas",
        "30_skulltulas",
        "40_skulltulas",
        "50_skulltulas",
        "frogs2",
    }


class HintDistribution(Choice):
    """Choose the hint distribution to use. Affects the frequency of strong hints, which items are always hinted, etc.
    Detailed documentation on hint distributions can be found on OoTRandomizer.com.
    The Async hint distribution is intended for async multiworlds. It removes Way of the Hero hints to improve generation times, since they are not very useful in asyncs."""
    display_name = "Hint Distribution"
    option_balanced = 0
    option_ddr = 1
    # option_league = 2
    # option_mw3 = 3
    option_scrubs = 4
    option_strong = 5
    # option_tournament = 6
    option_useless = 7
    option_very_strong = 8
    option_async = 9
    default = 9


class TextShuffle(Choice): 
    """Randomizes text in the game for comedic effect.
    Except Hints: does not randomize important text such as hints, small/boss key information, and item prices.
    Complete: randomizes every textbox, including the useful ones."""
    display_name = "Text Shuffle"
    option_none = 0
    option_except_hints = 1
    option_complete = 2
    alias_false = 0


class DamageMultiplier(Choice): 
    """Controls the amount of damage Link takes."""
    display_name = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1


class DeadlyBonks(Choice):
    """Bonking on a wall or object will hurt Link. "Normal" is a half heart of damage."""
    display_name = "Bonks Do Damage"
    option_none = 0
    option_half = 1
    option_normal = 2
    option_double = 3
    option_quadruple = 4
    option_ohko = 5


class HeroMode(Toggle):
    """Hearts will not drop from enemies or objects."""
    display_name = "Hero Mode"


class StartingToD(Choice):
    """Change the starting time of day.
    Daytime starts at Sunrise and ends at Sunset. Default is between Morning and Noon."""
    display_name = "Starting Time of Day"
    option_default = 0
    option_sunrise = 1
    option_morning = 2
    option_noon = 3
    option_afternoon = 4
    option_sunset = 5
    option_evening = 6
    option_midnight = 7
    option_witching_hour = 8


class BlueFireArrows(Toggle):
    """Ice arrows can melt red ice and break the mud walls in Dodongo's Cavern."""
    display_name = "Blue Fire Arrows"


class FixBrokenDrops(Toggle):
    """Fixes two broken vanilla drops: deku shield in child Spirit Temple, and magic drop on GTG eye statue."""
    display_name = "Fix Broken Drops"


class ConsumableStart(Toggle):
    """Start the game with full Deku Sticks and Deku Nuts."""
    display_name = "Start with Consumables"


class RupeeStart(Toggle):
    """Start with a full wallet. Wallet upgrades will also fill your wallet."""
    display_name = "Start with Rupees"


misc_options: typing.Dict[str, type(Option)] = {
    "correct_chest_appearances": CorrectChestAppearance,
    "minor_items_as_major_chest": MinorInMajor,
    "invisible_chests": InvisibleChests,
    "correct_potcrate_appearances": CorrectPotCrateAppearance,
    "key_appearance_matches_dungeon": KeyAppearanceMatchesDungeon,
    "ruto_already_at_f1": RutoAlreadyAtF1,
    "maintain_mask_equips": MaintainMaskEquips,
    "hints": Hints,
    "misc_hints": MiscHints,
    "hint_dist": HintDistribution,
    "text_shuffle": TextShuffle,
    "damage_multiplier": DamageMultiplier,
    "deadly_bonks": DeadlyBonks,
    "no_collectible_hearts": HeroMode,
    "starting_tod": StartingToD,
    "blue_fire_arrows": BlueFireArrows,
    "fix_broken_drops": FixBrokenDrops,
    "start_with_consumables": ConsumableStart,
    "start_with_rupees": RupeeStart,
}

class ItemPoolValue(Choice): 
    """Changes the number of items available in the game.
    Plentiful: One extra copy of every major item.
    Balanced: Original item pool.
    Scarce: Extra copies of major items are removed. Heart containers are removed.
    Minimal: All major item upgrades not used for locations are removed. All health is removed."""
    display_name = "Item Pool"
    option_plentiful = 0
    option_balanced = 1
    option_scarce = 2
    option_minimal = 3
    default = 1


class IceTraps(Choice): 
    """Adds ice traps to the item pool.
    Off: All ice traps are removed.
    Normal: The vanilla quantity of ice traps are placed.
    On/"Extra": There is a chance for some extra ice traps to be placed.
    Mayhem: All added junk items are ice traps.
    Onslaught: All junk items are replaced by ice traps, even those in the base pool."""
    display_name = "Ice Traps"
    option_off = 0
    option_normal = 1
    option_on = 2
    option_mayhem = 3
    option_onslaught = 4
    option_custom_count = 5
    option_custom_percent = 6
    default = 1
    alias_extra = 2


class CustomIceTrapPercent(Range):
    """Percentage of junk items replaced by ice traps when Ice Traps is set to Custom (%)."""
    display_name = "Custom Ice Trap Percent"
    range_start = 0
    range_end = 100
    default = 50


class CustomIceTrapCount(Range):
    """Number of junk items replaced by ice traps when Ice Traps is set to Custom (count)."""
    display_name = "Custom Ice Trap Count"
    range_start = 0
    range_end = 2000
    default = 100


class IceTrapVisual(Choice): 
    """Changes the appearance of traps, including other games' traps, as freestanding items."""
    display_name = "Trap Appearance"
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2


adult_trade_items = frozenset({
    "Pocket Egg",
    "Pocket Cucco",
    "Cojiro",
    "Odd Mushroom",
    "Odd Potion",
    "Poachers Saw",
    "Broken Sword",
    "Prescription",
    "Eyeball Frog",
    "Eyedrops",
    "Claim Check",
})

class AdultTradeStart(OptionSet):
    """Select the adult trade sequence items to shuffle.
    If Shuffle All Selected Adult Trade Items is off, one selected item starts the adult trade sequence.
    If Shuffle All Selected Adult Trade Items is on, every selected item is shuffled."""
    display_name = "Shuffle Adult Trade Sequence Items"
    valid_keys = adult_trade_items
    default = adult_trade_items


class AdultTradeShuffleOption(Toggle):
    """Shuffle every selected adult trade sequence item into the item pool."""
    display_name = "Shuffle All Selected Adult Trade Items"


class AddRandomStartingItems(Toggle):
    """Add random progression-safe starting items to start inventory."""
    display_name = "Additional Random Starting Items"


class RandomStartingItemsCount(Range):
    """How many additional random starting items to grant."""
    display_name = "Amount of Random Starting Items"
    range_start = 0
    range_end = 10
    default = 0


class RandomStartingItemsExclude(OptionSet):
    """Exclude item categories from random starting item selection."""
    display_name = "Exclude From Random Starting Items"
    valid_keys = {"songs", "bombchus", "shields", "deku_upgrades", "health_upgrades", "junk"}
    default = set()


itempool_options: typing.Dict[str, type(Option)] = {
    "item_pool_value": ItemPoolValue,
    "junk_ice_traps": IceTraps,
    "custom_ice_trap_percent": CustomIceTrapPercent,
    "custom_ice_trap_count": CustomIceTrapCount,
    "ice_trap_appearance": IceTrapVisual,
    "adult_trade_shuffle": AdultTradeShuffleOption,
    "adult_trade_start": AdultTradeStart,
    "add_random_starting_items": AddRandomStartingItems,
    "random_starting_items_count": RandomStartingItemsCount,
    "random_starting_items_exclude": RandomStartingItemsExclude,
}

# Start of cosmetic options

class Targeting(Choice): 
    """Default targeting option."""
    display_name = "Default Targeting Option"
    option_hold = 0
    option_switch = 1


class DisplayDpad(Choice):
    """Show dpad icon on HUD for quick actions (ocarina, hover boots, iron boots, mask).
    On: D-Pad shown on the right side (default).
    Left: D-Pad shown on the left side.
    Off: D-Pad hidden."""
    display_name = "Display D-Pad HUD"
    option_off = 0
    option_on = 1
    option_left = 2
    default = 1


class DpadDungeonMenu(DefaultOnToggle):
    """Show separated menus on the pause screen for dungeon keys, rewards, and Vanilla/MQ info."""
    display_name = "Display D-Pad Dungeon Info"


class CorrectColors(DefaultOnToggle):
    """Makes in-game models match their HUD element colors."""
    display_name = "Item Model Colors Match Cosmetics"


class Music(Choice): 
    option_normal = 0
    option_off = 1
    option_randomized = 2


class BackgroundMusic(Music):
    """Randomize or disable background music."""
    display_name = "Background Music"


class Fanfares(Music):
    """Randomize or disable item fanfares."""
    display_name = "Fanfares"


class OcarinaFanfares(Toggle):
    """Enable ocarina songs as fanfares. These are longer than usual fanfares. Does nothing without fanfares randomized."""
    display_name = "Ocarina Songs as Fanfares"


class SwordTrailDuration(Range):
    """Set the duration for sword trails."""
    display_name = "Sword Trail Duration"
    range_start = 4
    range_end = 20
    default = 4


class SpeedupMusicForLastTriforcePiece(Toggle):
    """In Triforce Hunt, speed up the music slightly when one piece away from the goal."""
    display_name = "Speed Up Music for Last Triforce Piece"


class SlowdownMusicWhenLowhp(Toggle):
    """Slow down the background music when at critically low health."""
    display_name = "Slowdown Music When Low HP"


class UninvertYAxisInFirstPersonCamera(Toggle):
    """Uninvert the Y-axis when in first-person camera mode (e.g. arrow aiming)."""
    display_name = "Uninvert Y-Axis in First Person Camera"


class InputViewer(Toggle):
    """Show a controller input display on screen."""
    display_name = "Input Viewer"


class DisableBattleMusic(Toggle):
    """Prevent background music from being interrupted by the battle theme when near enemies."""
    display_name = "Disable Battle Music"


class DisplayCustomSongNames(Choice):
    """When music is randomized, display the custom track name on screen."""
    display_name = "Display Custom Song Names"
    option_off = 0
    option_top = 1
    option_pause = 2


class CreditsMusic(Toggle):
    """Include the credits roll sequences in the background music shuffle pool."""
    display_name = "Credits Music as BGM"


cosmetic_options: typing.Dict[str, type(Option)] = {
    "default_targeting": Targeting,
    "display_dpad": DisplayDpad,
    "dpad_dungeon_menu": DpadDungeonMenu,
    "speedup_music_for_last_triforce_piece": SpeedupMusicForLastTriforcePiece,
    "slowdown_music_when_lowhp": SlowdownMusicWhenLowhp,
    "uninvert_y_axis_in_first_person_camera": UninvertYAxisInFirstPersonCamera,
    "input_viewer": InputViewer,
    "disable_battle_music": DisableBattleMusic,
    "display_custom_song_names": DisplayCustomSongNames,
    "credits_music": CreditsMusic,
    "correct_model_colors": CorrectColors,
    "background_music": BackgroundMusic,
    "fanfares": Fanfares,
    "ocarina_fanfares": OcarinaFanfares,
    "kokiri_color": kokiri_color,
    "goron_color":  goron_color,
    "zora_color":   zora_color,
    "silver_gauntlets_color":   silver_gauntlets_color,
    "golden_gauntlets_color":   golden_gauntlets_color,
    "mirror_shield_frame_color": mirror_shield_frame_color,
    "navi_color_default_inner": navi_color_default_inner,
    "navi_color_default_outer": navi_color_default_outer,
    "navi_color_enemy_inner":   navi_color_enemy_inner,
    "navi_color_enemy_outer":   navi_color_enemy_outer,
    "navi_color_npc_inner":     navi_color_npc_inner,
    "navi_color_npc_outer":     navi_color_npc_outer,
    "navi_color_prop_inner":    navi_color_prop_inner,
    "navi_color_prop_outer":    navi_color_prop_outer,
    "sword_trail_duration": SwordTrailDuration,
    "sword_trail_color_inner": sword_trail_color_inner,
    "sword_trail_color_outer": sword_trail_color_outer,
    "bombchu_trail_color_inner": bombchu_trail_color_inner,
    "bombchu_trail_color_outer": bombchu_trail_color_outer,
    "boomerang_trail_color_inner": boomerang_trail_color_inner,
    "boomerang_trail_color_outer": boomerang_trail_color_outer,
    "heart_color":          heart_color,
    "magic_color":          magic_color,
    "a_button_color":       a_button_color,
    "b_button_color":       b_button_color,
    "c_button_color":       c_button_color,
    "start_button_color":   start_button_color,
}

class SfxOcarina(Choice):
    """Change the sound of the ocarina."""
    display_name = "Ocarina Instrument"
    option_ocarina = 1
    option_malon = 2
    option_whistle = 3
    option_harp = 4
    option_grind_organ = 5
    option_flute = 6
    default = 1

sfx_options: typing.Dict[str, type(Option)] = {
    "sfx_navi_overworld":   sfx_navi_overworld,
    "sfx_navi_enemy":       sfx_navi_enemy,
    "sfx_low_hp":           sfx_low_hp,
    "sfx_menu_cursor":      sfx_menu_cursor,
    "sfx_menu_select":      sfx_menu_select,
    "sfx_nightfall":        sfx_nightfall,
    "sfx_horse_neigh":      sfx_horse_neigh,
    "sfx_hover_boots":      sfx_hover_boots,
    "sfx_iron_boots":       sfx_iron_boots,
    "sfx_silver_rupee":     sfx_silver_rupee,
    "sfx_boomerang_throw":  sfx_boomerang_throw,
    "sfx_hookshot_chain":   sfx_hookshot_chain,
    "sfx_arrow_shot":       sfx_arrow_shot,
    "sfx_slingshot_shot":   sfx_slingshot_shot,
    "sfx_magic_arrow_shot": sfx_magic_arrow_shot,
    "sfx_bombchu_move":     sfx_bombchu_move,
    "sfx_get_small_item":   sfx_get_small_item,
    "sfx_explosion":        sfx_explosion,
    "sfx_daybreak":         sfx_daybreak,
    "sfx_cucco":            sfx_cucco,
    "sfx_ocarina":          SfxOcarina,
}


class LogicTricks(OptionSet):
    """Set various tricks for logic in Ocarina of Time.
    Format as a comma-separated list of "nice" names: ["Fewer Tunic Requirements", "Hidden Grottos without Stone of Agony"].
    """
    display_name = "Logic Tricks"
    valid_keys = tuple(normalized_name_tricks.keys())
    valid_keys_casefold = True


class AdvancedAllowedTricks(OptionSet):
    """When Logic Rules is set to Advanced, choose which glitch and advanced tricks are in logic.
    Format as a comma-separated list of "nice" names:
    ["(Glitch) Infinite Sword Glitch (ISG)", "(Glitch) Hovering with Explosives"].
    """
    display_name = "Advanced Allowed Tricks"
    valid_keys = tuple(normalized_name_advanced_tricks.keys())
    valid_keys_casefold = True


@dataclass
class OoTOptions(PerGameCommonOptions):
    plando_connections: OoTPlandoConnections
    plandomized_locations: PlandomizedLocations
    death_link: DeathLink
    logic_rules: Logic
    logic_no_night_tokens_without_suns_song: NightTokens
    logic_tricks: LogicTricks
    advanced_allowed_tricks: AdvancedAllowedTricks
    open_forest: Forest
    open_kakariko: Gate
    open_door_of_time: DoorOfTime
    zora_fountain: Fountain
    gerudo_fortress: Fortress
    bridge: Bridge
    trials: Trials
    starting_age: StartingAge
    shuffle_interior_entrances: InteriorEntrances
    shuffle_grotto_entrances: GrottoEntrances
    shuffle_dungeon_entrances: DungeonEntrances
    shuffle_overworld_entrances: OverworldEntrances
    owl_drops: OwlDrops
    warp_songs: WarpSongs
    spawn_positions: SpawnPositions
    shuffle_bosses: BossEntrances
    shuffle_ganon_tower: ShuffleGanonTower
    # mix_entrance_pools: MixEntrancePools
    # decouple_entrances: DecoupleEntrances
    triforce_hunt: TriforceHunt
    triforce_goal: TriforceGoal
    extra_triforce_percentage: ExtraTriforces
    free_bombchu_drops: FreeBombchuDrops
    dungeon_shortcuts: DungeonShortcuts
    dungeon_shortcuts_list: DungeonShortcutsList
    mq_dungeons_mode: MQDungeons
    mq_dungeons_list: MQDungeonList
    mq_dungeons_count: MQDungeonCount
    # empty_dungeons_mode: EmptyDungeons
    # empty_dungeons_list: EmptyDungeonList
    # empty_dungeon_count: EmptyDungeonCount
    bridge_stones: BridgeStones
    bridge_medallions: BridgeMedallions
    bridge_rewards: BridgeRewards
    bridge_tokens: BridgeTokens
    bridge_hearts: BridgeHearts
    shuffle_dungeon_rewards: ShuffleDungeonRewards
    shuffle_map: ShuffleMap
    shuffle_compass: ShuffleCompass
    shuffle_smallkeys: ShuffleKeys
    shuffle_hideoutkeys: ShuffleGerudoKeys
    shuffle_bosskeys: ShuffleBossKeys
    enhance_map_compass: EnhanceMC
    shuffle_ganon_bosskey: ShuffleGanonBK
    ganon_bosskey_medallions: GanonBKMedallions
    ganon_bosskey_stones: GanonBKStones
    ganon_bosskey_rewards: GanonBKRewards
    ganon_bosskey_tokens: GanonBKTokens
    ganon_bosskey_hearts: GanonBKHearts
    key_rings: KeyRings
    key_rings_list: KeyRingList
    shuffle_song_items: SongShuffle
    ocarina_songs: OcarinaSongs
    shopsanity: ShopShuffle
    shop_slots: ShopSlots
    special_deal_price_distribution: SpecialDealPriceDistribution
    special_deal_price_min: SpecialDealPriceMin
    special_deal_price_max: SpecialDealPriceMax
    tokensanity: TokenShuffle
    shuffle_scrubs: ScrubShuffle
    shuffle_child_trade: ShuffleChildTrade
    shuffle_freestanding_items: ShuffleFreestanding
    shuffle_pots: ShufflePots
    shuffle_crates: ShuffleCrates
    shuffle_cows: ShuffleCows
    shuffle_beehives: ShuffleBeehives
    shuffle_wonderitems: ShuffleWonderitems
    shuffle_kokiri_sword: ShuffleSword
    shuffle_ocarinas: ShuffleOcarinas
    shuffle_gerudo_card: ShuffleCard
    shuffle_beans: ShuffleBeans
    shuffle_medigoron_carpet_salesman: ShuffleMedigoronCarpet
    shuffle_frog_song_rupees: ShuffleFrogRupees
    shuffle_100_skulltula_rupee: Shuffle100SkulltulaRupee
    shuffle_silver_rupees: ShuffleSilverRupees
    shuffle_tcgkeys: ShuffleTCGKeys
    shuffle_individual_ocarina_notes: ShuffleIndividualOcarinaNotes
    tcg_requires_lens: TCGRequiresLens
    shuffle_loach_reward: ShuffleLoachReward
    shuffle_hideout_entrances: ShuffleHideoutEntrances
    shuffle_gerudo_fortress_heart_piece: ShuffleGerudoFortressHeartPiece
    shuffle_gerudo_valley_river_exit: ShuffleGerudoValleyRiverExit
    key_rings_give_bosskeys: KeyRingsGiveBossKeys
    no_escape_sequence: SkipEscape
    no_guard_stealth: SkipStealth
    no_epona_race: SkipEponaRace
    skip_some_minigame_phases: SkipMinigamePhases
    complete_mask_quest: CompleteMaskQuest
    useful_cutscenes: UsefulCutscenes
    fast_chests: FastChests
    scarecrow_behavior: ScarecrowBehavior
    fast_bunny_hood: FastBunny
    plant_beans: PlantBeans
    easier_fire_arrow_entry: EasierFireArrowEntry
    chicken_count: ChickenCount
    big_poe_count: BigPoeCount
    fae_torch_count: FAETorchCount
    fast_shadow_boat: FastShadowBoat
    skip_reward_from_rauru: SkipRewardFromRauru
    correct_chest_appearances: CorrectChestAppearance
    minor_items_as_major_chest: MinorInMajor
    invisible_chests: InvisibleChests
    correct_potcrate_appearances: CorrectPotCrateAppearance
    key_appearance_matches_dungeon: KeyAppearanceMatchesDungeon
    ruto_already_at_f1: RutoAlreadyAtF1
    maintain_mask_equips: MaintainMaskEquips
    hints: Hints
    misc_hints: MiscHints
    hint_dist: HintDistribution
    text_shuffle: TextShuffle
    damage_multiplier: DamageMultiplier
    deadly_bonks: DeadlyBonks
    no_collectible_hearts: HeroMode
    starting_tod: StartingToD
    blue_fire_arrows: BlueFireArrows
    fix_broken_drops: FixBrokenDrops
    start_with_consumables: ConsumableStart
    start_with_rupees: RupeeStart
    item_pool_value: ItemPoolValue
    junk_ice_traps: IceTraps
    custom_ice_trap_percent: CustomIceTrapPercent
    custom_ice_trap_count: CustomIceTrapCount
    ice_trap_appearance: IceTrapVisual
    add_random_starting_items: AddRandomStartingItems
    random_starting_items_count: RandomStartingItemsCount
    random_starting_items_exclude: RandomStartingItemsExclude
    adult_trade_shuffle: AdultTradeShuffleOption
    adult_trade_start: AdultTradeStart
    default_targeting: Targeting
    display_dpad: DisplayDpad
    dpad_dungeon_menu: DpadDungeonMenu
    speedup_music_for_last_triforce_piece: SpeedupMusicForLastTriforcePiece
    slowdown_music_when_lowhp: SlowdownMusicWhenLowhp
    uninvert_y_axis_in_first_person_camera: UninvertYAxisInFirstPersonCamera
    input_viewer: InputViewer
    disable_battle_music: DisableBattleMusic
    display_custom_song_names: DisplayCustomSongNames
    credits_music: CreditsMusic
    correct_model_colors: CorrectColors
    background_music: BackgroundMusic
    fanfares: Fanfares
    ocarina_fanfares: OcarinaFanfares
    kokiri_color: kokiri_color
    goron_color:  goron_color
    zora_color:   zora_color
    silver_gauntlets_color:   silver_gauntlets_color
    golden_gauntlets_color:   golden_gauntlets_color
    mirror_shield_frame_color: mirror_shield_frame_color
    navi_color_default_inner: navi_color_default_inner
    navi_color_default_outer: navi_color_default_outer
    navi_color_enemy_inner:   navi_color_enemy_inner
    navi_color_enemy_outer:   navi_color_enemy_outer
    navi_color_npc_inner:     navi_color_npc_inner
    navi_color_npc_outer:     navi_color_npc_outer
    navi_color_prop_inner:    navi_color_prop_inner
    navi_color_prop_outer:    navi_color_prop_outer
    sword_trail_duration: SwordTrailDuration
    sword_trail_color_inner: sword_trail_color_inner
    sword_trail_color_outer: sword_trail_color_outer
    bombchu_trail_color_inner: bombchu_trail_color_inner
    bombchu_trail_color_outer: bombchu_trail_color_outer
    boomerang_trail_color_inner: boomerang_trail_color_inner
    boomerang_trail_color_outer: boomerang_trail_color_outer
    heart_color:          heart_color
    magic_color:          magic_color
    a_button_color:       a_button_color
    b_button_color:       b_button_color
    c_button_color:       c_button_color
    start_button_color:   start_button_color
    sfx_navi_overworld:   sfx_navi_overworld
    sfx_navi_enemy:       sfx_navi_enemy
    sfx_low_hp:           sfx_low_hp
    sfx_menu_cursor:      sfx_menu_cursor
    sfx_menu_select:      sfx_menu_select
    sfx_nightfall:        sfx_nightfall
    sfx_horse_neigh:      sfx_horse_neigh
    sfx_hover_boots:      sfx_hover_boots
    sfx_iron_boots:       sfx_iron_boots
    sfx_silver_rupee:     sfx_silver_rupee
    sfx_boomerang_throw:  sfx_boomerang_throw
    sfx_hookshot_chain:   sfx_hookshot_chain
    sfx_arrow_shot:       sfx_arrow_shot
    sfx_slingshot_shot:   sfx_slingshot_shot
    sfx_magic_arrow_shot: sfx_magic_arrow_shot
    sfx_bombchu_move:     sfx_bombchu_move
    sfx_get_small_item:   sfx_get_small_item
    sfx_explosion:        sfx_explosion
    sfx_daybreak:         sfx_daybreak
    sfx_cucco:            sfx_cucco
    sfx_ocarina:          SfxOcarina


oot_option_groups: typing.List[OptionGroup] = [
    OptionGroup("Open", [option for option in open_options.values()]),
    OptionGroup("World", [*[option for option in world_options.values()],
                *[option for option in bridge_options.values()]]),
    OptionGroup("Shuffle", [option for option in shuffle_options.values()]),
    OptionGroup("Dungeon Items", [option for option in dungeon_items_options.values()]),
    OptionGroup("Timesavers", [option for option in timesavers_options.values()]),
    OptionGroup("Misc", [option for option in misc_options.values()]),
    OptionGroup("Item Pool", [option for option in itempool_options.values()]),
    OptionGroup("Cosmetics", [option for option in cosmetic_options.values()]),
    OptionGroup("SFX", [option for option in sfx_options.values()])
]
