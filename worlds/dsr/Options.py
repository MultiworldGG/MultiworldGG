import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, OptionList, DeathLink, PerGameCommonOptions, OptionCounter, StartInventoryPool
from Options import OptionGroup
from .Skips import get_all_skips, SkipDifficulty


# QoL
class CanWarpWithoutLordvessel(DefaultOnToggle):
    """Gain the ability to warp as soon as you have rested at any warpable bonfire."""
    display_name = "Can Warp Without Lordvessel"

class WarpToAllBonfires(DefaultOnToggle):
    """Makes all bonfires eligible to be warped to via the in-game menu.
    No matter your settings, you will still need to actually rest at the warpable points to be able to warp to them.

    As a side-effect, this will also make warping set your destination as your "return" point upon next death, homeward, etc.
    Warpable bonfires are synced between all saves on the slot, regardless of your choice."""
    display_name = "Warp To All Bonfires"

# Difficulty
class GhostDifficulty(Choice):
    """How to manage difficulty for ghosts.

    - **Normal:** Ghost's behavior is unchanged and no mitigations are made to make them easier to deal with.
    - **Ghosts Are Not Ghostly:** Ghosts can be damaged by all weapons and items.
      Similar to having a transient curse always active.
    - **Rickert Sells Curses:** Rickert, the blacksmith/shopkeeper in the safe part of New Londo, 
      will sell unlimited transient curse items, 1500 souls apiece.
    """
    display_name = "Ghost Difficulty"
    option_normal = 0
    option_ghosts_are_not_ghostly = 1
    option_rickert_sells_curses = 2
    default = 2

class SoulMultiplierBase(Range):
    """Base value for a multiplier applied to enemy & boss soul drops, expressed as a percentage.
    100 is vanilla."""
    display_name = "Soul Multiplier - Base Percentage"
    range_start = 20
    range_end = 500
    default = 100

class SoulMultiplierMax(Range):
    """Maximum (final) value for a multiplier applied to enemy & boss soul drops, expressed as a percentage.
    
    Only takes effect if not equal to soul_multiplier_base, and soul_multiplier_steps is non-zero."""
    display_name = "Soul Multiplier - Maximum Percentage"
    range_start = 20
    range_end = 500
    default = 100

class SoulMultiplierSteps(Range):
    """Number of steps from the base to the maximum multiplier. 
    This is how many "Progressive Soul Multiplier" items will be added to the item pool.
    
    Upon receiving one, the soul multiplier will increase (1/(this value)) * (the distance from max to base).
    As an example, if your soul_multiplier_base is 100, soul_multiplier_max is 200, and this is set to 4, then the
    first such item will set the soul drop multiplier to 125%, 2nd to 150%, and so on.

    Progressive Soul Multiplier update will only take effect when enemies are reloaded or respawned.

    Has no effect if the soul_multiplier_base and soul_multiplier_max are equal.

    If zero, soul_multiplier_base is applied as a static multiplier."""
    display_name = "Soul Multiplier Steps"
    range_start = 0
    range_end = 10
    default = 0

class WeightMultiplierBase(Range):
    """Base value for a multiplier applied to weight of weapons, shields, and armors, expressed as a percentage.
    100 is vanilla weight.
    50 is half weight.
    0 is no weight."""
    display_name = "Weight Multiplier - Base Percentage"
    range_start = 0
    range_end = 300
    default = 100

class WeightMultiplierMin(Range):
    """Minimum (final) value for a multiplier applied to weight of weapons, shields, and armors, expressed as a percentage.

    Only takes effect if not equal to weight_multiplier_base, and weight_multiplier_steps is non-zero."""
    display_name = "Weight Multiplier - Minimum Percentage"
    range_start = 0
    range_end = 300
    default = 100

class WeightMultiplierSteps(Range):
    """Number of steps from the base to the minimum multiplier. 
    This is how many "Progressive Weight Reducer" items will be added to the item pool.
    
    Upon receiving one, the weight multiplier will decrease (1/(this value)) * (the distance from base to min).
    As an example, if your weight_multiplier_base is 100, weight_multiplier_min is 20, and this is set to 4, then the
    first such item will set the weight multiplier to 80%, 2nd to 60%, and so on.

    Has no effect if the weight_multiplier_base and weight_multiplier_min are equal.

    If zero, weight_multiplier_base is applied as a static multiplier.

    If you want to turn off weapon and armor weight entirely, set weight_multiplier_base and this value both to 0."""
    display_name = "Weight Multiplier Steps"
    range_start = 0
    range_end = 10
    default = 0

# Game Options
class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class ExcludedLocationBehaviorOption(Choice):
    """How to choose items for excluded locations in DSR.

    - **Forbid Useful:** Neither progression items nor useful items can be placed in excluded
      locations.
    - **Do Not Randomize:** Excluded locations always contain the same item as in vanilla
      Dark Souls: Remastered.
    """
    display_name = "Excluded Locations Behavior"
    option_forbid_useful = 2
    option_do_not_randomize = 3
    default = 2

class FogwallSanity(DefaultOnToggle):
    """Makes area fog walls uninteractable until you receive their items from the item pool. 
    Fog walls will also give checks when you pass through them.
    The Undead Asylum fog wall will not be locked, to avoid super-early BK.
    Recommended to turn this on."""
    display_name = "Fogwall Sanity" 

class BossFogwallSanity(Toggle):
    """Makes boss fog walls uninteractable until you receive their items from the item pool.
    Boss fog walls will also give checks when you pass through them.
    The following will be neither locations nor checks as they all do not have fog walls
    upon your first entry into their arena:
      Asylum Demon (first encounter),
      Sif,
      Seath (2nd encounter), and
      Kalameet."""
    display_name = "Boss Fogwall Sanity" 

class BossSoulShuffle(DefaultOnToggle):
    """Makes boss soul drops be shuffled into the multiworld item pool.
    Does not affect the Lord Souls, which are always shuffled in."""
    display_name = "Boss Soul Shuffle"

class BossHumanityShuffle(DefaultOnToggle):
    """Makes boss humanity and twin humanity drops be shuffled into the multiworld item pool."""
    display_name = "Boss Humanity Shuffle"

class BossBoneShuffle(Toggle):
    """Makes boss homeward bone drops be shuffled into the multiworld item pool."""
    display_name = "Boss Bone Shuffle"

class BlackKnightWeaponShuffle(DefaultOnToggle):
    """Makes Black Knight weapon drop locations guaranteed, and adds their weapons to the multiworld item pool.
    This only applies to the 7 non-respawning Black Knights in the game.
    With this off, their Titanite Chunk drops are still added to the pool, and the weapon drops are left to chance.

    These weapons are quite powerful, and this option adds 2 Swords, 2 Halberds, 1 Greataxe, 1 Greatsword, and 1 Shield to the pool."""
    display_name = "Black Knight Weapon Shuffle"

class CrystalLizardShuffle(Toggle):
    """Adds Crystal Lizard drop locations to the multiworld item pool.
    This adds 2 locations per lizard: 1 for their Twinkling Titanite, and 1 for an additional drop - which is made guaranteed.
    
    There are 25 total crystal lizards, 10 of which are in the Great Hollow, and 5 of which are in the DLC.
    If one escapes, typically you can quit out and reload to respawn it.
    Great Hollow lizards may each require several reloads, because they only have a 1 in 3 chance to activate each time."""
    display_name = "Crystal Lizard Shuffle"

class LimitedShopItemShuffle(DefaultOnToggle):
    """Adds limited quantity shop slots from unmissable shopkeepers as locations, and shuffles their items into the multiworld.
    Missable shopkeepers, who can be made unavailable based on progression or dialogue options, will not have their shops shuffled into the multiworld.
    Shuffled Shops' keepers will be made immune to player attacks to make them unmissable, and their drops added as shuffled locations to their shop.
    
    Shops Shuffled by this option:
    Andre of Astora
    Big Hat Logan
    Crestfallen Merchant
    Domhnall of Zena (not including post-boss equipment yet)
    Female Undead Merchant
    Giant Blacksmith (shared Repairbox and Blacksmith Giant Hammer)
    Griggs of Vinheim
    Hawkeye Gough
    Male Undead Merchant
    Marvelous Chester
    Oswald of Carim
    Petrus of Thorolund
    Rickert of Vinheim
    Vamos (shared Repairbox + 2 drops only)
    """
    display_name = "Limited Shop Item Shuffle"

class ShopHints(Choice):
    """When Shop items are shuffled, this options control what types of Archipelago Hints will be created upon talking to the relevant merchant (with the shop slots unlocked)."""
    display_name = "Shop Hints"
    option_off = 0
    option_progression = 1
    option_progression_and_useful = 2
    option_all = 3
    default = 1

def skip_logic_helper(difficulty: SkipDifficulty): 
    available_skips = get_all_skips()
    valid_keys = {skip.name for skip in available_skips if skip.difficulty == difficulty}
    default = {skip.name: 0 for skip in available_skips if skip.difficulty == difficulty}

    return valid_keys, default

class SkipLogicEasy(OptionCounter):
    """ In the following section you can enable specific skips to perform. The skips are losely categorized by their difficulty. 
        Numbers other than 0 put the skip into logic.
        Recommended to edit in the yaml, due to problems in Options Creator. 

        For more detailed description of each individual skip visit https://docs.google.com/spreadsheets/d/1X7CHM0lT8vMiZmlGNtzdr3UXz71onuuRC2FyrNRw-UQ/edit?gid=840526629#gid=840526629
    """
    display_name = "Enabled Easy Skips"
    available_skips = get_all_skips()
    difficulty = SkipDifficulty.EASY
    valid_keys, default = skip_logic_helper(difficulty)


class SkipLogicMedium(OptionCounter):
    display_name = "Enabled Medium Skips"
    difficulty=SkipDifficulty.MEDIUM
    valid_keys, default = skip_logic_helper(difficulty)


class SkipLogicHard(OptionCounter):
    display_name = "Enabled Hard Skips"
    difficulty=SkipDifficulty.HARD
    valid_keys, default = skip_logic_helper(difficulty)

class SkipLogicVeryHard(OptionCounter):
    display_name = "Enabled Very Hard Skips"
    difficulty=SkipDifficulty.VERY_HARD
    valid_keys, default = skip_logic_helper(difficulty)

class LogicToAccessFirelinkAltar(Choice):
    """Firelink Altar logical Access requirement.
     Before the chosen condition, Firelink Altar will be considered "out of logic".
     This will also restrict logical access to areas behind golden fog walls, since Firelink Altar access is required for placing the lordvessel.
     This will not actually prevent you from accessing the Altar from either Serpent.

    - **Either:** As soon as you can reach either Serpent (Kaathe or Frampt), Firelink Altar in-logic. It is left up to chance (the generate process) which one is expected by the logic.
    - **Both:** Only when both Serpents are accessible is Firelink Altar considered in-logic. This is the "safest" option.
    - **Frampt:** (default) Frampt being accessible puts Firelink Altar in-logic (both bells can be rung)
    - **Kaathe:** Kaathe being accessible puts Firelink Altar in-logic (via defeating the Four Kings in the Abyss under New Londo).

    If you accidentally dismiss or anger Kaathe, and this option is "Either" or "Kaathe", thus making you unable to get to the altar, you can use the /warp FA command in the client to warp to the altar."""
    display_name = "Logic Requirement to Access Firelink Altar"
    option_either_serpent = 0
    option_both_serpents = 1
    option_frampt = 2
    option_kaathe = 3
    default = 2

class LogicToAccessCatacombs(Choice):
    """Artificial logic for The Catacombs access. 
     Before the chosen condition, The Catacombs will be considered "out of logic"

    - **no_logic:** (not recommended) Catacombs is in-logic as soon as you get to Firelink Shrine.
    - **undead_merchant:** Access to Undead Merchant in the Upper Undead Burg puts Catacombs in-logic.
    - **andre:** Access to Andre puts Catacombs in-logic.
    - **andre_or_undead_merchant:** Access to either Andre or Undead Merchant puts Catacombs in-logic.
    - **ornstein_and_smough:** (Default) Access to Ornstein and Smough puts Catcombs in-logic."""
    display_name = "Logic Requirement to Access Catacombs"
    option_no_logic = 0
    option_undead_merchant = 1
    option_andre = 2
    option_andre_or_undead_merchant = 3
    option_ornstein_and_smough = 4
    default = 4

class LogicToAccessTotG(Choice):
    """Artificial logic for Tomb of the Giants (TotG) access.
     Before the chosen condition, TotG will be considered "out of logic".

    - **no_logic:** TotG is in-logic as soon as you defeat Pinwheel.
    - **skull_lantern:** Receiving a Skull Lantern as an AP item puts TotG in-logic.
    - **sunlight_maggot:** Receiving a Sunlight Maggot as an AP item puts TotG in-logic.
    """
    display_name = "Logic Requirement to Access Tomb of the Giants"
    option_no_logic = 0
    option_skull_lantern = 1
    option_sunlight_maggot = 2
    default = 1

class RandomizeStartingLoadouts(DefaultOnToggle):
    """Randomize each class's starting weapons, shields, and armors.
    This will also replace the thief's master key, which would break logic.
    Shields will always be 1-handed-wieldable with starting stats.
    Weapons will always be at least 2-handed-wieldable with starting stats.
    You can see what weapons/shield/item each class starts with in their description.
    Starting spells are randomized separately.""" 
    display_name = "Randomize Starting Loadout"

class RandomizeStartingGifts(DefaultOnToggle):
    """Randomize the starting gift options to a subset of a custom item pool.
    This pool includes many additional consumable options, and some rings.
    This pool also includes most of the default gifts, except Master key, which breaks logic.
    """
    display_name = "Randomize Starting Gifts"

class RequireOneHandedStartingWeapons(DefaultOnToggle):
    """If randomize_starting_loadouts is on, this option determines if each class's weapons can be wielded with one hand with their starting stats.
    Ignored if no_weapon_requirements is true."""
    display_name = "Require One Handed Starting Weapons"

class ExtraStartingWeaponForMeleeClasses(Toggle):
    """If randomize_starting_loadouts is on, this option determines if melee classes will get a second melee weapon."""
    display_name = "Extra Starting Weapon For Melee Classes"
    
class ExtraStartingShieldForAllClasses(Toggle):
    """If randomize_starting_loadouts is on, this option determines if all classes will get a second starting shield."""
    display_name = "Extra Starting Shield For All Classes"

class StartingSorcery(Choice):
    """How to randomize starting sorceries.
    Limited to spells the sorcerer can cast with their starting stats, unless "remove_spell_stat_requirements" is on.

    - **Soul Arrow:** Default option - vanilla starting sorcery
    - **Any:** Any sorcery
    - **Attack:** Any attack sorcery"""
    display_name = "Starting Sorcery"
    option_soul_arrow = 0
    option_any = 1
    option_attack = 2
    default = 0

class StartingMiracle(Choice):
    """How to randomize starting miracles.
    Limited to spells the cleric can cast with their starting stats, unless "remove_spell_stat_requirements" is on.

    - **Heal:** Default option - vanilla starting miracle
    - **Any:** Any miracle
    - **Healing:** Any healing miracle"""
    display_name = "Starting Miracle"
    option_heal = 0
    option_any = 1
    option_healing = 3
    default = 0

class StartingPyromancy(Choice):
    """How to randomize starting pyromancies.

    - **Fireball:** Default option - vanilla starting pyromancy
    - **Any:** Any pyromancy
    - **Attack:** Any attack pyromancy"""
    display_name = "Starting Pyromancy"
    option_fireball = 0
    option_any = 1
    option_attack = 2
    default = 0

class NoWeaponRequirements(Toggle):
    """Removes weapon and shield stat requirements."""
    display_name = "No Weapon Stat Requirements"

class NoSpellStatRequirements(Toggle):
    """Removes stat requirements for casting all miracles and sorceries."""
    display_name = "No Spell Stat Requirements"

class NoMiracleCovenantRequirements(DefaultOnToggle):
    """Removes covenant requirements for casting certain miracles."""
    display_name = "No Miracle Covenant Requirements"

class UpgradedWeaponsPercentage(Range):
    """Percentage of weapons (including shields) in the pool that will be replaced with upgraded versions, if possible.
    Does not affect starting equipment.
    Choose a higher value for an easier time."""
    display_name = "Upgraded Weapons Percentage"
    range_start = 0
    range_end = 100
    default = 0

class UpgradedWeaponsAllowedInfusions(OptionList):
    """Which infusions are allowed if UpgradedWeapons.
    Available infusion types are Normal, Raw, Magic, Fire, Divine, Chaos, Enchanted, Occult, Crystal, and Lightning.
    If "Normal" is removed, all upgraded weapons will have a different, available infusion."""
    display_name = "Upgraded Weapons - Allowed Infusions"
    default = {"Normal", "Raw", "Magic", "Fire", "Divine", "Chaos", "Enchanted", "Occult", "Crystal", "Lightning"}
    valid_keys = ["Normal", "Raw", "Magic", "Fire", "Divine", "Chaos", "Enchanted", "Occult", "Crystal", "Lightning"]

class UpgradedWeaponsAdjustedLevels(DefaultOnToggle):
    """For upgraded weapons added to the pool, Whether to 'adjust' weapon levels for applying the ranges.
    When true, the min/max levels will apply to an calculated "level" of an infused weapon adjusted by:
     +5 for Raw/Magic/Fire/Divine
     +10 for Chaos/Enchanted/Occult/Crystal/Lightning 
    When false, the min/max levels will not be adjusted."""
    display_name = "Upgraded Weapons - Adjust Ranges"

class UpgradedWeaponsMinLevel(Range):
    """Minimum upgrade value on upgraded weapons in the pool.
    This can exclude certain infusions if their calculated level cannot be at the minimum level. """
    display_name = "Upgraded Weapons - Minimum Level"
    range_start = 0
    range_end = 15
    default = 0


class UpgradedWeaponsMaxLevel(Range):
    """Maximum upgrade plus value on upgraded weapons in the pool."""
    display_name = "Upgraded Weapons - Maximum Level"
    range_start = 0
    range_end = 15
    default = 15

class EnableDeathlinkOption(Toggle):
    """Includes Deathlink"""
    display_name = "Enable Deathlink"

class GoalConditionOption(Choice):
    """Set the goal condition
    
    - **Gwyn:** Default option -Beat Gwyn, Lord of Cinder
    - **Bosses:** Defeat all bosses
    - **Ornstein and Smough:** Kill Ornstein and Smough"""
    display_name = "Goal Condition"
    option_gwyn = 0
    option_all_bosses = 1
    option_ornstein_and_smough = 2
    option_manus = 3
    default = 0
    
# Group relevant options
option_groups = [
    OptionGroup("Quality of Life", [
        CanWarpWithoutLordvessel,
        WarpToAllBonfires,
        ]),
    OptionGroup("Difficulty", [
        GhostDifficulty,
        SoulMultiplierBase,
        SoulMultiplierMax,
        SoulMultiplierSteps,
        WeightMultiplierBase,
        WeightMultiplierMin,
        WeightMultiplierSteps,
        ]),
    OptionGroup("Sanity", [
        FogwallSanity,
        BossFogwallSanity,
        ]),
    OptionGroup("Shuffling", [
        BossSoulShuffle,
        BossHumanityShuffle,
        BossBoneShuffle,
        BlackKnightWeaponShuffle,
        CrystalLizardShuffle,
        ]),
    OptionGroup("Shops", [
        LimitedShopItemShuffle,
        ShopHints,
        ]),
    OptionGroup("Logic", [
        LogicToAccessFirelinkAltar,
        LogicToAccessCatacombs,
        LogicToAccessTotG,
        ]),
    # OptionGroup("Skip Logic - Warning!", [
    #     SkipLogicEasy,
    #     SkipLogicMedium,
    #     SkipLogicHard,
    #     SkipLogicVeryHard
    #     ]),
    OptionGroup("Equipment", [
        RandomizeStartingLoadouts,
        RandomizeStartingGifts,
        RequireOneHandedStartingWeapons,
        ExtraStartingWeaponForMeleeClasses,
        ExtraStartingShieldForAllClasses,
        StartingSorcery,
        StartingMiracle,
        StartingPyromancy,
        NoWeaponRequirements,
        NoSpellStatRequirements,
        NoMiracleCovenantRequirements
        ]),
    OptionGroup("Upgraded Weapons", [
        UpgradedWeaponsPercentage,
        UpgradedWeaponsAllowedInfusions,
        UpgradedWeaponsAdjustedLevels,
        UpgradedWeaponsMinLevel,
        UpgradedWeaponsMaxLevel,
        ])
    ]


@dataclass
class DSROption(PerGameCommonOptions):

    # Game Options
    enable_deathlink: EnableDeathlinkOption
    goal_condition: GoalConditionOption
    guaranteed_items: GuaranteedItemsOption
    excluded_location_behavior: ExcludedLocationBehaviorOption
    start_inventory_from_pool: StartInventoryPool

    # QoL
    can_warp_without_lordvessel: CanWarpWithoutLordvessel
    warp_to_all_bonfires: WarpToAllBonfires
  
  
    # Difficulty
    ghost_difficulty: GhostDifficulty
    soul_multiplier_base: SoulMultiplierBase
    soul_multiplier_max: SoulMultiplierMax
    soul_multiplier_steps: SoulMultiplierSteps
    weight_multiplier_base: WeightMultiplierBase
    weight_multiplier_min: WeightMultiplierMin
    weight_multiplier_steps: WeightMultiplierSteps

    # Sanity
    fogwall_sanity: FogwallSanity
    boss_fogwall_sanity: BossFogwallSanity

    # Shuffling
    boss_soul_shuffle: BossSoulShuffle
    boss_humanity_shuffle: BossHumanityShuffle
    boss_bone_shuffle: BossBoneShuffle
    bk_weapon_shuffle: BlackKnightWeaponShuffle
    lizard_shuffle: CrystalLizardShuffle

    # Shops
    limited_shop_item_shuffle: LimitedShopItemShuffle
    shop_hints: ShopHints

    # Logic
    logic_to_access_firelink_altar: LogicToAccessFirelinkAltar
    logic_to_access_catacombs: LogicToAccessCatacombs
    logic_to_access_totg: LogicToAccessTotG

    # Skip Logic
    # skip_logic_easy: SkipLogicEasy
    # skip_logic_medium: SkipLogicMedium
    # skip_logic_hard: SkipLogicHard
    # skip_logic_very_hard: SkipLogicVeryHard

    # Equipment
    randomize_starting_loadouts: RandomizeStartingLoadouts
    randomize_starting_gifts: RandomizeStartingGifts
    require_one_handed_starting_weapons: RequireOneHandedStartingWeapons
    extra_starting_weapon_for_melee_classes: ExtraStartingWeaponForMeleeClasses
    extra_starting_shield_for_all_classes: ExtraStartingShieldForAllClasses
    starting_sorcery: StartingSorcery
    starting_miracle: StartingMiracle
    starting_pyromancy: StartingPyromancy
    no_weapon_requirements: NoWeaponRequirements
    no_spell_stat_requirements: NoSpellStatRequirements
    no_miracle_covenant_requirements: NoMiracleCovenantRequirements

    # Upgraded Weapons
    upgraded_weapons_percentage: UpgradedWeaponsPercentage
    upgraded_weapons_allowed_infusions: UpgradedWeaponsAllowedInfusions
    upgraded_weapons_adjusted_levels : UpgradedWeaponsAdjustedLevels
    upgraded_weapons_min_level: UpgradedWeaponsMinLevel
    upgraded_weapons_max_level: UpgradedWeaponsMaxLevel
