from dataclasses import dataclass
from enum import Enum

from Options import Choice, FreeText, OptionDict, OptionGroup, PerGameCommonOptions, Range, TextChoice, Toggle, Visibility


class WorldMode(Choice):
    """Open: Start from Link's House or Sanctuary, without needing to save Zelda in Hyrule Castle
    Standard: Start at Link's House and save Zelda in Hyrule Castle before accessing the rest of the world
    Inverted: The Light World and Dark World have been flipped.
        - Link spawns at the Bomb Shop and Dark Sanctuary
        - All Dark World portals now take you to the Light World
        - Link is a bunny in the Light World unless you have the Moon Pearl
        - Agahnim's Tower and Ganon's Tower have swapped places. Agahnim's Tower now requires crystals to enter
        - Ganon is hiding in a new hole on top of Hyrule Castle
        - The Magic Mirror takes you from the Light World to the Dark World
        - The Flute is always pre-activated and will take you to locations across the Dark World, including the top of Death Mountain
        - Light World terrain has been modified so that mirror-locked locations can be reached without the mirror
        - The top of Turtle Rock can be accessed by jumping from its tail"""
    display_name = "World Mode"
    option_open = 0
    option_standard = 1
    option_inverted = 2
    # option_retro = "retro"
    default = "open"


class Goal(Choice):
    """Sets the goal for this seed.

    crystals: Collect the required number of crystals and kill Ganon.
    ganon: Collect the required number of crystals, kill Agahnim on top of Ganon's Tower, then kill Ganon.
    dungeons: Obtain all pendants and crystals, defeat both Agahnims, then kill Ganon.
    pedestal: Collect all 3 pendants and pull the Master Sword from its pedestal.
    triforcehunt: Collect the required number of pieces of the Triforce, then talk to Murahdahla outside Hyrule Castle.
    ganonhunt: Collect the required number of pieces of the Triforce, then kill Ganon.
    trinity: Either kill Ganon, pull the pedestal, or collect the required number of Triforce pieces and talk to Murahdahla outside Hyrule Castle.
    completionist: Collect every check in the game, then kill Ganon."""
    display_name = "Goal"
    option_crystals = 0
    option_ganon = 1
    option_dungeons = 2
    option_pedestal = 3
    option_triforcehunt = 4
    option_ganonhunt = 5
    option_trinity = 6
    option_completionist = 7
    default = "crystals"


class OpenPyramid(Choice):
    """ Whether the Pyramid hole leading to Ganon should be open at the start. Choosing "auto" will open or close it based on your goal setting;
    it will be open for crystals, trinity, and ganonhunt, and closed for other goals, or if crossed entrance is enabled regardless of the goal."""
    display_name = "Open Pyramid"
    option_auto = 0
    option_open = 1
    option_closed = 2
    default = "auto"

def open_pyramid_string_from_option(option):
    # OWR uses "yes" and "no", but "open" and "closed" is what people are used to from the core AP implementation
    if option == "auto":
        return "auto"
    elif option == "open":
        return "yes"
    elif option == "closed":
        return "no"
    else:
        raise Exception(f"Invalid option {option} for OpenPyramid")


class CrystalsNeededForGanonsTower(Range):
    """How many crystals are needed to enter Ganon's Tower"""
    display_name = "Crystals Needed for Ganon's Tower"
    range_start = 0
    range_end = 7
    default = 7


class CrystalsNeededForGanon(Range):
    """How many crystals are needed before Ganon can be killed"""
    display_name = "Crystals Needed for Ganon"
    range_start = 0
    range_end = 7
    default = 7


class TriforceHuntGoal(Range):
    """How many Triforce Pieces are required to beat the game when the goal is set to Triforce Hunt or Ganon Hunt"""
    display_name = "Triforce Hunt Goal"
    range_start = 1
    range_end = 850
    default = 20


class TriforceHuntTotal(Range):
    """How many Triforce Pieces are in the item pool when the goal is set to Triforce Hunt or Ganon Hunt"""
    display_name = "Triforce Hunt Total"
    range_start = 1
    range_end = 850
    default = 30


class MapShuffle(Toggle):
    """Maps can now appear outside of their dungeon. The map screen will not show if a dungeon gives a pendant or crystal until its map has been found."""
    display_name = "Map Shuffle"


class CompassShuffle(Toggle):
    """Compasses can now appear outside of their dungeon."""
    display_name = "Compass Shuffle"


class SmallKeyShuffle(Toggle):
    """Small keys can now appear outside of their dungeon."""
    display_name = "Small Key Shuffle"


class BigKeyShuffle(Toggle):
    """Big keys can now appear outside of their dungeon."""
    display_name = "Big Key Shuffle"


class KeyDropShuffle(Toggle):
    """Shuffle keys that are dropped by enemies or hidden under pots, regardless of potsanity or enemy drop settings."""
    display_name = "Key Drop Shuffle"
    default = False
    visibility = Visibility.none


class EntranceShuffle(Choice):
    """Randomize where each building, cave, and dungeon entrance leads to.
    vanilla: No entrance shuffle.
    dungeonssimple: Dungeon entrances are shuffled amongst each other. The four entrances of Hyrule Castle, Desert Palace, and Turtle Rock remain grouped together.
    dungeonsfull: Dungeon entrances are shuffled amongst each other. Dungeons with multiple entrances can be split apart, but they will either all be in the light world or all in the dark world.
    crossed: All buildings, caves, and dungeon entrances are randomized. Caves and dungeons with multiple entrances can connect the Light and Dark Worlds."""
    display_name = "Entrance Shuffle"
    option_vanilla = 0
    option_dungeonssimple = 1
    option_dungeonsfull = 2
    option_crossed = 3
    default = "vanilla"


class ShuffleLinksHouse(Toggle):
    """Adds Link's House to the entrance pool for crossed entrance shuffle."""
    display_name = "Shuffle Links House"
    default = False


class ShuffleTavern(Toggle):
    """Adds the back of Kakariko Tavern to the entrance pool for crossed entrance shuffle."""
    display_name = "Shuffle Tavern"
    default = False


class Zelgawoods(Toggle):
    """If entrance shuffle is enabled, add Skull Woods entrances and dropdowns to the entrance shuffle. The main Skull Woods entrance/big chest
    dropdown and the second Skull Woods entrance/the dropdown in the back are both added to the dropdown pool. The other two dropdowns in the
    front are vanilla, and at least one of the entrances in the back of the Skull Woods area must be a connector."""
    # TODO: If I have a good link to the image description a picture is better than text descriptions
    display_name = "Zelgawoods"


class DoorShuffle(Choice):
    """Randomize the layout of each dungeon. Rooms are rearranged or appear in other dungeons, and doors are randomized.

    * Dungeons always have their original boss room, which drops that dungeon's prize.
    * Dropdowns are vanilla, and rooms connected by a dropdown are always in the same dungeon.
    * Dungeons may have different key counts. Agahnims Tower could have a Big Key, and other dungeons may not have a Big Key.
    * Killing Blind requires bombing the cracked floor in the attic, which may be in a different dungeon.
    * Bringing the Maiden to the Thieves Town boss room will tell you which dungeon has the attic.
    * Locations will have the name of their original dungeon, not the dungeon they appear in.
    * Dungeon counters, mirror scroll, and key drop shuffle are enabled regardless of YAML settings. Small keys are shuffled if the door shuffle is partitioned or crossed.

    vanilla: Dungeons have their vanilla layout
    basic: Dungeon layouts are shuffled, but each room stays in its own dungeon
    partitioned: Dungeon layouts are shuffled, with rooms from different dungeons being mixed together. Rooms in light world dungeons including Hyrule
        Castle and Agahnims Tower are shuffled together, early dark world dungeons (Palace of Darkness to Thieves Town) are shuffled together, and
        Mitts-locked dungeons (Ice Palace to Ganons Tower) are shuffled together.
    crossed: Rooms from all dungeons are shuffled together."""
    display_name = "Door Shuffle"
    option_vanilla = 0
    option_basic = 1
    option_partitioned = 2
    option_crossed = 3
    default = "vanilla"


class LobbyShuffle(Toggle):
    """With door shuffle enabled, randomize the first room in each dungeon."""
    display_name = "Lobby Shuffle"
    default = False


class DoorTypeShuffle(Choice):
    """With door shuffle enabled, randomize the types of each door.
    original: All dungeon doors which are open, bombable, bonkable, or small key locked become a random type of door.
    big: Doors that are big key locked are also randomized."""
    display_name = "Door Type Shuffle"
    option_original = 0
    option_big = 1
    default = "original"


class EnemyShuffle(Choice):
    """All enemies except bosses are randomized. Logical enemy shuffle might require defeating enemies that
    require specific items (Eyegore, Freezors, etc.) to progress in a dungeon."""
    display_name = "Enemy Shuffle"
    option_vanilla = 0
    option_shuffled = 1
    option_logical = 2
    default = "vanilla"

def enemy_shuffle_string_from_option(option):
    if option == "vanilla":
        return "none"
    elif option == "shuffled" or option == "logical":
        return "shuffled"
    else:
        raise Exception(f"Invalid option {option} for enemy_shuffle")


class BossShuffle(Choice):
    """Bosses are randomized. This includes the Armos/Lanmolas/Moldorm rematches in Ganon's Tower, but not Ganon or either Aganhim fight. Some bosses cannot appear in some locations.

    * Vanilla: Bosses are in their original locations.
    * Simple: Bosses are shuffled randomly. Armos Knights, Lanmolas, and Moldorm will be fought twice.
    * Full: Bosses are shuffled randomly, and three random bosses will be fought twice.
    * Chaos: Bosses are shuffled randomly, and any boss can be fought any number of times."""
    display_name = "Boss Shuffle"
    option_vanilla = 0
    option_simple = 1
    option_full = 2
    option_chaos = 3
    default = "vanilla"

def boss_shuffle_string_from_option(option):
    if option == "vanilla":
        return "none"
    elif option == "simple":
        return "simple"
    elif option == "full":
        return "full"
    elif option == "chaos":
        return "random"
    else:
        raise Exception(f"Invalid option {option} for boss_shuffle")


class BomblessStart(Toggle):
    """Start without the ability to use bombs. Two bomb capacity upgrades are added to the item pool and will give the ability to use bombs."""
    display_name = "Bombless Start"
    default = False


class Shopsanity(Toggle):
    """All shops contain randomized items, including Potion Shop and Capacity Upgrade Fairy. Adds 32 items to the item pool.
    Each type of potion can be purchased at a random shop."""
    display_name = "Shopsanity"
    default = False


class PrizeShuffle(Toggle):
    """Adds Pendants and Crystals to the itempool."""
    display_name = "Prize Shuffle"
    default = False


class Potsanity(Choice):
    """Pots contain randomized items. Any pots that haven't been checked will have their color changed, and dungeon counters
    are forced on with dungeon or lottery settings. A max of 256 multiworld items can be under pots.
    - None - No pots are in the pool, like normal randomizer
    - Key Pots - The pots that have keys are in the pool
    - Cave Pots - The pots that are not found in dungeons are in the pool (includes Spike Cave large block)
    - Cave + Keys Pots - Both non-dungeon pots and pots that used to have keys
    - Dungeon Pots - The pots that are in dungeons
    - Lottery - All pots and large blocks are in the pool"""
    display_name = "Pot Shuffle"
    option_none = 0
    option_keys = 1
    option_cave = 2
    option_cavekeys = 3
    option_dungeon = 4
    option_lottery = 5
    default = "none"


class EnemyDropShuffle(Choice):
    """Enemies drop randomized items. With all underworld (caves + dungeons) enemies randomized, a blue square will be shown
    in the top-left corner if there is a undefeated enemy in the same supertile (usually in the current or adjacent room), and
    dungeon counters are forced on. A starting sword is recommended for underworld enemy drop shuffle."""
    display_name = "Enemy Drop Shuffle"
    option_none = 0
    option_keys = 1
    option_underworld = 2
    default = "none"


class LocalFillPercent(Range):
    """Force a percentage of extra filler items from pot and enemy drop shuffle into your own world."""
    display_name = "Local Fill Percent"
    range_start = 0
    range_end = 100
    default = 0


class FluteShuffle(Choice):
    """Randomize the Flute spot destinations. Balanced will spread the Flute spots around the overworld, while Chaos will place them randomly."""
    display_name = "Flute Shuffle"
    option_vanilla = 0
    option_balanced = 1
    option_chaos = 2
    default = "vanilla"

def flute_shuffle_string_from_option(option):
    if option == "vanilla":
        return "vanilla"
    elif option == "balanced":
        return "balanced"
    elif option == "chaos":
        return "random"
    else:
        raise Exception(f"Invalid option {option} for flute_shuffle")


class Pseudoboots(Toggle):
    """Psuedoboots give Link the ability to dash like Pegasus Boots, but they cannot bonk rocks, open King's Tomb, knock items off torches/the Library, or clear small gaps"""
    display_name = "Pseudoboots"
    default = False


class MirrorScroll(Toggle):
    """Mirror Scroll is an inventory item that warps Link to the start of their current dungeon, and is replaced upon finding the Magic Mirror."""
    display_name = "Mirror Scroll"
    default = False


class PreActivatedFlute(Toggle):
    """The Flute does not need to be activated at the village statue after finding it."""
    display_name = "Pre Activated Flute"
    default = False


class DungeonCounters(Choice):
    """Displays two counters in each dungeon showing the collected/total number of checks and number of small keys.
    If pickup is selected, the counters will be displayed after finding that dungeon's map and compass. The counters
    are always displayed if door shuffle is enabled."""
    display_name = "Dungeon Counters"
    option_on = 0
    option_pickup = 1
    option_off = 2
    default = "pickup"


class TrapAppearance(Choice):
    """How Trap items will appear in-game."""
    display_name = "Trap Appearance"
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2
    default = "major_only"


class Sprite(FreeText):
    """A custom sprite to use for Link. Must be 'Link' or the exact name of a sprite listed at https://alttpr.com/en/sprite_preview.
    If an error occurs when loading the sprite, the default Link sprite will be used."""
    display_name = "Sprite"
    default = "Link"


class HeartBeepRate(Choice):
    """The rate at which heart beeps are played when Link is at low health."""
    display_name = "Heart Beep Rate"
    option_double = 0
    option_normal = 1
    option_half = 2
    option_quarter = 3
    option_never = 4
    default = "normal"

def heart_beep_rate_string_from_option(option):
    if option == "double":
        return "double"
    elif option == "normal":
        return "normal"
    elif option == "half":
        return "half"
    elif option == "quarter":
        return "quarter"
    elif option == "never":
        return "off"
    else:
        raise Exception(f"Invalid option {option} for heart_beep_rate")


class HeartColor(Choice):
    """The color of Link's heart meter."""
    display_name = "Heart Color"
    option_red = 0
    option_blue = 1
    option_green = 2
    option_yellow = 3
    default = "red"


class FastMenu(Choice):
    """The rate at which the menu opens and closes."""
    display_name = "Fast Menu"
    option_normal = 0
    option_instant = 1
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_half = 5
    default = "normal"


# class OWPalettes(TextChoice):
#     """The palette of the overworld sprites."""
#     display_name = "Overworld Palettes"
#     option_default = "default"
#     option_randomized = "randomized"
#     option_blackout = "blackout"
#     default = "default"


# class UWPalettes(TextChoice):
#     """The palette of the underworld sprites."""
#     display_name = "Underworld Palettes"
#     option_default = "default"
#     option_randomized = "randomized"
#     option_blackout = "blackout"
#     default = "default"


class DisableMusic(Toggle):
    """Disables game music."""
    display_name = "Disable Music"
    default = False


# class ShuffleSFX(Toggle):
#     """Shuffles the soundtrack."""
#     display_name = "Shuffle SFX"
#     default = False


# class ShuffleSFXInstruments(Toggle):
#     """Shuffles the soundtrack instruments."""
#     display_name = "Shuffle SFX Instruments"
#     default = False


# class ShuffleSongInstruments(Toggle):
#     """Shuffles the soundtrack instruments on a per-song basis, so each song will have its own shuffled set of instruments."""
#     display_name = "Shuffle Song Instruments"
#     default = False


class MSUResume(Toggle):
    """While using an MSU, when entering and leaving a building/cave/dungeon, the overworld music will pick up where it left off, instead of restarting every time."""
    display_name = "MSU Resume"
    default = False


class TestSlotData(OptionDict):
    """Optional slot data, used for unit testing ONLY"""
    visibility = Visibility.none
    default = {}


@dataclass
class ALttPROptions(PerGameCommonOptions):
    world_mode: WorldMode
    goal: Goal
    open_pyramid: OpenPyramid
    crystals_needed_for_ganons_tower: CrystalsNeededForGanonsTower
    crystals_needed_for_ganon: CrystalsNeededForGanon
    triforce_hunt_goal: TriforceHuntGoal
    triforce_hunt_total: TriforceHuntTotal
    map_shuffle: MapShuffle
    compass_shuffle: CompassShuffle
    small_key_shuffle: SmallKeyShuffle
    big_key_shuffle: BigKeyShuffle
    key_drop_shuffle: KeyDropShuffle
    entrance_shuffle: EntranceShuffle
    shuffle_links_house: ShuffleLinksHouse
    shuffle_tavern: ShuffleTavern
    zelgawoods: Zelgawoods
    door_shuffle: DoorShuffle
    lobby_shuffle: LobbyShuffle
    door_type_shuffle: DoorTypeShuffle
    enemy_shuffle: EnemyShuffle
    boss_shuffle: BossShuffle
    bombless_start: BomblessStart
    shopsanity: Shopsanity
    prize_shuffle: PrizeShuffle
    flute_shuffle: FluteShuffle
    potsanity: Potsanity
    enemy_drop_shuffle: EnemyDropShuffle
    local_fill_percent: LocalFillPercent
    pre_activated_flute: PreActivatedFlute
    pseudoboots: Pseudoboots
    mirror_scroll: MirrorScroll
    dungeon_counters: DungeonCounters
    trap_appearance: TrapAppearance
    sprite: Sprite
    heart_beep_rate: HeartBeepRate
    heart_color: HeartColor
    fast_menu: FastMenu
    # ow_palettes: OWPalettes
    # uw_palettes: UWPalettes
    disable_music: DisableMusic
    # shuffle_sfx: ShuffleSFX
    # shuffle_sfxinstruments: ShuffleSFXInstruments
    # shuffle_songinstruments: ShuffleSongInstruments
    msu_resume: MSUResume
    test_slot_data: TestSlotData


alttpr_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Victory Conditions",
        [
            Goal,
            OpenPyramid,
            CrystalsNeededForGanon,
            CrystalsNeededForGanonsTower,
            TriforceHuntGoal,
            TriforceHuntTotal,
        ],
    ),
    OptionGroup(
        "Item Pool",
        [
            MapShuffle,
            CompassShuffle,
            SmallKeyShuffle,
            BigKeyShuffle,
            KeyDropShuffle,
            BomblessStart,
            PrizeShuffle,
            Shopsanity,
            Potsanity,
            EnemyDropShuffle,
            LocalFillPercent,
        ],
    ),
    OptionGroup(
        "World Settings",
        [
            WorldMode,
            FluteShuffle,
            EnemyShuffle,
            BossShuffle,
        ],
    ),
    OptionGroup(
      "Entrance Shuffle",
      [
          EntranceShuffle,
          Zelgawoods,
          ShuffleLinksHouse,
          ShuffleTavern,
      ]
    ),
    OptionGroup(
        "Door Shuffle",
        [
            DoorShuffle,
            DoorTypeShuffle,
            LobbyShuffle,
        ],
    ),
    OptionGroup(
        "Quality of Life",
        [
            Pseudoboots,
            MirrorScroll,
            PreActivatedFlute,
            DungeonCounters,
            TrapAppearance,
            Sprite,
            HeartBeepRate,
            HeartColor,
            FastMenu,
            DisableMusic,
            MSUResume,
        ],
    ),
]