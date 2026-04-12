from dataclasses import dataclass
from BaseClasses import MultiWorld
from Options import (OptionGroup, Toggle, Choice, Range, FreeText, ItemsAccessibility, StartInventoryPool,
                     PerGameCommonOptions)


class OpenedNO4NO3(Choice):
    """Determines the behavior for the back door from Entrance to Underground Cavern
    closed: The door will be closed as in vanilla
    open: The door will be open after reaching Alchemy Laboratory, ensuring the Death cutscene
    open_early: The door will be open from the start, allowing you to break the Death cutscene"""
    display_name = "Opened NO4 Backdoor"
    option_closed = 0
    option_open = 1
    option_open_early = 2
    default = 0


class OpenedDAIARE(Toggle):
    """
        If true, the back door from Chapel to Colosseum will be open
    """
    display_name = "Opened ARE Backdoor"


class Extension(Choice):
    """relic_prog: Only relics, silver/gold rings, spike breaker and holy glasses locations are checks
    guarded: All of the above, plus most items guarded by bosses
    equipment: All of the above, plus most floor equipment
    full: Every location on the map is added to the pool"""
    display_name = "Item pool"
    option_relic_prog = 0
    option_guarded = 1
    option_equipment = 2
    option_full = 3
    default = 3


class InfiniteWing(Toggle):
    """
        Makes wing smash continue until you hit a wall or run out of MP (cancellable by exiting bat form)
    """
    display_name = "Infinite wing smash"


class RandomizeNonLocations(Toggle):
    """
        Will randomize items not chosen from the item_pool setting
    """
    display_name = "Randomize extra items"


class ExtraPool(Toggle):
    """
        Try to add powerful items to the pool: Duplicator, Crissaegrim, Ring of varda, Mablung sword, Masamune, Marsil, Yasutsuna
    """
    display_name = "Powerful items"


class BossLocations(Toggle):
    """Boss drops would be part of the seed pool."""
    display_name = "Make boss drops part of the pool"


class Enemysanity(Toggle):
    """Hitting an enemy becomes a check. Extra locations will be added based on difficult
    easy: Duplicate relics and progression items adds 50 extra vessels and random equipments
    normal: Duplicate progression items adds 35 extra vessels and random equipments
    hard: 15 extra vessels and random equipments"""
    display_name = "Enemysanity"


class EnemyScroll(Toggle):
    """Enemysanity require Faerie Scroll"""
    display_name = "Enemysanity require Spirit Orb"


class Difficult(Choice):
    """easy: 50% less monster HP, attack and defense and drop chance increased
    normal: All vanilla stats
    hard: 50% more monster HP, attack and defense
    very_hard: 100% more monster HP, attack, and defense"""
    display_name = "Difficult"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_very_hard = 3
    default = 1


class EnemyModifier(Range):
    """Modifier for monster HP, attack and defense, override difficult preset
    Any number above 100 increase the attribute and bellow decrease. 24 means OFF"""
    display_name = "Enemy modifier"
    range_start = 24
    range_end = 200
    default = 24


class DropModifier(Choice):
    """Modifier for monster drop. Override difficult preset
    normal: Drop chance is not modified
    increase: increase the odds of a drop
    abundant: increase further odds of a drop
    guaranteed: guarantees drops for every enemy that has one. Ring of arcana makes them drop their rare item instead"""
    display_name = "Drop modifier"
    option_normal = 0
    option_increased = 1
    option_abundant = 2
    option_guaranteed = 3
    default = 0


class RandomStartGear(Toggle):
    """Randomize starting equipment"""
    display_name = "Randomize starting equipment"


class DeathLink(Toggle):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    display_name = "Death link"


class RemovePrologue(Toggle):
    """Remove prologue fight"""
    display_name = "No prologue"


class MapColor(Choice):
    """Change map colors"""
    display_name = "Map colors"
    option_default = 0
    option_dark_blue = 1
    option_crimson = 2
    option_brown = 3
    option_dark_green = 4
    option_gray = 5
    option_purple = 6
    option_pink = 7
    option_black = 8
    option_invisible = 9
    default = 0


class AlucardPalette(Choice):
    """Change Alucard palette colors"""
    display_name = "Alucard palette"
    option_default = 0
    option_bloody_tears = 1
    option_blue_danube = 2
    option_swamp_thing = 3
    option_white_knight = 4
    option_royal_purple = 5
    option_pink_passion = 6
    option_shadow_prince = 7
    default = 0


class AlucardLiner(Choice):
    """Change Alucard liner colors"""
    display_name = "Alucard liner"
    option_gold_trim = 0
    option_bronze_trim = 1
    option_silver_trim = 2
    option_onyx_trim = 3
    option_coral_trim = 4
    default = 0


class MagicVessels(Toggle):
    """Replace heart max up with magic max up"""
    display_name = "Magic vessels"


class AntiFreeze(Toggle):
    """Remove screen freezes on level-up, relic and vessels acquisition"""
    display_name = "Anti freeze"


class MyPurse(Toggle):
    """Prevent Death from stealing your gear"""
    display_name = "That's my purse"


class FastWarp(Toggle):
    """Quickens warp animation when using teleporters"""
    display_name = "Fast warp"


class UnlockedMode(Toggle):
    """Opens all five shorcuts in first castle and one in second castle
    Might break logic"""
    display_name = "Unlocked mode"


class RelicSurprise(Toggle):
    """All relics are hidden behind the same sprite and palette.
    The player cannot tell what the relic is until the collect it"""
    display_name = "Relic surprise!"


class EnemyStats(Toggle):
    """Enemy stats are randomized ranging from 25% to 200% of their original value and their attack and defense types
    are randomized to include random elements. Modification options WILL OVERRIDE THIS OPTION"""
    display_name = "Enemy stats"


class RandomShopStock(Choice):
    """Randomize items sold by Librarian
    on: Any item can appear at shop
    on_lib: Any item can appear at shop and enforcing a Library card on sale
    on_no_prog: Any item can appear at shop and no progression item will appear
    on_no_prog_lib: No progression item can appear at shop enforcing a Library card on sale"""
    display_name = "Randomize shop stock"
    option_off = 0
    option_on = 1
    option_on_lib = 2
    option_on_no_prog = 3
    option_on_no_prog_lib = 4
    default = 0


class ShopPrices(Toggle):
    """Randomize shop prices between 50% to 150%. OVERRIDE difficult preset"""
    display_name = "Shop prices"


class StartingZone(Choice):
    """Start in the entrance as usual but after the first Warg, you are teleported to a random zone to start the
    rest of your run. (Could break logic)
    vanilla: Normal entrance
    normal_castle: Your random room will be on the first castle
    reverse_castle: Your random room will be on the reverse castle
    any_castle: Your random room could be anywhere"""
    option_vanilla = 0
    option_normal_castle = 1
    option_reverse_castle = 2
    option_any_castle = 3
    default = 0
    display_name = "Starting zone"


class ReverseLibraryCard(Toggle):
    """Adds a new function to library cards. Hold down while using them to take Alucard to the second castle library
    after Richter is saved"""
    display_name = "Reverse library card"


class RandomizeMusic(Toggle):
    """Randomize the game music"""
    display_name = "Randomize music"


class SkipClockTowerPuzzle(Toggle):
    """Disable rotating gears clock tower puzzle. Hitting any gear once opens the secret door"""
    display_name = "Clock tower puzzle"


class NoLogic(Toggle):
    """There is logic. Seed might be unbeatable. Heavy on glitch knowledge"""
    display_name = "No logic rules"


class AutoHeal(Toggle):
    """
        Entering a save room heal Alucard
    """
    display_name = "Heal when enter a save room"


class ColorRandomizer(Toggle):
    """Randomize various color paletter. Ex: Cape colors, gravity boots trail, hydrostorm"""
    display_name = "Color randomizer"


class RandomizeDrop(Choice):
    """Randomize enemy drops
    simple: Only randomize between each enemy drop
    simple_global: Only randomize between each enemy drop including global drops"""
    option_off = 0
    option_simple = 1
    option_simple_global = 2
    default = 0
    display_name = "Randomize enemy drops"


@dataclass
class SOTNOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    start_inventory: StartInventoryPool
    open_no4: OpenedNO4NO3
    open_are: OpenedDAIARE
    item_pool: Extension
    infinite_wing_smash: InfiniteWing
    randomize_items: RandomizeNonLocations
    powerful_items: ExtraPool
    boss_locations: BossLocations
    enemysanity: Enemysanity
    enemy_scroll: EnemyScroll
    difficult: Difficult
    enemy_mod: EnemyModifier
    drop_mod: DropModifier
    rng_start_gear: RandomStartGear
    death_link: DeathLink
    remove_prologue: RemovePrologue
    map_color: MapColor
    alucard_palette: AlucardPalette
    alucard_liner: AlucardLiner
    magic_vessels: MagicVessels
    anti_freeze: AntiFreeze
    my_purse: MyPurse
    fast_warp: FastWarp
    unlocked_mode: UnlockedMode
    relic_suprise: RelicSurprise
    enemy_stats: EnemyStats
    random_shop: RandomShopStock
    shop_prices: ShopPrices
    starting_zone: StartingZone
    reverse_library: ReverseLibraryCard
    random_music: RandomizeMusic
    skip_nz1: SkipClockTowerPuzzle
    no_logic: NoLogic
    auto_heal: AutoHeal
    color_randomizer: ColorRandomizer
    randomize_drop: RandomizeDrop


sotn_option_groups = [
    OptionGroup("Item Pool", [
        Extension, Enemysanity, ExtraPool, BossLocations,
    ]),
    OptionGroup("Gameplay Tweaks", [
        OpenedNO4NO3, OpenedDAIARE,  RandomizeNonLocations, EnemyScroll, Difficult, EnemyModifier, DropModifier,
        RandomizeDrop, RandomStartGear, DeathLink, RandomShopStock, UnlockedMode, RelicSurprise, EnemyStats, ShopPrices,
        StartingZone, ReverseLibraryCard, NoLogic
    ]),
    OptionGroup("QOL", [
        InfiniteWing,  RemovePrologue,  MagicVessels, AntiFreeze, MyPurse, FastWarp, SkipClockTowerPuzzle, AutoHeal
    ]),
    OptionGroup("Cosmetics", [
        MapColor, AlucardPalette, AlucardLiner, RandomizeMusic, ColorRandomizer
    ])
]




