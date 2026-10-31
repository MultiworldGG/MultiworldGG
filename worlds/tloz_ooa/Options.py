from dataclasses import dataclass

from Options import Choice, OptionDict, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, ItemSet, OptionSet, Accessibility

from .data.Constants import TREES_TABLE

from .common.Options import *

class OracleOfAgesGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Veran: beat the usual final boss
    - Beat Ganon: teleport to the Room of Rites after beating Onox or Veran, then beat Ganon (same as linked game)
    - Collect Maku Seed - Don't Feel like fighting Veran or Ganon to goal? Then don't! (similar to a triforce hunt in ALTTPR)
    """
    display_name = "Goal"

    option_beat_veran = 0
    option_beat_ganon = 1
    option_collect_maku_seed = 2

    default = 0
    include_in_patch = True
    include_in_slot_data = True

class OracleOfAgesRequiredSlates(Range):
    """
    The amount of slate that need to be obtained in order to get to the boss of the eighth dungeons.
    """
    display_name = "Required Slates"
    range_start = 0
    range_end = 4
    default = 4

    include_in_slot_data = True
    include_in_patch = True
    
class OracleOfAgesVasuRings_Enabled(Toggle):
    """
    When enabled, vasu will congradulate you based off of the number of rupees (for Rupee Ring check), and number of enemies defeated (for Slayer's Ring check). 
    """
    display_name = "Vasu Additionnal Rings enabled"

    default = False
    
    include_in_patch = True
    include_in_slot_data = True
    
class OracleOfAgesVasuRings_RupeeCount(Range):
    """
    if Vasu Additionnal Rings enabled, this set the number of rupees you need to collect in order for vasu to give you a check. (from 1 to 9999)
    /!\\ Above 1000, the logic assume that you will need to farm in some capacity as there will certainly not be enough rupees in the pool, so be aware of it before you go beyond that number.
    """
    display_name = "Vasu Rupee Ring Requirement"
    
    range_start = 1
    range_end = 9999
    default = 1000
    
    include_in_patch = True
    include_in_slot_data = True
    
class OracleOfAgesVasuRings_KillCount(Range):
    """
    if Vasu Additionnal Rings enabled, this set the amount of enemies that you need to defeat in order for vasu to give you a check. (from 1 to 1000)
    """
    display_name = "Vasu Slayer Ring Requirement"
    
    range_start = 1
    range_end = 1000
    default = 50
    
    include_in_patch = True
    include_in_slot_data = True

class OracleOfAgesMinibossLocations(Toggle):
    """
    When enabled, all minibosses will have a check that you will need to get each time they are defeated.
    """
    display_name = "Miniboss Locations"

    include_in_patch = True
    include_in_slot_data = True

class OracleOfAgesWarpToStartLocation(Choice):
    """
    This option changes the spot you warp in when you press select or start, A, and B buttons to warp back to the forest of time.
    Please note that depending on the option you select, logic will be affected.
    """
    display_name = "Warp to Start Location"

    option_near_timeportal = 0
    option_near_triforce_stone = 1

    default = 1

    include_in_patch = True
    include_in_slot_data = True


class OracleOfAgesDuplicateSeedTrees(OptionSet):
    """
    The game contains 8 seed trees, but only 5 types of seeds. This means that some types of seeds can appear on
    multiple trees. This setting lets you choose seed trees that will be guaranteed to not hold a unique type of
    seed. You can choose up to 3.
    Regardless of what you choose, each seed type will appear on at most 2 trees.
    Valid choices are:
    - Lynna City
    - Ambi's Palace
    - Deku Forest
    - Symmetry City
    - Crescent Island
    - Rolling Ridge West
    - Rolling Ridge East
    - Zora Village
    """
    display_name = "Duplicate Seed Trees"
    default = {"Crescent Island", "Zora Village", "Rolling Ridge East"}
    valid_keys = {key for key in TREES_TABLE.keys()}

    include_in_patch = True
    include_in_slot_data = True


class OracleOfAgesLinkedHerosCave(Choice):
    """
    Adds linked hero's cave to a list of locations for you to complete. This option also allows you to mark which location the linked hero's cave will be in.
    - Maku Tree Entrance Right Side: A cave will be placed to the right side of the maku tree entrance
    """
    display_name = "Linked Hero's Cave"

    option_disabled = 0
    option_maku_tree_entrance_right_side = 1

    default = 0

    include_in_patch = True
    include_in_slot_data = True


class OracleOfAgesSlateShuffle(Toggle):
    """
    If enabled, Slates can be found anywhere instead of being confined in Dungeon 8.
    """
    display_name = "Slates Outside Dungeon 8"

    include_in_slot_data = True
    include_in_patch = True


class OracleOfAgesEssenceSanity(Toggle):
    """
    If enabled, essences will be shuffled anywhere in the multiworld instead of being guaranteed to be found
    at the end their respective dungeons.
    """
    display_name = "Shuffle Essences"
    include_in_patch = True

# Keeping this for now
class OracleOfAgesPricesFactor(Range):
    """
    A factor (expressed as percentage) that will be applied to all prices inside all shops in the game.
    - Setting it at 10% will make all items almost free
    - Setting it at 500% will make all items horrendously expensive, use at your own risk!
    """
    display_name = "Prices Factor (%)"

    range_start = 10
    range_end = 500
    default = 100

    include_in_slot_data = True
    include_in_patch = True

class OracleOfAgesLynnaGardener(Toggle):
    """
    When enabled, a friendly gardener will have trimmed the bushes outside of Lynna City and cleared the path
    so you don't have to! This will expand the sphere 0 checks to include everything past the bushes that you
    normally would need nothing for.
    It is recommended to have this enabled for multiworlds.
    """
    display_name = "Lynna Gardener"

    include_in_patch = True
    include_in_slot_data = True

class OracleOfAgesEnforcePotionInShop(Choice):
    """
    When enabled, the potion will always be available in the selected shop and will refill.
    WARNING : THIS POTION DOESN'T CURE KING ZORA, you still need to find a specific (blue) potion to cure him
    - disabled : The potion is not available by default, and if it's still in a shop, you can only buy it once
    - lynna_shop : A check will be removed in Lynna City's shop and potions will always be sold here
    - syrup_hut : A check will be removed in Syrup Hut and potions will always be sold here
    """
    display_name = "Potion always available"

    option_disabled = 0
    option_lynna_shop = 1
    option_syrup_hut = 2

    default = 0

    include_in_patch = True
    include_in_slot_data = True
    

class OracleOfAgesEntranceRandomizer(Choice):
    """
    When enabled, entrances in the overworld will lead to a random cave/house/dungeon/etc. picked at generation time.
    - disabled : no entrances are randomized
    - dungeon_only : Only dungeon are randomized with each other.
    - all_entrances : All overworld and dungeon entrances are randomized

    /!\\ DON'T ENABLE THIS IF YOU NEVER RANDOMIZED OR PLAYED THIS GAME BEFORE
    /!\\ The all_entrances option require extensive knowledge of the game to really be enjoyable. 

    /!\\ The dungeon_only is here for you to have a taste of it without being overwhelming.
    /!\\ full ER tend to be quite longer than regular randomized run, as it's quite easy to forget what is where, and
    /!\\ where is what. It is not recommended to enable it when playing with other players without asking for there consent.
    /!\\ Also please, don't activate it in big async (or ever smaller async for that matter) without the organizer's autorization.

    /!\\ You're more likely to get stuck, as some spot can lead to softlocks. You still have the warp to start to unlock you
    /!\\ Please read the FAQ of the game before asking question about being stuck in the game channel (this also apply for normal games...)
    /!\\ It is recommended to play this with the Universal Tracker and with some kind of note to keep track of the important
    /!\\ entrances, because sadly nobody will be mad enough to make a tracker that helps you in this context, and even more so
    /!\\ when rolling ridge is a thing in this game. We hope you know what you're doing. YOU HAVE BEEN WARNED.
    """
    display_name = "Entrances Randomizer (ER)"

    option_disabled = 0
    option_dungeon_only = 1
    option_all_entrances = 2

    default = 0
    include_in_patch = True

class OracleOfAgesEntranceRandomizer_PastPresentPairing(Toggle):
    """
    When ER is set to all entrances and this is enabled, past entrance will be grouped together and randomized 
    with each other instead of being randomized with the present ones, and vice-versa.
    Work with Surface/Underwater Pairing
    """
    display_name = "ER Past/Present Pairing"

    default = False

class OracleOfAgesEntranceRandomizer_SurfaceUnderwaterPairing(Toggle):
    """
    When ER is set to all entrances and this is enabled, underwater entrance will be grouped together and randomized 
    with each other instead of being randomized with the surfaces ones, and vice-versa.
    Work with Past/Present Pairing
    """
    display_name = "ER Surface/Underwater Pairing"

    default = False

class OracleOfAgesEntranceRandomizer_DungeonPairing(Toggle):
    """
    When ER is set to all entrances and this is enabled, dungeon entrances will be grouped together and randomized with each other
    instead of being randomized with the others without taking in consideration Past/Present & Surface/Underwater pairing 
    (i.e. even if Past/Present & Surface/Underwater pairing are enabled, D7 can always pair itself with D8)
    If not enabled, dungeon follow the Past/Present & Surface/Underwater pairing like any other entrances
    """
    display_name = "ER Dungeon/Standard Door Pairing"

    default = False

class OracleOfAgesEntranceRandomizer_SurfaceToUnderwaterFreedom(Toggle):
    """
    When ER is set to all entrances or dungeon only and this is enabled, Link can freely enter surface entrance shuffled with
    underwater entrance without drowning even without the Mermaid Suit, but they can't surface without it.
    If it's not enabled and Link doesn't have the Mermaid Suit, they will drown when trying to warp to an underwater entrance
    """
    display_name = "ER Surface To Underwater Freedom"

    default = False
    include_in_patch = True

class OracleOfAgesEntranceRandomizer_InsideLock(Choice):
    """
    Determine how locked doors / caves / bushes behave when you try to exit them when they are not open with entrance randomization.
    - fully_blocked : you can't exit to a blocked exit if it wasn't open before.
    - conditionnal_block : you can't exit to a blocked exit if you don't have the item required to open that exit. If you do the exit automatically open
    - fully_open : the exit always automatically open if reached from the inside
    NOTE : 
    * Does nothing if ER is fully disabled
    * This doesn't include underwater entrances & symmetry city present. (They will always drown you if you don't have the mermaid suit or saved symettry city)
    * Bombable walls require you to have received bombs or bombchu without the need to use them and same goes for bushes and ember seeds
    * Library present will automatically open only with fully_open (this will open both past & present) and require you to find and open the past exit otherwise 
    * Exit to the cave behind moblin fort without destroying it will still block you in fully_open as it's linked to a location check
    * Exitting Jabu Jabu still require the explicit permission from the king. So even if you cleaned the waters and saved him, you need to find the king to open jabu jabu entrance
    """
    display_name = "ER Inside Lock"
    
    option_fully_blocked = 0
    option_conditionnal_block = 1
    option_fully_open = 2

    default = 1
    include_in_patch = True
    
class OracleOfAgesEntranceRandomizer_ExcludedEntrances(OptionSet):
    """
    Determine entrances that won't be shuffled when ER is enabled
    NOTE : 
    * Also work with dungeon shuffle
    * Does nothing if ER is fully disabled
    * All entrances' names can be found here : https://github.com/josephanimate2021/ArchipelagoOoA/blob/ooa/worlds/tloz_ooa/data/Entrances.py
    * 
    """
    display_name = "ER Excluded Entrance"

    default = [
        # black tower,
        # maku road
    ]

    include_in_patch = True

class OracleOfAgesGashaLocations(Range):
    """
    When set to a non-zero value, planting a Gasha tree on a unique soil gives a deterministic item which is taken
    into account by logic. Once an item has been obtained this way, the soil disappears forever to avoid any chance
    of softlocking by wasting several Gasha Seeds on the same soil.
    The value of this option is the number of items that can be obtained that way, the maximum value expecting you
    to plant a tree on each one of the 16 Gasha spots in the game.
    """
    display_name = "Deterministic Gasha Locations"

    range_start = 0
    range_end = 15

    default = 0
    include_in_patch = True
    include_in_slot_data = True
    
class OracleOfAgesGashaNutKillRequirement(NamedRange):
    """
    This option lets you configure how many kills are required to make a gasha tree grow.
    Using a gasha ring halves this number.
    """

    display_name = "Gasha Nut Requirement"

    range_start = 0
    range_end = 250

    default = 20
    special_range_names = {"vanilla": 40}
    include_in_patch = True


@dataclass
class OracleOfAgesOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: OracleOfAgesGoal
    logic_difficulty: OraclesLogicDifficulty
    death_link: OraclesDeathLink

    # Optional locations
    advance_shop: OraclesAdvanceShop
    deterministic_gasha_locations: OracleOfAgesGashaLocations
    secret_locations: OraclesIncludeSecretLocations
    linked_heros_cave: OracleOfAgesLinkedHerosCave
    miniboss_locations: OracleOfAgesMinibossLocations
    vasu_additional_rings: OracleOfAgesVasuRings_Enabled

    # Essences
    required_essences: OraclesRequiredEssences
    shuffle_essences: OracleOfAgesEssenceSanity
    
    # Overworld layout options
    animal_companion: OraclesAnimalCompanion
    default_seed: OraclesDefaultSeedType
    duplicate_seed_trees: OracleOfAgesDuplicateSeedTrees
    warp_to_start_location: OracleOfAgesWarpToStartLocation
    lynna_gardener: OracleOfAgesLynnaGardener

    # Entrance Randomizer (ER)
    entrance_randomizer: OracleOfAgesEntranceRandomizer
    entrance_randomizer_past_present_pairing: OracleOfAgesEntranceRandomizer_PastPresentPairing
    entrance_randomizer_surface_underwater_pairing: OracleOfAgesEntranceRandomizer_SurfaceUnderwaterPairing
    entrance_randomizer_dungeon_pairing: OracleOfAgesEntranceRandomizer_DungeonPairing
    entrance_randomizer_inside_lock: OracleOfAgesEntranceRandomizer_InsideLock
    entrance_randomizer_excluded_entrances: OracleOfAgesEntranceRandomizer_ExcludedEntrances

    #entrance_randomizer_surface_to_underwater_freedom: OracleOfAgesEntranceRandomizer_SurfaceToUnderwaterFreedom

    # Dungeon Items
    master_keys: OraclesMasterKeys
    keysanity_small_keys: OraclesSmallKeyShuffle
    keysanity_boss_keys: OraclesBossKeyShuffle
    keysanity_maps_compasses: OraclesMapCompassShuffle
    required_slates: OracleOfAgesRequiredSlates
    keysanity_slates: OracleOfAgesSlateShuffle

    # Numeric requirements for some checks / access to regions
    gasha_nut_kill_requirement: OracleOfAgesGashaNutKillRequirement
    vasu_rupee_ring_requirement: OracleOfAgesVasuRings_RupeeCount
    vasu_slayer_ring_requirement: OracleOfAgesVasuRings_KillCount
    
    # Miscellaneous options
    required_rings: OraclesRequiredRings
    excluded_rings: OraclesExcludedRings
    shop_prices_factor: OracleOfAgesPricesFactor
    combat_difficulty: OraclesCombatDifficulty
    enforce_potion_in_shop: OracleOfAgesEnforcePotionInShop
    bird_hint: OraclesBirdHint
