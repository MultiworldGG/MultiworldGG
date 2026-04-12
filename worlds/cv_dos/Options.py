from dataclasses import dataclass
from Options import (Toggle, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, DefaultOnToggle, Choice, TextChoice, OptionSet, DeathLink, NamedRange)
from .Items import soul_filler_table


class Goal(Choice):
    """The goal for your game.
       Throne Room: Get to the Throne Room and defeat Menace there.
       Abyss: Open the path to the Mine of Judgment, then defeat Menace in the Abyss."""
    display_name = "Goal"
    option_throne_room = 0
    option_abyss = 1
    default = 0

class ReplaceMenaceWithSoma(Toggle):
    """Replaces Menace with Soma-Dracula"""
    display_name = "Soma Replaces Menace"

class RemoveMoneyGates(DefaultOnToggle):
    """Removes the gates that require you to own a specific amount of money."""
    display_name = "Remove Money Gates"

class DisableBossSeals(Toggle):
    """Removes the requirement to draw Magic Seals to defeat bosses."""
    display_name = "No Drawing Seals"

class EarlySeal1(Toggle):
    """Places Magic Seal 1 early in your own game to prevent getting stuck early."""
    display_name = "Early Seal 1"

class RevealMap(DefaultOnToggle):
    """Start with the entire map visible."""
    display_name = "Reveal Map"

class StartingWeapon(TextChoice):
    """The weapon you start the game with.
       Random Base: Start with a random base-level weapon
       Random Any: Start with any random weapon
       You can also choose to start with any specific weapon."""
    option_random_base = 0
    option_random_any = 1
    default = "Knife"
    display_name = "Starting Weapon"

class FixLuck(DefaultOnToggle):
    """Fixes how the Luck stat is applied.
       With the fix applied, each point of luck gives +0.1% to any drop.
       Without the fix, each point of luck is +0.04% for souls, 0.25% for items."""
    display_name = "Fix Luck"

class RevealBreakableWalls(Toggle):
    """Automatically destroys/reveals all breakable walls"""
    display_name = "Reveal Hidden Walls"

class BoostSpeed(Toggle):
    """Increases Soma's base walking speed by 33%"""
    display_name = "Boost Speed"

class OneScreenMode(Toggle):
    """Allows the entire game to be played with only the bottom screen. Press Select to view the map."""
    display_name = "One-Screen Mode"

class SoulRandomizer(Choice):
    """Randomizes Enemy souls.
            Disabled: Enemy souls are unchanged.
            Shuffled: Enemy souls will be shuffled amongst each other. Souls that unlock things are unchanged.
            Soulsanity: Enemy soul drops can be anything, even important items or non-souls. You can change the expected soul rarity with Soulsanity level."""
    option_disabled = 0
    option_shuffled = 1
    option_soulsanity = 2
    default = 0
    display_name = "Soul Randomizer"

class SoulsanityLevel(Choice):
    """The maximum tier of soul rarity that have Locations on them.
       Rare souls always expect you to have the Soul Eater Ring."""
    option_simple = 0
    option_medium = 1
    option_rare = 2
    default = 0
    display_name = "Soulsanity Level"

class GuaranteedSouls(OptionSet):
    """The specified Souls will be guaranteed to have at least one copy in the item pool. Unspecified souls can still be randomly selected from the soul pool.
       You can also use Common, Uncommon, or Rare to add all souls of that rarity."""
    display_name = "Guranteed Souls"
    default = {"Procel Soul", "Mud Demon Soul", "Black Panther Soul"}
    valid_keys = {soul.casefold() for soul in set(soul_filler_table) | {"common", "uncommon", "rare"}}
    valid_keys_casefold = True

class RandomizeStartingWarp(Toggle):
    """Randomizes which Warp Room is unlocked by default."""
    display_name = "Random Starting Warp Room"

class OpenDrawbridge(Toggle):
    """If enabled, the drawbridge in Lost Village will start open instead of closed."""
    display_name = "Open Drawbridge"

class ShopRandomizer(Toggle):
    """Randomizes Hammer's shop items."""
    display_name = "Shop Randomizer"

class ShuffleDrops(Toggle):
    """Randomizes items dropped by enemies"""
    display_name = "Drop Shuffle"

class ExperiencePercent(NamedRange):
    """What percentage of EXP enemies give you. This is a percent of their original EXP amount."""
    display_name = "Experience Percentage"
    range_start = 50
    range_end = 500
    default = 100
    special_range_names = {
        "half": 50,
        "normal": 100,
        "double": 200,
        "quadruple": 400
    }

class SoulDropPercent(NamedRange):
    """Percentage applied to an enemy's base chance of dropping their soul."""
    display_name = "Soul Drop Percentage"
    range_start = 50
    range_end = 500
    default = 100
    special_range_names = {
        "half": 50,
        "normal": 100,
        "double": 200,
        "triple": 300
    }

class AreaMusicShuffle(Toggle):
    """Randomizes area music."""
    display_name = "Area Music Randomizer"

class BossMusicShuffle(Toggle):
    """Randomizes boss music."""
    display_name = "Boss Music Randomizer"

class SoulWallRandomizer(Toggle):
    """Randomizes which souls are needed to break the red Soul Barriers."""
    display_name = "Soul Wall Randomizer"

class RandomizeSynthSouls(Toggle):
    """Randomizes which souls are required for Synthesis crafting."""
    display_name = "Shuffle Synthesis Souls"

class FreeBat(Toggle):
    """Removes Bat Company's MP cost"""
    display_name = "Free Bat"

class PassiveSoulEaterRing(Toggle):
    """If enabled, you will gain the bonus from the Soul Eater Ring without needing to equip it
       as long as you have at least one in your inventory."""
    display_name = "Passive Soul Eater Ring"

class GateItems(Choice):
    """Defines how the 4 metal switch gates act.
       Normal: Normal behavior. Gates can only be opened by pressing the respective button.
       Add Keys: The same as normal behavior, but also adds keys to the item pool that can open the gate from the other side.
       Buttonsanity: Adds keys to each gate, and the corresponding button will grant a check."""
    option_normal = 0
    option_add_keys = 1
    option_buttonsanity = 2
    default = 0
    display_name = "Gate Items"

class HardMode(Toggle):
    """Puts the game in Hard Mode. Enemies are tougher, sometimes have additional properties, but drop rates are increased.
       There are no checks exclusive to Hard Mode."""
    display_name = "Hard Mode"

class BossShuffle(Toggle):
    """Randomizes boss fights."""
    display_name = "Boss Shuffle"

class SealShuffle(Toggle):
    """Randomizes which seal is required for each boss/door.
       Early Seal 1 will guarantee Flying Armor to always use Seal 1."""
    display_name = "Seal Shuffle"

class RandomizeSealPatterns(Toggle):
    """Randomizes the drawn pattern for Magic Seals, as well as their rotation."""
    display_name = "Randomize Seal Patterns"

class MenaceCondition(Choice):
    """This Condition is required to be met before you can fight Menace.
       None: None
       Throne Room: Defeat Aguni in the Throne Room (If Goal is set to throne room, this will be set to None.)
       Garden: Avoid the bad ending in the Garden of Madness
       Bosses: Defeat all available bosses"""
    display_name = "Menace Condition"
    option_none = 0
    option_throne_room = 1
    option_garden = 2
    option_bosses = 3
    default = 0

class MineCondition(Choice):
    """This Condition is required to be met before you can enter the Mine of Judgment.
       None: None
       Throne Room: Defeat Aguni in the Throne Room (If Goal is set to throne room, the mine and the Abyss will be inaccessible.)
       Garden: Avoid the bad ending in the Garden of Madness
       Bosses: Defeat all available bosses"""
    display_name = "Mine Condition"
    option_none = 0
    option_throne_room = 1
    option_garden = 2
    option_bosses = 3
    default = 2

class GardenCondition(Choice):
    """This Condition is required to be met before Celia appears in the Garden of Madness.
       None: None
       Throne Room: Defeat Aguni in the Throne Room (This condition is considered unreachable if Goal is set to throne room)
       Bosses: Defeat all available bosses"""
    display_name = "Garden Condition"
    option_none = 0
    option_throne_room = 1
    option_bosses = 2
    default = 0
    display_name = "Garden Condition"

#class RevealBreakableWalls(Choice):
 #   """Controls how breakable walls act.
  #     Normal: Breakable walls are breakable, you are assumed to already know where they are.
   #    Revealed: All breakable walls are already broken
    #   Eye Spy: Breakable walls are breakable, you require Peeping Eye's soul to break them at all."""
    #display_name = "Breakable Walls"
    #option_normal = 0
    #option_revealed = 1
    #option_eye_spy = 2
    #default = 0

@dataclass
class DoSOptions(PerGameCommonOptions):
    goal: Goal
    replace_menace_with_soma: ReplaceMenaceWithSoma
    remove_money_gates: RemoveMoneyGates
    disable_boss_seals: DisableBossSeals
    early_seal_1: EarlySeal1
    reveal_map: RevealMap
    starting_weapon: StartingWeapon
    reveal_hidden_walls: RevealBreakableWalls
    fix_luck: FixLuck
    boost_speed: BoostSpeed
    one_screen_mode: OneScreenMode
    soul_randomizer: SoulRandomizer
    soulsanity_level: SoulsanityLevel
    guaranteed_souls: GuaranteedSouls
    shuffle_starting_warp_room: RandomizeStartingWarp
    open_drawbridge: OpenDrawbridge
    shop_randomizer: ShopRandomizer
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    shuffle_enemy_drops: ShuffleDrops
    experience_percentage: ExperiencePercent
    soul_drop_percentage: SoulDropPercent
    area_music_randomizer: AreaMusicShuffle
    boss_music_randomizer: BossMusicShuffle
    randomize_red_soul_walls: SoulWallRandomizer
    randomize_synthesis_souls: RandomizeSynthSouls
    no_mp_bat: FreeBat
    passive_soul_eater_ring: PassiveSoulEaterRing
    gate_items: GateItems
    hard_mode: HardMode
    boss_shuffle: BossShuffle
    seal_shuffle: SealShuffle
    randomize_seal_patterns: RandomizeSealPatterns
    menace_condition: MenaceCondition
    mine_condition: MineCondition
    garden_condition: GardenCondition

dos_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        MenaceCondition,
        MineCondition,
        GardenCondition,
        ReplaceMenaceWithSoma

    ]),

    OptionGroup("Soul Settings", [
        SoulRandomizer,
        SoulsanityLevel,
        GuaranteedSouls,
        SoulDropPercent

    ]),

    OptionGroup("Item Options", [
        StartingWeapon,
        ShopRandomizer,
        GateItems

    ]),

    OptionGroup("Seal Settings", [
        DisableBossSeals,
        EarlySeal1,
        SealShuffle,
        RandomizeSealPatterns
    ]),

    OptionGroup("Weapon Synth Settings", [
        RandomizeSynthSouls,

    ]),

    OptionGroup("World Settings", [
        RandomizeStartingWarp,
        OpenDrawbridge,
        SoulWallRandomizer

    ]),

    OptionGroup("Enemy Settings", [
        ShuffleDrops,
        ExperiencePercent,
        HardMode,
        BossShuffle

    ]),

    OptionGroup("Quality of Life", [
        RemoveMoneyGates,
        RevealMap,
        RevealBreakableWalls,
        FixLuck,
        BoostSpeed,
        OneScreenMode,
        FreeBat,
        PassiveSoulEaterRing
    ]),

    OptionGroup("Music Randomizer", [
        AreaMusicShuffle,
        BossMusicShuffle

    ]),
]
