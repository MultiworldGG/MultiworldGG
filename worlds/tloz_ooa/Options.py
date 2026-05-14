from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, ItemSet, OptionSet, Accessibility

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
    The amount of slate that need to be obtained in order to get to the boss of the eigth dungeons.
    """
    display_name = "Required Slates"
    range_start = 0
    range_end = 4
    default = 4

    include_in_slot_data = True
    include_in_patch = True

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


class OracleOfAgesLinkedHerosCave(Choice):
    """
    Adds linked hero's cave to a list of locations for you to complete. This option also allows you to mark which location the linked hero's cave will be in.
    - Maku Tree Entrance Right Side: A cave will be placed to the right side of the maku tree entrance, allowing access despite the finished game flag not being set.
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
    """
    display_name = "Lynna Gardener"

    include_in_patch = True
    include_in_slot_data = True

@dataclass
class OracleOfAgesOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: OracleOfAgesGoal
    logic_difficulty: OraclesLogicDifficulty
    required_essences: OraclesRequiredEssences
    required_slates: OracleOfAgesRequiredSlates
    warp_to_start_location: OracleOfAgesWarpToStartLocation
    animal_companion: OraclesAnimalCompanion
    default_seed: OraclesDefaultSeedType
    linked_heros_cave: OracleOfAgesLinkedHerosCave
    duplicate_seed_trees: OracleOfAgesDuplicateSeedTrees
    shuffle_dungeons: OraclesDungeonShuffle
    master_keys: OraclesMasterKeys
    lynna_gardener: OracleOfAgesLynnaGardener
    keysanity_small_keys: OraclesSmallKeyShuffle
    keysanity_boss_keys: OraclesBossKeyShuffle
    keysanity_maps_compasses: OraclesMapCompassShuffle
    keysanity_slates: OracleOfAgesSlateShuffle
    required_rings: OraclesRequiredRings
    excluded_rings: OraclesExcludedRings
    shop_prices_factor: OracleOfAgesPricesFactor
    advance_shop: OraclesAdvanceShop
    combat_difficulty: OraclesCombatDifficulty
    death_link: DeathLink
