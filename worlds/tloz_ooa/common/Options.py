from dataclasses import dataclass
from datetime import datetime

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle, StartInventoryPool, \
    ItemDict, ItemsAccessibility, ItemSet, Visibility, OptionGroup, NamedRange
from ..data.Items import ITEMS_DATA


class OraclesGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Vanila Boss: beat the usual final boss (Onox for seasons, Veran for Ages)
    - Beat Ganon: teleport to the Room of Rites after beating Onox or Veran, then beat Ganon (same as linked game)
    - Retrieve Maku Seed - You will have to retrieve the maku seed from the maku tree in order cut straight into the credits scene (similar to a triforce hunt in ALTTPR)
    """
    display_name = "Goal"

    option_beat_vanila_boss = 0
    option_beat_ganon = 1
    option_retrieve_maku_seed = 2

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OraclesLogicDifficulty(Choice):
    """
    The difficulty of the logic used to generate the seed.
    - Casual: expects you to know what you would know when playing the game for the first time
    - Medium: expects you to know well the alternatives on how to do basic things, but won't expect any trick
    - Hard: expects you to know difficult tricks such as bomb jumps
    - Hell: expects you to use tricks and glitches that span over more than a few inputs
    """
    display_name = "Logic Difficulty"

    option_casual = 0
    option_medium = 1
    option_hard = 2
    option_hell = 3

    default = 0
    include_in_slot_data = True


class OraclesRequiredEssences(Range):
    """
    The amount of essences that need to be obtained in order to get the seed from the Maku Tree and be able
    to fight the final boss (depends on Goal Settings)
    """
    display_name = "Required Essences"

    range_start = 0
    range_end = 8

    default = 8
    include_in_patch = True
    include_in_slot_data = True


class OraclesPlacedEssences(Range):
    """
    The amount of essences that will be placed in the world. Removed essences are replaced by filler items instead, and
    if essences are not shuffled, those filler items will be placed on the pedestal where the essence would have been.
    If the value for "Placed Essences" is lower than "Required Essences" (which can happen when using random values
    for both), a new random value is automatically picked in the valid range.
    """
    display_name = "Placed Essences"

    range_start = 0
    range_end = 8

    default = 8


class OraclesAnimalCompanion(Choice):
    """
    Determines which animal companion you can summon using the Flute, as well as the layout of the Natzu region.
    - Ricky: the kangaroo with boxing skills
    - Dimitri: the swimming dinosaur who can eat anything
    - Moosh: the flying blue bear (in seasons, he has a passion for Spring Bananas)
    """
    display_name = "Animal Companion"

    option_ricky = 0
    option_dimitri = 1
    option_moosh = 2

    default = "random"
    include_in_patch = True
    include_in_slot_data = True


class OraclesDefaultSeedType(Choice):
    """
    Determines which of the 5 seed types will be the "default seed type", which is given:
    - when obtaining Seed Satchel
    - when obtaining Slingshot or Seed Shooter
    - by Horon (or Lynna) Seed Tree
    """
    display_name = "Default Seed Type"

    option_ember = 0
    option_scent = 1
    option_pegasus = 2
    option_gale = 3
    option_mystery = 4

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OraclesDungeonShuffle(Toggle):
    """
    If enabled, each dungeon entrance will lead to a random dungeon picked at generation time.
    Otherwise, all dungeon entrances lead to their dungeon as intended.
    """
    display_name = "Shuffle Dungeons"

    include_in_slot_data = True


class OraclesOldMenShuffle(Choice):
    """
    Determine how the Old Men which give or take rupees are handled by the randomizer.
    - Vanilla: Each Old Man gives/takes the amount of rupees it usually does in the base game
    - Shuffled Values: The amount of given/taken rupees are shuffled between Old Men
    - Random Values: Each Old Man will give or take a random amount of rupees
    - Random Positive Values: Each Old Man will give a random amount of rupees, but never make you pay
    - Turn Into Locations: Each Old Man becomes a randomized check, and the total amount of rupees they usually give
      in vanilla is shuffled into the item pool
    """

    display_name = "Rupee Old Men"

    option_vanilla = 0
    option_shuffled_values = 1
    option_random_values = 2
    option_random_positive_values = 3
    option_turn_into_locations = 4

    default = 3
    include_in_patch = True
    include_in_slot_data = True

class OraclesBusinessScrubsShuffle(Toggle):
    """
    This option adds the 4 (Seasons Only) accessible business scrubs (Spool Swamp, Samasa Desert, D2, D4 for Seasons) to the pool of randomized
    locations. Just like any other shop, they ask for rupees in exchange of the randomized item,
    which can only be purchased once.
    Please note that scrubs inside dungeons can hold dungeon items, such as keys.
    """
    display_name = "Shuffle Business Scrubs"

    include_in_patch = True
    include_in_slot_data = True


class OraclesEssenceSanity(Toggle):
    """
    If enabled, essences will be shuffled anywhere in the multiworld instead of being guaranteed to be found
    at the end their respective dungeons.
    """
    display_name = "Shuffle Essences"

    include_in_patch = True
    include_in_slot_data = True


class OraclesExcludeDungeonsWithoutEssence(DefaultOnToggle):
    """
    If enabled, all dungeons whose essence has been removed because of the "Placed Essences" option will be excluded,
    which means you can safely ignore them since they cannot contain an item that is required to complete the seed.
    If "Shuffle Essences" is enabled, this option has no effect.
    Hero's Cave is not considered to be a dungeon for this option, and therefore is never excluded.
    """
    display_name = "Exclude Dungeons Without Essence"


class OraclesShowDungeonsWithMap(DefaultOnToggle):
    """
    If enabled, dungeons will indicate where they are once their corresponding map is obtained
    """
    display_name = "Show Dungeons With Map"

    include_in_patch = True
    include_in_slot_data = True


class OraclesShowDungeonsWithEssence(Choice):
    """
    Determines the condition required to highlight dungeons having an essence on their end pedestal
    (with a sparkle on the in-game map).
    This is especially useful when using "Exclude Dungeons Without Essence" to know which dungeons you can ignore.
    If "Shuffle Essences" is enabled, this option has no effect.
    - Disabled: Dungeons with an essence are never shown on the map
    - With Compass: Dungeons with an essence can only be highlighted after obtaining their Compass
    - Always: Dungeons with an essence are always shown on the map
    """
    # TODO: - With Treasure Map: Dungeons with an essence all become highlighted when you obtain the unique Treasure Map item
    display_name = "Show Dungeons With Essence"

    option_disabled = 0
    option_with_compass = 1
    option_always = 2

    default = 1
    include_in_patch = True
    include_in_slot_data = True


class OraclesMasterKeys(Choice):
    """
    - Disabled: All dungeon keys must be obtained individually, just like in vanilla
    - All Small Keys: Small Keys are replaced by a single Master Key for each dungeon which is capable of opening
      every small keydoor for that dungeon
    - All Dungeon Keys: the Master Key for each dungeon is also capable of opening the boss keydoor,
      removing Boss Keys from the item pool
    Master Keys placement is determined following the "Keysanity (Small Keys)" option.
    """
    display_name = "Master Keys"

    option_disabled = 0
    option_all_small_keys = 1
    option_all_dungeon_keys = 2

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OraclesSmallKeyShuffle(Toggle):
    """
    If enabled, dungeon Small Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Small Keys)"

    include_in_patch = True
    include_in_slot_data = True


class OraclesBossKeyShuffle(Toggle):
    """
    If enabled, dungeon Boss Keys can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Keysanity (Boss Keys)"

    include_in_patch = True
    include_in_slot_data = True


class OraclesMapCompassShuffle(Toggle):
    """
    If enabled, Dungeon Maps and Compasses can be found anywhere instead of being confined in their dungeon of origin.
    """
    display_name = "Maps & Compasses Outside Dungeon"

    include_in_patch = True
    include_in_slot_data = True


class OraclesGashaNutKillRequirement(NamedRange):
    """
    This option lets you configure how many kills are required to make a gasha tree grow.
    Using a gasha ring halves this number.
    """
    display_name = "Gasha Nut Requirement"

    range_start = 0
    range_end = 250

    default = 20
    special_range_names = {
        "vanilla": 40
    }
    include_in_patch = True


class OraclesGashaLocations(Range):
    """
    When set to a non-zero value, planting a Gasha tree on a unique soil gives a deterministic item which is taken
    into account by logic. Once an item has been obtained this way, the soil disappears forever to avoid any chance
    of softlocking by wasting several Gasha Seeds on the same soil.
    The value of this option is the number of items that can be obtained that way, the maximum value expecting you
    to plant a tree on each one of the 16 Gasha spots in the game.
    """
    display_name = "Deterministic Gasha Locations"

    range_start = 0
    range_end = 16

    default = 0
    include_in_patch = True
    include_in_slot_data = True


class OraclesShopPrices(Choice):
    """
    Determine the cost of items found in shops of all sorts (including Business Scrubs. In seasons, this also includes the Subrosian Market):
    - Vanilla: shop items have the same cost as in the base game
    - Free: all shop items can be obtained for free
    - Cheap: shop prices are randomized with an average cost of 50 Rupees
    - Reasonable: shop prices are randomized with an average cost of 100 Rupees
    - Expensive: shop prices are randomized with an average cost of 200 Rupees
    - Outrageous: shop prices are randomized with an average cost of 350 Rupees
    """
    display_name = "Shop Prices"

    option_vanilla = 0
    option_free = 1
    option_cheap = 2
    option_reasonable = 3
    option_expensive = 4
    option_outrageous = 5

    default = 0


class OraclesAdvanceShop(Toggle):
    """
    In the vanilla game, there is a house (northwest of Horon Village in Seasons, and south of the maku tree entrance in Lynna Village for Ages) hosting the secret "Advance Shop" that can only
    be accessed if the game is being played on a Game Boy Advance console.
    If enabled, this option makes this shop always open, adding 3 shop locations to the game (and some rupees to the
    item pool to compensate for the extra purchases that might be required)
    """
    display_name = "Open Advance Shop"

    include_in_patch = True
    include_in_slot_data = True

class OraclesRequiredRings(ItemSet):
    """
    Forces a specified set of rings to appear somewhere in the seed.
    Adding too many rings to this list can cause generation failures.
    List of ring names can be found here: https://zeldawiki.wiki/wiki/Magic_Ring
    """
    display_name = "Required Rings"
    valid_keys = {name for name, idata in ITEMS_DATA.items() if "ring" in idata}


class OraclesExcludedRings(ItemSet):
    """
    Forces a specified set of rings to not appear in the seed.
    List of ring names can be found here: https://zeldawiki.wiki/wiki/Magic_Ring
    """
    display_name = "Excluded Rings"
    default = {name for name, idata in ITEMS_DATA.items() if "ring" in idata and idata["ring"] == "useless"}
    valid_keys = {name for name, idata in ITEMS_DATA.items() if "ring" in idata}


class OraclesEnforcePotionInShop(Toggle):
    """
    When enabled, you are guaranteed to have a renewable Potion for 300 rupees inside Horon Or Lynna shop
    """
    display_name = "Enforce Potion in Shop"

    include_in_patch = True
    include_in_slot_data = True


class OraclesCombatDifficulty(Choice):
    """
    Modifies the damage taken during combat to make this aspect of the game easier or harder depending on the
    type of experience you want to have
    """
    display_name = "Combat Difficulty"

    option_peaceful = 4
    option_easier = 2
    option_vanilla = 0
    option_harder = -2
    option_insane = -4

    default = 0
    include_in_patch = True


class OraclesQuickFlute(DefaultOnToggle):
    """
    When enabled, playing the flute (and harp for ages) will immobilize you during a very small amount of time compared to vanilla game.
    """
    display_name = "Quick Flute"

    include_in_patch = True


class OraclesStartingMapsCompasses(Toggle):
    """
    When enabled, you will start the game with maps and compasses for every dungeon in the game.
    This makes navigation easier and removes those items for the pool, which are replaced with random filler items.
    """
    display_name = "Start with Dungeon Maps & Compasses"

    include_in_patch = True
    include_in_slot_data = True


class OraclesRandomizeAi(Toggle):
    """
    When enabled, enemy AI will be randomized.
    This option is only visible on yamls generated in April.

    ⚠ This option may cause logic issues or unbeatable seeds due to some untested combos caused
    by the high number of possibilities. Some graphical oddities are also to be expected.
    ⚠ Required golden beasts is 0 because you are not guaranteed to get an enemy
    with a golden beast AI that would be counted for the old man
    """
    display_name = "Randomize AI"

    include_in_patch = True
    visibility = Visibility.all if (datetime.now().month == 4) else Visibility.none  # Only visible in april


class OraclesRemoveItemsFromPool(ItemDict):
    """
    Removes specified amount of given items from the item pool, replacing them with random filler items.
    This option has significant chances to break generation if used carelessly, so test your preset several times
    before using it on long generations. Use at your own risk!
    """
    display_name = "Remove Items from Pool"
    verify_item_name = False


class OraclesIncludeCrossItems(Toggle):
    """
    When enabled, adds cross items to both games (For seasons, Cane Of Somaria, Switch Hook, and Seed Shooter will be added. For ages, Roc's Cape, Slingshot, Fool's Ore, and Rod of Seasons will be added)
    ⚠ Requires the Oracles of Ages (If seasons is being played, otherwise Seasons) US ROM on patch. You won't be able to use this setting without it.
    """
    display_name = "Cross Items"
    include_in_patch = True


class OraclesIncludeSecretLocations(Toggle):
    """
    When enabled, add the linked game secrets to the list of locations
    """
    display_name = "Secret Locations"

    include_in_patch = True
    include_in_slot_data = True


class OraclesDeathLink(DeathLink):
    """
    When you die, everyone who enabled death link dies. Of course, the reverse is true too.
    """
    include_in_slot_data = True  # This is for the bizhawk client


class OraclesMoveLink(Toggle):
    """
    When enabled, movement will be linked between games that enabled this option.
    This option is only visible on yamls generated in April.

    ⚠ This option may easily cause softlocks and may cause some issues. Some graphical oddities are also to be expected.
    """
    display_name = "Randomize AI"
    visibility = Visibility.all if (datetime.now().month == 4) else Visibility.none  # Only visible in april

    include_in_slot_data = True  # This is for the bizhawk client

class OraclesBirdHint(Choice):
    """
    Disabled: The Owls and Know-it-all birds say their vanilla text when talked to
    Know-it-all: Enable region hints from the birds in the house next to the advance shop
    Owl: Enable owls to give hints about items from your world
    """
    display_name = "Bird Hint"

    option_disabled = 0b00
    option_know_it_all = 0b01
    option_owl = 0b10
    option_both = 0b11

    default = option_both

    def know_it_all(self) -> bool:
        return bool(self.value & OraclesBirdHint.option_know_it_all)

    def owl(self) -> bool:
        return bool(self.value & OraclesBirdHint.option_owl)