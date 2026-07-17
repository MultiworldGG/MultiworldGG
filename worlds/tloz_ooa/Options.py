from dataclasses import dataclass

from Options import Choice, OptionDict, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, ItemSet, OptionSet, Accessibility

from .data.Constants import TREES_TABLE

from .common.Options import *

class OracleOfAgesGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Veran: beat the usual final boss
    - Beat Ganon: teleport to the Room of Rites after beating Onox or Veran, then beat Ganon (same as linked game)
    - Retrieve Maku Seed - You will have to retrieve the maku seed from the maku tree in order cut straight into the credits scene (similar to a triforce hunt in ALTTPR)
    """
    display_name = "Goal"

    option_beat_veran = 0
    option_beat_ganon = 1

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

class OracleOfAgesVasuRingChecksRequirement(OptionDict):
    """
    When enabled, vasu will congradulate you based off of the number of rupees (for Rupee Ring check), and number of enemies defeated (for Slayer's Ring check). 

    Disable Entirely: Determines whatever or not vasu will give out mutiple checks when the friendship ring check is finished.
    Rupee Requirement for Rupee Ring Check: Determines the amount of rupees that you need to collect in order for vasu to give you a check. (from 1 to 9999)
    Amount of Enemies Defeated for Slayer Ring Check: Determines the amount of enemies that you need to defeat in order for vasu to give you a check. (from 1 to 1000)
    """
    display_name = "Vasu Ring Checks Requirement"

    default = {
        "disable_entirely": True,
        "amount_of_enemies_defeated_for_slayer_ring_check": 50,
        "rupee_requirement_for_rupee_ring_check": 1000,
    }
    
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

    # Essences
    required_essences: OraclesRequiredEssences
    shuffle_essences: OracleOfAgesEssenceSanity
    
    # Overworld layout options
    animal_companion: OraclesAnimalCompanion
    shuffle_dungeons: OraclesDungeonShuffle
    default_seed: OraclesDefaultSeedType
    duplicate_seed_trees: OracleOfAgesDuplicateSeedTrees
    warp_to_start_location: OracleOfAgesWarpToStartLocation
    lynna_gardener: OracleOfAgesLynnaGardener

    # Dungeon Items
    master_keys: OraclesMasterKeys
    keysanity_small_keys: OraclesSmallKeyShuffle
    keysanity_boss_keys: OraclesBossKeyShuffle
    keysanity_maps_compasses: OraclesMapCompassShuffle
    required_slates: OracleOfAgesRequiredSlates
    keysanity_slates: OracleOfAgesSlateShuffle

    # Numeric requirements for some checks / access to regions
    vasu_ring_checks_requirement: OracleOfAgesVasuRingChecksRequirement
    gasha_nut_kill_requirement: OracleOfAgesGashaNutKillRequirement
    
    # Miscellaneous options
    required_rings: OraclesRequiredRings
    excluded_rings: OraclesExcludedRings
    shop_prices_factor: OracleOfAgesPricesFactor
    combat_difficulty: OraclesCombatDifficulty
    enforce_potion_in_shop: OracleOfAgesEnforcePotionInShop
