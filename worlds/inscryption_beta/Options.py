from dataclasses import dataclass

from schema import Schema, Optional
from Options import Toggle, Choice, DeathLinkMixin, DeathLink, StartInventoryPool, PerGameCommonOptions, DefaultOnToggle, Range, OptionCounter, OptionGroup


class Act1DeathLinkBehaviour(Choice):
    """If DeathLink is enabled, determines what counts as a death in act 1. This affects deaths sent and received.

    - Sacrificed: Send a death when sacrificed by Leshy. Receiving a death will extinguish all candles.

    - Candle Extinguished: Send a death when a candle is extinguished. Receiving a death will extinguish a candle."""
    display_name = "Act 1 Death Link Behaviour"
    option_sacrificed = 0
    option_candle_extinguished = 1
    default = 0


class EnableAct1(DefaultOnToggle):
    """Play Act 1 in the randomizer."""
    display_name = "Enable Act 1"

class EnableAct2(DefaultOnToggle):
    """Play Act 2 in the randomizer."""
    display_name = "Enable Act 2"

class EnableAct3(DefaultOnToggle):
    """Play Act 3 in the randomizer."""
    display_name = "Enable Act 3"


class ActUnlocks(Choice):
    """Defines how acts are unlocked. You can always switch between any unlocked act.

    - Sequential: You start with the first enabled act. After completing an act, you gain access to the next enabled one.

    - Open: Every act is unlocked from the start.

    - Items: You start with a random enabled act. There are "Act 1", "Act 2", and "Act 3" items that unlock other acts."""
    display_name = "Act Unlocks"
    option_sequential = 0
    option_open = 1
    option_items = 2
    default = 0


class StartingAct(Choice):
    """Choose which act to start with.
    This only applies to Act Unlocks: Items, and no other options."""
    display_name = "Starting Act"
    option_act_1 = 0
    option_act_2 = 1
    option_act_3 = 2
    default = 0


class Goal(Choice):
    """Choose how many acts to beat in order to complete the randomizer.
    If you choose a higher number than are enabled, it requires all of them."""
    display_name = "Goal"
    option_one_act = 0
    option_two_acts = 1
    option_all_acts = 2
    default = 2


class RandomizeCodes(Toggle):
    """Randomize codes and passwords in the game (clocks, safes, etc.)"""
    display_name = "Randomize Codes"


class RandomizeDeck(Choice):
    """Randomize cards in your deck into new cards.

    - Disable: Disable the feature.

    - Every Encounter Within Same Type: Randomize cards within the same type every encounter (keep rarity/scrybe type).

    - Every Encounter Any Type: Randomize cards into any possible card every encounter.

    - Starting Only: Only randomize cards given at the beginning of runs and acts."""
    display_name = "Randomize Deck"
    option_disable = 0
    option_every_encounter_within_same_type = 1
    option_every_encounter_any_type = 2
    option_starting_only = 3
    default = 0


class RandomizeSigils(Choice):
    """Randomize sigils printed on the cards into new sigils.

    - Disable: Disable the feature.

    - Randomize Addons: Every encounter, randomize sigils added from sacrifices or other means.

    - Randomize All: Every encounter, randomize all sigils.
    
    - Randomize Once: When a new card is obtained, randomize its sigils. In Act 2, every copy of the same card will have the same randomized sigils."""
    display_name = "Randomize Abilities"
    option_disable = 0
    option_randomize_addons = 1
    option_randomize_all = 2
    option_randomize_once = 3
    default = 0


class ExtraSigils(Toggle):
    """Allow extra sigils to show up in Act 1 and 3.
    These include sigils from other acts, Kaycee's Mod, or just new ones from the same act.
    Some very strong sigils will not show up."""
    display_name = "Extra Sigils"

class RandomizeNodes(Toggle):
    """Some important nodes on the map in Act 1 won't do anything until they're received.
    Logic will expect nodes and challenges for later parts of the map.
    
    This option will add checks for beating every battle on the map."""
    display_name = "Randomize Nodes"


class RandomizeChallenges(Choice):
    """Some Kaycee's Mod Challenges will be enabled by default in Act 1 and need items to remove them.
    Logic will expect nodes and challenges for later parts of the map.
    Also, Grizzly Bosses Challenge has been split into 3 different Progressive Grizzlies,
    and there's additional Tipped Scales Challenges that each tick down your health.

    This option will add checks for trading in each type of pelt to the trader, a check for 
    finishing Act 1, and new consumables in each map area (except the last one) that grant checks.
    There's also 3 free checks scattered around the cabin.
    If Randomize Nodes is disabled, this will also add checks for each battle.
    
    - No Grizzlies: Randomize everything except Grizzly Bosses Challenge, which is disabled."""
    display_name = "Randomize Challenges"
    option_disable = 0
    option_no_grizzlies = 1
    option_randomize = 2
    default = 0


class RandomizeHammer(Choice):
    """Instead of starting with the hammer in Act 2 and 3, it's an item that needs to be found first.

    - Vanilla: Start with the hammer, as normal.

    - Randomize: The hammer needs to be found in the randomizer.

    - Remove: Remove the hammer entirely."""
    display_name = "Randomize Hammer"
    option_vanilla = 0
    option_randomize = 1
    option_remove = 2
    default = 0


class RandomizeShortcuts(Choice):
    """The 3 shortcuts opened by NPCs in Botopia can be randomized, and have locations.

    - Vanilla: You open them normally by talking to the NPCs

    - Randomize: There's items that open the shortcuts, and locations for talking to the NPCs.

    - Open: They start open, and there's still locations for them. For a faster Act 3 experience."""
    display_name = "Randomize Shortcuts"
    option_vanilla = 0
    option_randomize = 1
    option_open = 2
    default = 0


class RandomizeVesselUpgrades(Choice):
    """The 3 Vessel Upgrades from Uberbots and the Conduit Upgrade can be randomized, and have locations.
    These will give your vessels a random beneficial (but not broken) sigil, including those not in the normal options.

    - Vanilla: You gain them normally, by picking them up from bosses.

    - Randomize: Your vessels are upgraded instantly upon receiving a Vessel Upgrade, and there's locations for them.

    - Remove One: Same as randomize, but there's one less upgrade in the pool."""
    display_name = "Randomize Vessel Upgrades"
    option_vanilla = 0
    option_randomize = 1
    option_remove_one = 2
    default = 0


class OptionalDeathCard(Choice):
    """Add a moment after death in act 1 where you can decide to create a death card or not.

    - Disable: Disable the feature.

    - Always On: The choice is always offered after losing all candles.

    - DeathLink Only: The choice is only offered after receiving a DeathLink event."""
    display_name = "Optional Death Card"
    option_disable = 0
    option_always_on = 1
    option_deathlink_only = 2
    default = 2


class SkipTutorial(DefaultOnToggle):
    """Skips the first few tutorial runs of act 1. Bones are available from the start."""
    display_name = "Skip Tutorial"


class SkipEpilogue(Toggle):
    """Completes the goal as soon as the required acts are completed without the need of completing the epilogue."""
    display_name = "Skip Epilogue"


class Act2RandomizeBridge(Choice):
    """Choose whether the bridge in Act 2 should be randomized.

    - Disable: The bridge will require beating one Scrybe, as normal.

    - Enable: The bridge will be repaired upon receiving "Act 2 Bridge Repair".

    - Left Side Start: Like Enable, but you start on the left side of the bridge rather than the right."""
    display_name = "Act 2 Randomize Bridge"
    option_disable = 0
    option_enable = 1
    option_left_side_start = 2
    default = 0


class Act3Overhaul(Toggle):
    """Change up the standard progression of Act 3 in this randomizer to be less linear.
    - Inspectometer Battery will no longer lock you out of the game map,
    and only prevents access to the Foul Backwater area.
    - There'll be an "Act 3 Bridge Repair" item that repairs the bridge.
    - There'll be a "Respledent Bastion Gate" item that unlocks that gate,
    and the satellite dish that normally unlocks it will be a check."""
    display_name = "Act 3 Overhaul"


class EpitaphPiecesRandomization(Choice):
    """Determines how epitaph pieces in act 2 are randomized. This can affect your chances of getting stuck.

    - All Pieces: Randomizes all nine pieces as their own item.

    - In Groups: Randomizes pieces in groups of three.

    - As One Item: Group all nine pieces as a single item."""
    display_name = "Epitaph Pieces Randomization"
    option_all_pieces = 0
    option_in_groups = 1
    option_as_one_item = 2
    default = 0


class PaintingChecksBalancing(Choice):
    """Generation options for the second and third painting checks in act 1.
    If Randomize Nodes or Randomize Challenges are enabled, this has extra logic regardless of the option.
    Force Filler still will work, though.

    - None: Adds no progression logic to these painting checks. They will all count as sphere 1 (early game checks).

    - Balanced: Adds rules to these painting checks. Early game items are less likely to appear into these paintings.

    - Force Filler: For when you dislike doing these last two paintings. Their checks will only contain filler items."""
    display_name = "Painting Checks Balancing"
    option_none = 0
    option_balanced = 1
    option_force_filler = 2
    default = 1


class TrapChance(Range):
    """The probability for each filler item to be replaced with a trap item.
    If you don't want any traps, set this to 0."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0


class TrapTypeWeights(OptionCounter):
    """When a filler item is replaced with a trap, these weights determine the
    odds for each trap type to be selected.
    If you don't want a specific trap type, omit it or set its weight to 0.
    Setting all weights to 0 is the same as setting trap_chance to 0.

    Bleach Trap: All your cards in play lose their sigils.
    Trash Trap: A useless card is added to your deck.
    Deck Size Trap: Increases the Act 2 minimum deck size (which is normally 20) by 1
    Reinforcements Trap: Fills the back row with enemy cards.
    
    Bleach Trap doesn't work in Act 2, and Deck Size Trap is exclusive to Act 2,
    so those won't be generated if relevant acts are disabled."""
    schema = Schema({
        Optional("Bleach Trap"): lambda n: n >= 0,
        Optional("Trash Trap"): lambda n: n >= 0,
        Optional("Deck Size Trap"): lambda n: n >= 0,
        Optional("Reinforcements Trap"): lambda n: n >= 0,
    })
    display_name = "Trap Type Weights"
    default = {
        "Bleach Trap": 2,
        "Trash Trap": 1,
        "Deck Size Trap": 1,
        "Reinforcements Trap": 2
    }


@dataclass
class InscryptionOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    enable_act_1: EnableAct1
    enable_act_2: EnableAct2
    enable_act_3: EnableAct3
    skip_tutorial: SkipTutorial
    skip_epilogue: SkipEpilogue
    act_unlocks: ActUnlocks
    starting_act: StartingAct
    goal: Goal
    death_link: DeathLink
    act1_death_link_behaviour: Act1DeathLinkBehaviour
    optional_death_card: OptionalDeathCard
    randomize_codes: RandomizeCodes
    randomize_deck: RandomizeDeck
    randomize_sigils: RandomizeSigils
    extra_sigils: ExtraSigils
    painting_checks_balancing: PaintingChecksBalancing
    randomize_nodes: RandomizeNodes
    randomize_challenges: RandomizeChallenges
    act2_randomize_bridge: Act2RandomizeBridge
    epitaph_pieces_randomization: EpitaphPiecesRandomization
    randomize_hammer: RandomizeHammer
    act3_overhaul: Act3Overhaul
    randomize_shortcuts: RandomizeShortcuts
    randomize_vessel_upgrades: RandomizeVesselUpgrades
    trap_chance: TrapChance
    trap_type_weights: TrapTypeWeights


inscryption_option_groups = [
    OptionGroup("Item Randomization", [
        PaintingChecksBalancing,
        RandomizeNodes,
        RandomizeChallenges,
        Act2RandomizeBridge,
        EpitaphPiecesRandomization,
        RandomizeHammer,
        Act3Overhaul,
        RandomizeShortcuts,
        RandomizeVesselUpgrades,
    ]),
    OptionGroup("Other Randomization", [
        RandomizeCodes,
        RandomizeDeck,
        RandomizeSigils,
        ExtraSigils,
    ]),
    OptionGroup("Traps", [
        TrapChance,
        TrapTypeWeights,
    ]),
]
