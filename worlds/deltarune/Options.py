from enum import StrEnum

from Options import Choice, Toggle, Range, PerGameCommonOptions, NamedRange, OptionGroup
from dataclasses import dataclass


class ProgressionBalancing(NamedRange):
    """
    ATTEMPTS TO BALANCE THE PROGRESSION OF YOUR ITEMS.

    SETTING THE VALUE LOWER WILL RESULT IN MORE WAITING TO RECIEVE ITEMS.

    SETTING THE VALUE HIGHER WILL RESULT IN LESS WAITING TO RECIEVE ITEMS.
    """

    default = 50
    range_start = 0
    range_end = 99
    display_name = "Progression Balancing"
    rich_text_doc = True
    special_range_names = {
        "disabled": 0,
        "normal": 50,
        "extreme": 99,
    }


class Accessibility(Choice):
    """
    SETS THE RULES FOR THE ABILITY TO REACH ALL ITEMS.

    - **Full** *GUARANTEES THAT ALL ITEMS CAN BE OBTAINED.*

    - **Minimal** *GUARANTEES ONLY WHAT IS NECESSARY, BUT NO MORE.*
    """

    display_name = "Accessibility"
    rich_text_doc = True
    option_full = 0
    option_minimal = 2
    alias_none = 2
    alias_locations = 0
    alias_items = 0
    default = 0


class BetterOdds(Toggle):
    """
    SHOULD EVENTS RELIANT ON LUCK HAVE BETTER ODDS TO HAPPEN?

    - **Chapter 1&2 Eggs**
    """

    display_name = "Better Odds"
    default = 0


class ChosenRoute(Choice):
    """
    CHOOSE THE ROUTE THAT YOU PREFER.

    - **Neutral Route** *Proceed through the story normally.*
    - **Weird Route** *Proceed through the "Weird Route" storyline while losing all possible recruits.*
    - **All Recruits** *Progress through the story by recruiting everyone.*
    - **All Routes** *Both All Recruits and Weird Route at the same times.*
      *(Doesn't require to finish multiple times chapter, either ending would count as completing a chapter)*

    (The chosen route only chooses if recruiting or loosing recruits are included or not.)
    (This doesn't require you to finish a chapter with a specific route yet, but will in the future.)
    """

    display_name = "Chosen Route"
    option_all_recruits = 0
    option_weird_route = 1
    option_all_routes = 2
    option_neutral_route = 3
    default = option_all_recruits


class ChosenRouteOptions(StrEnum):
    all_recruits = "all_recruits"
    weird_route = "weird_route"
    all_routes = "all_routes"
    neutral_route = "neutral_route"


class RandomizeChapters(Choice):
    """
    HOW WILL YOU PROGRESS THROUGH THE CHAPTERS?

    - **In Order** *The next chapter will be unlocked once you complete the one you're in.*
    - **Randomized** *Chapters are unlocked through getting items. You'll be expected to move in-between chapters a lot.*
    - **All Unlocked** *All chapters are unlocked from the start. You will be expected to play through another chapter once stuck.*

    (The goal is closing the final fountain of each chapter whatever the option chosen.)
    """

    display_name = "Randomize Chapters"
    option_in_order = 0
    option_randomized = 1
    option_all_unlocked = 2
    default = option_all_unlocked


class StartingChapter(Choice):
    """
    WHICH CHAPTER WILL BEGIN THE JOURNEY?

    (This only applies if you set Randomize Chapters to random.)
    """

    display_name = "Starting Random Chapter"
    option_random_chapter = 0
    option_chapter_1 = 1
    option_chapter_2 = 2
    option_chapter_3 = 3
    option_chapter_4 = 4
    default = option_random_chapter


class RandomizeChapterOptions(StrEnum):
    in_order = "in_order"
    randomized = "randomized"
    all_unlocked = "all_unlocked"


class RandomizeSecretBosses(Choice):
    """
    ITEMS GIVEN BY SECRET BOSSES WILL BE RANDOMIZED OR EVEN REQUIRED.

    - **Mandatory** *Secret Bosses rewards will be randomized and required to do to access the fountain*

    *Secret bosses are: Jevil, Spamton Neo, Mantle/ERAM, Chapter 3 Knight, Hammer of Justice*
    """

    display_name = "Randomize Secret Bosses"
    option_false = 0
    option_true = 1
    option_mandatory = 2
    default = option_false


class RandomizeSecretBossesOptions(StrEnum):
    false = "false"
    true = "true"
    mandatory = "mandatory"


class RandomizeMANTLE(Choice):
    """
    CHECKS RECIEVED IN THE ORIGINAL GAME OF THE THIRD CHAPTER WILL BE RANDOMIZED.

    - **Mantleless** *Items in the Original Game will be randomized but the Shadow Mantle/ERAM fight isn't mandatory if secret bosses is set to mandatory*
    """

    display_name = "Randomize MANTLE"
    option_false = 0
    option_true = 1
    option_mantleless = 2
    default = option_false


class RandomizeMANTLEOptions(StrEnum):
    false = "false"
    true = "true"
    mantleless = "mantleless"


class IncludeShadowMantle(Toggle):
    """
    THE SHADOW MANTLE WILL BE IN THE RANDOM ITEM POOL OF THE THIRD CHAPTER.

    - **False** *The Shadow Mantle is the reward for beating the Shadow Mantle/ERAM*
    - **True** *The Shadow Mantle will be in the itempool in logic before Knight fight*
    """

    display_name = "Include Shadow Mantle"
    default = 1


class ExcludeTRank(Toggle):
    """
    THE HIGHEST RANK OF THE THIRD CHAPTER WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude T Rank"
    default = 1


class ExcludeZRank(Toggle):
    """
    THE LOWEST RANK OF THE THIRD CHAPTER WILL BE EXCLUDED FROM CONTAINING AN IMPORTANT ITEM.
    """

    display_name = "Exclude Z Rank"
    default = 1


class IncludeTRankOptions(StrEnum):
    false = "false"
    true = "true"
    excluded_from_logic = "excluded_from_logic"


class ItemBalancing(Toggle):
    """
    IF AN ITEM IS OBTAINED EARLY, ITS POWER WILL BE SCALED DOWN.

    *Formula is basically `item_stat * (current_chapter / item_chapter)`, only scaling down*
    """

    display_name = "ItemBalancing"
    default = 0


class IncludeHiddenItems(Toggle):
    """
    RANDOMIZES ITEMS THAT ARE CONSIDERABLY MORE DIFFICULT TO FIND OR TEDIOUS TO OBTAIN.

    - **Golden Prizes**
    - **Eggs**
    - **Dog Dollars**
    - **Moss**
    """

    display_name = "Randomize Grindy/Hidden Items"
    default = 0


class IncludeSecretBossesItemsRequirement(Toggle):
    """
    RANDOMIZES ITEMS THAT ARE NECESSARY TO ACCESS SECRET BOSSES.

    - **Broken Keys**
    - **Door Key**
    - **KeyGen**
    - **Empty Disk**

    *(For MANTLE items, see the RandomizeMANTLE option)*
    """

    display_name = "Randomize Items required for Secret Bosses"
    default = 1


class RemoveStartingEquipment(Toggle):
    """
    SHOULD STARTING FROM A CHAPTER MAKE THE HEROES HAVE NOTHING?

    *(Normally if you start a save file on a chapter, you'll start with some equipment from the previous two chapters.)*
    *(If this option is set to true, you'll start every chapter like chapter 1, with no armors and only the starting weapons.)*
    *(However, If you're continuing through to the next chapter using completion data, you'll keep your stuff.)*
    """

    display_name = "Remove Starting Equipment"
    default = 1


class IncludeChapter1(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 1?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 1"
    default = 1


class Chapter1Recruit(Toggle):
    """
    THE SYSTEM TO RECRUIT ENEMIES WILL BE PRESENT IN THE FIRST CHAPTER.
    """

    display_name = "Recruits/Lost for chapter 1"
    default = 1


class IncludeChapter2(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 2?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 2"
    default = 1


class IncludeLoseSwatchling(Toggle):
    """
    WILL LOSING THE SWATCHLING RECRUIT BE A CHECK LOCATION?

    *(Since Swatchlings don't normally appear in weird route, enabling this means you have to do Singapore Wrong Warps.)*
    *(In All Routes, it requires either reloading your save on a regular route or doing the wrong warp again.)*
    """

    display_name = "Include Lose Swatchling"
    default = 0


class ExcludePostChapter2Locations(Toggle):
    """
    WILL LOCATIONS EXCLUSIVE TO THE END OF CHAPTER 2 BE KEPT AWAY FROM HOLDING IMPORTANT ITEMS?

    - CH2: Castle Town - Tasque Manager Says Challenge
    - CH2: Castle Town - Ch2 All Stars Challenge

    *(Since you "beat" the chapter after sealing the Cyber World fountain,)*
    *(enabling this means you can just go to the next chapter afterwards.)*
    """

    display_name = "Exclude Post-Chapter 2 Locations"
    default = 0


class IncludeChapter3(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 3?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 3"
    default = 1


class IncludeChapter4(Toggle):
    """
    DO YOU WISH TO PLAY CHAPTER 4?

    *(Items from this chapter will also be included)*
    """

    display_name = "Include Chapter 4"
    default = 1


class MacGuffinChapter1(Range):
    """
    A NEW ROADBLACK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 1.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (King-Shaped Key Pieces)
    """

    display_name = "Macguffin Chapter 1 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter2(Range):
    """
    A NEW ROADBLACK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 2.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (KeyGen 2 Segments)
    """

    display_name = "Macguffin Chapter 2 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter3(Range):
    """
    A NEW ROADBLACK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 3.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (Remote Batteries)
    """

    display_name = "Macguffin Chapter 3 Amount"
    default = 0
    range_start = 0
    range_end = 10


class MacGuffinChapter4(Range):
    """
    A NEW ROADBLACK WILL APPEAR BEFORE THE FINAL BOSS OF CHAPTER 4.

    THIS OPTION DETERMINES HOW MANY OF THESE ITEMS WILL BE REQUIRED TO PROGRESS.

    (Combination Lock Digits)
    """

    display_name = "Macguffin Chapter 4 Amount"
    default = 3
    range_start = 0
    range_end = 10


class MacGuffinExtra(Range):
    """
    THE AMOUNT OF EXTRA ITEMS IN THE ITEMPOOL TO UNBLOCK THE ROAD TO FINAL BOSSES.

    *(So, if you choose to have 3 macguffin items in Chapter 1 and set this option to 1,)*
    *(you'll have 4 macguffin items in the pool, but you'll still only need 3 to progress)*
    """

    display_name = "Extra MacGuffin Amount"
    default = 1
    range_start = 0
    range_end = 5


class DeathLink(Toggle):
    """
    YOUR FAILURE CAUSES THE FAILURE OF EVERYONE WHO HAS ENABLED THIS OPTION.

    TO COMPLIMENT, THE REVERSE IS TRUE AS WELL.
    """

    display_name = "Death Link"
    default = 0


filler_weight_range_names = {"common": 50, "uncommon": 25, "rare": 10, "very rare": 5, "extremely rare": 1}


class FillerHealingWeight(NamedRange):
    """
    DETERMINES HOW OFTEN HEALING ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Healing Items Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["common"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerCurrencyWeight(NamedRange):
    """
    DETERMINES HOW OFTEN ALL CURRENCIES WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Currency Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["uncommon"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class TrapWeight(NamedRange):
    """
    DETERMINES HOW OFTEN TRAPS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Trap Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["uncommon"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerArmorWeight(NamedRange):
    """
    DETERMINES HOW OFTEN ARMOR ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Armors Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerTensionWeight(NamedRange):
    """
    DETERMINES HOW OFTEN TENSION ITEMS WILL APPEAR COMPARED TO OTHERS ITEMS.
    """

    display_name = "Tension Items Weights"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["very rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class FillerSMILEWeight(NamedRange):
    """
    DETERMINES HOW OFTEN IT WILL SMILE.
    """

    display_name = "SMILE Weight"
    range_start = 0
    range_end = 99
    default = filler_weight_range_names["extremely rare"]
    rich_text_doc = True
    special_range_names = filler_weight_range_names


class ProgressiveKrisWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE CAGE WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Kris Weapons"
    default = 1


class ProgressiveSusieWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE GIRL WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Susie Weapons"
    default = 1


class ProgressiveRalseiWeapons(Toggle):
    """
    THE WEAPONS RECEIVED FOR THE PRINCE WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Ralsei Weapons"
    default = 1


class ProgressiveNoelleWeapons(Toggle):
    """
    THE FORBIDDEN RINGS WILL BE IN SEQUENTIAL ORDER OF RISING POWER.
    """

    display_name = "Progressive Noelle Weapons"
    default = 1


class UnlockCharacters(Choice):
    """
    THE ABILITY TO USE HEROES IN COMBAT SEQUENCIES WILL NEED TO BE UNLOCKED.
    
    *(If someone isn't unlocked, they'll be at -666HP, and you can't use them in battle.)*
    *(If nobody is unlocked, then it will immediately be the enemy's turn, but you still get one hit to live.)*
    """

    display_name = "Unlock Characters"
    option_false = 0
    option_true = 1
    option_except_kris = 2
    default = option_false


class UnlockCharactersOptions(StrEnum):
    false = "false"
    true = "true"
    except_kris = "except_kris"


class IncludeUnusedItems(Choice):
    """
    CERTAIN ITEMS ARE NOT NORMALLY PRESENT.
    WILL THEY NOW BE WITH THE REST?

    - **True without EveryBodyWeapon** *(Include unused items but without EveryBodyWeapon, which is a super powerful unbalanced item probably used by the dev team for debugging.)*
    """

    display_name = "Include Unused Items"
    option_false = 0
    option_true = 1
    option_true_without_everybodyweapon = 2
    default = option_false


class IncludeUnusedItemsOptions(StrEnum):
    false = "false"
    true = "true"
    true_without_everybodyweapon = "true_without_everybodyweapon"


class IncludeMike(Choice):
    """
    WILL THE DEFEAT OF THE MICROPHONE IMITATORS AS WELL AS THEIR GAMES COUNT AS CHECK LOCATIONS?
    """

    display_name = "Include Mike"
    option_false = 0
    option_battle_only = 1
    option_battle_and_games = 2
    default = option_false


class ExcludeMikePlatinum(Toggle):
    """
    WILL THE PLATINUM TROPHY IN THE MICROPHONE IMITATORS' GAMES BE KEPT AWAY FROM HOLDING AN IMPORTANT ITEM?
    """

    display_name = "Exclude Platinum trophy"
    default = 0


class IncludeMikeOptions(StrEnum):
    false = "false"
    battle_only = "battle_only"
    battle_and_games = "battle_and_games"


class UnlockFunGangActions(Toggle):
    """
    THE ABILITY TO USE THE ACTIONS OF THE GIRL, THE PRINCE, AND THE WHITE CLOAK WILL BE AN ITEM.
    """

    display_name = "Unlock S/R/N-Actions"
    default = 1


deltarune_option_groups = [
    OptionGroup(
        "Chapters",
        [
            RandomizeChapters,
            StartingChapter,
            RemoveStartingEquipment,
            MacGuffinExtra,
        ],
    ),
    OptionGroup("Chapter 1", [IncludeChapter1, MacGuffinChapter1, Chapter1Recruit]),
    OptionGroup("Chapter 2", [IncludeChapter2, MacGuffinChapter2, IncludeLoseSwatchling, ExcludePostChapter2Locations]),
    OptionGroup(
        "Chapter 3",
        [
            IncludeChapter3,
            MacGuffinChapter3,
            RandomizeMANTLE,
            IncludeShadowMantle,
            ExcludeTRank,
            ExcludeZRank,
        ],
    ),
    OptionGroup("Chapter 4", [IncludeChapter4, MacGuffinChapter4, IncludeMike, ExcludeMikePlatinum]),
    OptionGroup(
        "Fillers",
        [
            FillerHealingWeight,
            FillerCurrencyWeight,
            TrapWeight,
            FillerArmorWeight,
            FillerTensionWeight,
            FillerSMILEWeight,
        ],
    ),
    OptionGroup(
        "Goal",
        [
            ChosenRoute,
            RandomizeSecretBosses,
        ],
    ),
    OptionGroup(
        "Items",
        [
            IncludeHiddenItems,
            IncludeSecretBossesItemsRequirement,
            IncludeUnusedItems,
            ProgressiveKrisWeapons,
            ProgressiveSusieWeapons,
            ProgressiveRalseiWeapons,
            ProgressiveNoelleWeapons,
            UnlockCharacters,
            UnlockFunGangActions,
        ],
    ),
]


@dataclass
class DeltaruneOptions(PerGameCommonOptions):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility
    remove_starting_equipment: RemoveStartingEquipment
    include_chapter_1: IncludeChapter1
    include_chapter_2: IncludeChapter2
    include_chapter_3: IncludeChapter3
    include_chapter_4: IncludeChapter4
    randomize_chapters: RandomizeChapters
    starting_chapter: StartingChapter
    chosen_route: ChosenRoute
    include_lose_swatchling: IncludeLoseSwatchling
    exclude_post_chapter_2_locations: ExcludePostChapter2Locations
    item_balancing: ItemBalancing
    macguffin_chapter_1: MacGuffinChapter1
    macguffin_chapter_2: MacGuffinChapter2
    macguffin_chapter_3: MacGuffinChapter3
    macguffin_chapter_4: MacGuffinChapter4
    macguffin_extra: MacGuffinExtra
    randomize_secret_bosses: RandomizeSecretBosses
    randomize_mantle: RandomizeMANTLE
    include_shadow_mantle: IncludeShadowMantle
    exclude_t_rank: ExcludeTRank
    exclude_z_rank: ExcludeZRank
    include_hidden_items: IncludeHiddenItems
    include_secret_bosses_items_requirement: IncludeSecretBossesItemsRequirement
    include_unused_items: IncludeUnusedItems
    death_link: DeathLink
    filler_healing_weight: FillerHealingWeight
    filler_currency_weight: FillerCurrencyWeight
    trap_weight: TrapWeight
    filler_armor_weight: FillerArmorWeight
    filler_tension_weight: FillerTensionWeight
    filler_smile_weight: FillerSMILEWeight
    progressive_kris_weapons: ProgressiveKrisWeapons
    progressive_susie_weapons: ProgressiveSusieWeapons
    progressive_ralsei_weapons: ProgressiveRalseiWeapons
    progressive_noelle_weapons: ProgressiveNoelleWeapons
    unlock_characters: UnlockCharacters
    include_mike: IncludeMike
    exclude_mike_platinum: ExcludeMikePlatinum
    better_odds: BetterOdds
    unlock_fun_gang_actions: UnlockFunGangActions
    chapter_1_recruit: Chapter1Recruit


#    include_traps: IncludeTraps

options_presets = {
    "Complete Experience": {
        "remove_starting_equipment": True,
        "randomize_chapters": "randomized",
        "chosen_route": "all_routes",
        "macguffin_chapter_1": 10,
        "macguffin_chapter_2": 10,
        "macguffin_chapter_3": 10,
        "macguffin_chapter_4": 10,
        "macguffin_extra": 0,
        "randomize_secret_bosses": "mandatory",
        "randomize_mantle": "true",
        "exclude_t_rank": False,
        "exclude_z_rank": False,
        "include_hidden_items": True,
        "include_unused_items": "true",
        "death_link": True,
        "filler_healing_weight": "random",
        "filler_currency_weight": "random",
        "trap_weight": "random",
        "filler_armor_weight": "random",
        "filler_tension_weight": "random",
        "filler_smile_weight": "random",
        "unlock_characters": "true",
        "include_mike": "battle_and_games",
        "chapter_1_recruit": True,
    }
}
