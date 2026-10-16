from __future__ import annotations

from dataclasses import dataclass

from Options import (
    Accessibility,
    Choice,
    FreeText,
    OptionGroup,
    OptionDict,
    PerGameCommonOptions,
    ProgressionBalancing,
    Range,
    StartInventoryPool,
    Toggle,
    Visibility,
)

from .minor_families import (
    MINOR_FAMILY_KEYS,
    MINOR_FAMILY_OPTION_BY_KEY,
)


class GameMode(Choice):
    """
    Choose Classic or Steel Soul. Steel Soul changes some checks and ends the save on death.
    """

    display_name = "Game Mode"
    option_classic = 0
    option_steel_soul = 1
    default = option_classic


class GlobalRandomization(Choice):
    """
    Keep a category vanilla or mix it into the global pool.
    """

    option_vanilla = 0
    alias_off = 0
    option_anywhere = 1
    default = option_anywhere


class SkillRandomization(GlobalRandomization):
    """
    Randomizes the 8 traversal skills in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Skill Randomization"


class ToolRandomization(GlobalRandomization):
    """
    Randomizes tools other than Compass in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Tool Randomization"


class QuillRandomization(GlobalRandomization):
    """
    Keep Quill at Shakra's shop or mix it into the global item pool.

    Independent of Skill Randomization. Start Fully Mapped removes the need for Quill.
    """

    display_name = "Quill Randomization"


class CompassRandomization(GlobalRandomization):
    """
    Keep Compass at Shakra's shop or mix it into the global item pool.

    Independent of Tool Randomization. Automatic Compass supplies the position marker without the tool.
    """

    display_name = "Compass Randomization"


class SilkSkillRandomization(GlobalRandomization):
    """
    Randomizes the 6 Silk Skills in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Silk Skill Randomization"


class SilkSoarBegone(Toggle):
    """
    Removes Silk Soar from runs without Act 3 areas. When Act 3 areas are included,
    Silk Soar stays at its vanilla shrine, even with skill randomization enabled.
    """

    display_name = "Silk Soar Begone"


class CrestRandomization(GlobalRandomization):
    """
    Randomizes the 7 Crests in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Crest Randomization"


class EvaRandomization(GlobalRandomization):
    """
    Randomizes Eva's two Hunter evolutions, two Vesticrests and Sylphsong.

    vanilla: Eva gives her normal rewards
    anywhere: mixes her rewards into the global item pool
    """

    display_name = "Eva Randomization"
    default = GlobalRandomization.option_vanilla


class SoulRandomization(GlobalRandomization):
    """
    Randomizes Maiden Soul, Hermit Soul and Seeker Soul for Act 2, Cursed and Act 3 goals.
    """

    display_name = "Soul Randomization"
    default = GlobalRandomization.option_vanilla


class OldHeartRandomization(GlobalRandomization):
    """
    Randomizes Pollen Heart, Hunter's Heart and Encrusted Heart for the Act 3 goal. 
    Conjoined Heart stays vanilla.
    """

    display_name = "Old Heart Randomization"
    default = GlobalRandomization.option_vanilla


class MementoRandomization(GlobalRandomization):
    """
    Randomizes Mementos available for your goal. 
    Hunter's Memento stays vanilla. Hearts follow Old Heart Randomization.
    """

    display_name = "Memento Randomization"
    default = GlobalRandomization.option_vanilla


class EverbloomRandomization(GlobalRandomization):
    """
    Randomizes Everbloom for Act 3 goals. 
    The final Abyss route still requires the three-heart ritual and Red Memory to be completed.
    """

    display_name = "Everbloom Randomization"
    default = GlobalRandomization.option_vanilla


class TwistedBudRandomization(GlobalRandomization):
    """
    Randomizes Twisted Bud.
    """

    display_name = "Twisted Bud Randomization"
    default = GlobalRandomization.option_vanilla


class FleaRandomization(GlobalRandomization):
    """
    Randomizes the 30 Fleas in the game, including Kratt, Vog and the Huge Flea.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Flea Randomization"


class CrestSlotRandomization(GlobalRandomization):
    """
    Randomizes the 20 Crest Slots in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool

    If needed, filler rewards become extra Memory Lockets so every randomized
    slot has enough Lockets available. Native pickups stay unchanged.
    """

    display_name = "Crest Slot Randomization"


class MaskShardRandomization(GlobalRandomization):
    """
    Randomizes the 20 Mask Shards in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Mask Shard Randomization"


class SpoolFragmentRandomization(GlobalRandomization):
    """
    Randomizes the 18 Spool Fragments in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Spool Fragment Randomization"


class SilkHeartRandomization(GlobalRandomization):
    """
    Randomizes the 3 Silk Hearts in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Silk Heart Randomization"


class SilkHeartLogic(Toggle):
    """
    Places logical routes for abilities that require silk behind the
    acquisition of at least one Silk Heart. These include Needolin,
    Clawline and Silk Soar.

    Turning this option off may cause more frequent soft locks as you
    may get stuck in a location where you can't get more silk.
    """

    display_name = "Silk Heart Logic"
    default = 1


class BellwayRandomization(GlobalRandomization):
    """
    Randomizes the 10 Bellways in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Bellway Randomization"


class VentricaRandomization(GlobalRandomization):
    """
    Randomizes the 6 Ventricas in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Ventrica Randomization"


class MapRandomization(GlobalRandomization):
    """
    Randomizes the 28 Maps in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Map Randomization"


class MelodyRandomization(GlobalRandomization):
    """
    Randomizes the 5 Melodies in the game: 
    the three required to finish Act 2, 
    Beastling Call and Elegy of the Deep.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Melody Randomization"


class PinRandomization(GlobalRandomization):
    """
    Randomizes the 4 map-pin types in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Pin Randomization"


class RelicRandomization(GlobalRandomization):
    """
    Randomizes the 21 Relics in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Relic Randomization"


class CraftingKitRandomization(GlobalRandomization):
    """
    Randomizes the 4 Crafting Kits in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Crafting Kit Randomization"


class ToolPouchRandomization(GlobalRandomization):
    """
    Randomizes the 4 Tool Pouch upgrades in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Tool Pouch Randomization"


class LoreTabletRandomization(GlobalRandomization):
    """
    Randomizes the 38 Lore Tablets in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Lore Tablet Randomization"
    default = GlobalRandomization.option_vanilla


class RepeatedCollectibleRandomization(GlobalRandomization):
    """
    Randomize a repeated consumable family globally or leave it vanilla.
    """

    default = GlobalRandomization.option_vanilla


class MemoryLocketRandomization(RepeatedCollectibleRandomization):
    """
    Randomizes the 20 Memory Lockets in the game.

    If Crest Slots are randomized, using a Memory Locket will not unlock the
    slot for use, but whatever took its place in that slot remains its AP check.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Memory Locket Randomization"


class CraftmetalRandomization(RepeatedCollectibleRandomization):
    """
    Randomizes the 8 Craftmetals in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Craftmetal Randomization"


class MossberryRandomization(RepeatedCollectibleRandomization):
    """
    Randomizes the 7 Mossberries in the game. 

    Three are required for the Moss Druid's quest, 
    while giving her the remaining four earns another check.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Mossberry Randomization"


class PollipHeartRandomization(RepeatedCollectibleRandomization):
    """
    Randomizes the 6 finite Pollip Hearts in the game. 

    They are required for Greyroot's quest in Shellwood.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Pollip Heart Randomization"
    default = GlobalRandomization.option_vanilla


class SilkeaterRandomization(RepeatedCollectibleRandomization):
    """
    Randomizes the 9 Silkeaters in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Silkeater Randomization"


class MajorKeyRandomization(GlobalRandomization):
    """
    Randomizes Key of Apostate, White Key, Surgeon's Key, Architect's Key and Craw Summons.

    Key of Heretic and Key of Indolent remain at their vanilla locations until
    logic for the Slab is finished.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Major Key Randomization"
    default = GlobalRandomization.option_vanilla


class DivingBellKeyRandomization(Toggle):
    """
    Adds a Diving Bell Key to the item pool. Repairing the Diving Bell requires
    this key as well as accepting the shaman's The Dark Below quest.
    """

    display_name = "Diving Bell Key Randomization"


class SimpleKeyRandomization(Choice):
    """
    Randomize four destination-specific keys without fungible spending.

    anywhere: mixes them into the global item pool
    shuffle: mixes them up between one another
    """

    option_anywhere = GlobalRandomization.option_anywhere
    option_shuffle = 2
    default = option_anywhere
    display_name = "Simple Key Randomization"


class MinorFamilyRandomization(RepeatedCollectibleRandomization):
    """
    Choose how this minor pickup family participates in the seed.
    """


class MinorCacheRandomization(GlobalRandomization):
    """
    Choose how a cache family with varied amounts joins the seed.
    """

    default = GlobalRandomization.option_vanilla


class FrayedRosaryStringRandomization(MinorFamilyRandomization):
    """
    Randomizes the 19 Frayed Rosary Strings in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Frayed Rosary String Randomization"


class RosaryStringRandomization(MinorFamilyRandomization):
    """
    Randomizes the 4 Rosary Strings in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Rosary String Randomization"


class RosaryNecklaceRandomization(MinorFamilyRandomization):
    """
    Randomizes Rosary Necklaces, including wish rewards.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Rosary Necklace Randomization"


class HeavyRosaryNecklaceRandomization(MinorFamilyRandomization):
    """
    Randomizes Heavy Rosary Necklaces, including wish rewards and Loddie's second pin challenge.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Heavy Rosary Necklace Randomization"


class PaleRosaryNecklaceRandomization(MinorFamilyRandomization):
    """
    Randomizes the 2 Pale Rosary Necklaces in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Pale Rosary Necklace Randomization"


class ShardBundleRandomization(MinorFamilyRandomization):
    """
    Randomizes the 12 Shard Bundles in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Shard Bundle Randomization"


class BeastShardRandomization(MinorFamilyRandomization):
    """
    Randomizes the 7 Beast Shard upgrades in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Beast Shard Randomization"


class PristineCoreRandomization(MinorFamilyRandomization):
    """
    Randomizes the 2 Pristine Cores in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Pristine Core Randomization"


class RosaryCacheRandomization(MinorCacheRandomization):
    """
    Randomizes the 200 Rosary Caches in the game.

    These are the Rosaries usually seen strung up and out in the open while exploring.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Rosary Cache Randomization"


class ShellShardCacheRandomization(MinorCacheRandomization):
    """
    Randomizes the 153 Shell Shard Caches in the game.

    These are the Shards found in fossils that must be hit several times.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Shell Shard Cache Randomization"


class JournalRandomization(GlobalRandomization):
    """
    Randomizes the Hunter's Journal and boss journal entries.
    Entries that need multiple kills have separate completion checks and items.

    vanilla: keeps the usual journal
    anywhere: mixes journal items into the multiworld
    """

    display_name = "Journal Randomization"
    default = GlobalRandomization.option_vanilla


class BossSanity(GlobalRandomization):
    """
    EXPERIMENTAL FEATURE, should be fine but please don't bring to syncs

    Adds boss checks and replaces their filler with boss credit items.
    Receiving a credit grants that boss's story unlocks.
    Items dropped by bosses follow their own randomization settings.

    Fight difficulty and arena exits stay with the boss you face.
    Act transitions still require their original fights.

    vanilla: keeps the usual boss progression without extra checks
    anywhere: boss credits can appear anywhere in the multiworld
    """

    display_name = "Boss Sanity"
    default = GlobalRandomization.option_vanilla


class BossSouls(Toggle):
    """
    Randomize Boss Souls into the item pool.
    Bosses do not spawn and their respective arenas are not available until their "soul" has been collected. Bosses that have a gauntlet attached to them are the sole requirement for the gauntlet's spawn.
    Example: Groal's Soul makes his boss fight available and the Bilehaven gauntlet available as well.
    """

    display_name = "Boss Souls (Beta)"
    visibility = Visibility.none
    default = 0


class EnemySouls(Toggle):
    """
    Randomize Enemy Souls into the item pool.
    Enemies do not spawn and their respective gauntlets are not available until their "soul" has been collected. Bosses and boss gauntlets are affected by the boss souls option. Killing an enemy for the first time grants a check.
    """
    display_name = "Enemy Souls (Beta)"
    visibility = Visibility.none
    default = 0


class NpcSouls(Toggle):
    """
    Randomize NPC Souls into the item pool.
    NPCs do not spawn until their respective soul has been collected.
    """

    display_name = "NPC Souls (Beta)"
    visibility = Visibility.none
    default = 0


class BellShrineSanity(GlobalRandomization):
    """
    Randomizes the 5 Judge Bell Shrines.
    """

    display_name = "Bell Shrine Sanity"
    default = GlobalRandomization.option_vanilla


class QuestSanity(GlobalRandomization):
    """
    Adds completion checks for wishes without a separately randomized item reward.
    Items earned from bosses and wishes follow their own randomization settings.
    
    vanilla: no additional wish completion checks
    anywhere: fills wish completion checks from the global item pool
    """

    display_name = "Wish-Sanity"
    default = GlobalRandomization.option_vanilla


class ShuffleWishOffers(Toggle):
    """
    EXPERIMENTAL FEATURE, should be fine but please don't bring to syncs

    Shuffles supported wishes between boards and NPCs independently of Wish-Sanity.
    Each wish keeps its tasks and story effects. Linked NPC follow-ups stay with
    their original NPCs.
    """

    display_name = "Shuffle Wish Offers"


class WishPlando(OptionDict):
    """
    Fix which wish an offer gives. Requires Shuffle Wish Offers.
    Use wish names, with the original offer on the left and the wanted wish on the right.
    Example: {"Wish: Berry Picking": "Wish: Final Audience"}
    The remaining offers are shuffled. Assignments that block progression are rejected.
    """

    display_name = "Wish Offer Plando"
    default = {}


CATEGORY_OPTION_BY_LOCATION_CATEGORY: dict[str, str] = {
    "Skill": "skill_randomization",
    "Quill": "quill_randomization",
    "Compass": "compass_randomization",
    "Tool": "tool_randomization",
    "Spell": "silk_skill_randomization",
    "Crest": "crest_randomization",
    "Eva": "eva_randomization",
    "Soul": "soul_randomization",
    "OldHeart": "old_heart_randomization",
    "Everbloom": "everbloom_randomization",
    "Memento": "memento_randomization",
    "TwistedBud": "twisted_bud_randomization",
    "Flea": "flea_randomization",
    "CrestSlot": "crest_slot_randomization",
    "MaskShard": "mask_shard_randomization",
    "SpoolFragment": "spool_fragment_randomization",
    "SilkHeart": "silk_heart_randomization",
    "Bellway": "bellway_randomization",
    "Ventrica": "ventrica_randomization",
    "Map": "map_randomization",
    "NeedleUpgrade": "needle_upgrade_randomization",
    "PaleOil": "pale_oil_randomization",
    "Melody": "melody_randomization",
    "Pin": "pin_randomization",
    "Relic": "relic_randomization",
    "Upgrade": "crafting_kit_randomization",
    "Key": "simple_key_randomization",
    "MemoryLocket": "memory_locket_randomization",
    "Craftmetal": "craftmetal_randomization",
    "Mossberry": "mossberry_randomization",
    "PollipHeart": "pollip_heart_randomization",
    "Silkeater": "silkeater_randomization",
    "MajorKey": "major_key_randomization",
    "ToolPouch": "tool_pouch_randomization",
    "LoreTablet": "lore_tablet_randomization",
    "Boss": "boss_sanity",
    "Journal": "journal_randomization",
    "BellShrine": "bell_shrine_sanity",
    "Quest": "wish_sanity",
}

CATEGORY_MODE_KEY_BY_VALUE: dict[int, str] = {
    GlobalRandomization.option_vanilla: "vanilla",
    GlobalRandomization.option_anywhere: "anywhere",
    SimpleKeyRandomization.option_shuffle: "shuffle",
}


def get_category_mode_value(options, category: str) -> int:
    option_name = CATEGORY_OPTION_BY_LOCATION_CATEGORY[category]
    option = getattr(options, option_name)
    value = int(option.value)
    if (
        value == SimpleKeyRandomization.option_shuffle
        and not hasattr(type(option), "option_shuffle")
    ):
        raise ValueError(f"{option_name} does not support shuffle.")
    return value


def get_category_mode_key(options, category: str) -> str:
    value = get_category_mode_value(options, category)
    try:
        return CATEGORY_MODE_KEY_BY_VALUE[value]
    except KeyError as exc:
        raise ValueError(
            f"Unknown {category} randomization mode value: {value!r}"
        ) from exc


def get_minor_family_mode_key(options, family_key: str) -> str:
    try:
        option_name = MINOR_FAMILY_OPTION_BY_KEY[family_key]
    except KeyError as exc:
        raise ValueError(
            f"Unknown minor pickup family: {family_key!r}"
        ) from exc

    option = getattr(options, option_name)
    if (
        int(option.value) == SimpleKeyRandomization.option_shuffle
        and not hasattr(type(option), "option_shuffle")
    ):
        raise ValueError(f"{option_name} does not support shuffle.")
    key = option.current_key
    if key not in {"vanilla", "anywhere"}:
        raise ValueError(
            f"Unknown {option_name} mode: {key!r}"
        )
    return key


def get_minor_family_modes(options) -> dict[str, str]:
    return {
        family_key: get_minor_family_mode_key(options, family_key)
        for family_key in MINOR_FAMILY_KEYS
    }




def get_aggregate_minor_mode_key(options) -> str:
    modes = tuple(get_minor_family_modes(options).values())
    return "anywhere" if "anywhere" in modes else "vanilla"


class SilksongAccessibility(Accessibility):
    """
    Set rules for reachability of your items/locations.

    **Full:** ensure everything can be reached and acquired.

    **Minimal:** ensure what is needed to reach your goal can be acquired.
    """

    display_name = "Accessibility"
    default = Accessibility.option_full


class Goal(Choice):
    """
    Act 1-3 require beating the chosen act, Cursed Ending is self
    explanatory, Flea Hunt is getting the set amount of fleas and Spelling Bee
    is getting every unique letter in the chosen phrase with Alphabet Rando on.
    """

    display_name = "Goal"
    option_act_1 = 3
    option_act_2 = 0
    option_act_3 = 1
    option_flea_hunt = 2
    option_cursed_ending = 4
    option_spelling_bee = 5
    default = option_act_3


class SpellingBeePhrase(FreeText):
    """
    The word or phrase used by the Spelling Bee goal.

    A-Z letters, spaces, commas, periods, question marks and exclamation marks
    are supported. At least one letter is required. Other characters change the goal to
    Act 2 and do not automatically enable Alphabet Mode.
    """

    display_name = "Spelling Bee Phrase"
    default = "Hornet"


class FleaHuntCount(Range):
    """
    Number of distinct AP Fleas received for Flea Hunt victory.
    """

    display_name = "Flea Hunt Count"
    range_start = 1
    range_end = 30
    default = 30


class StartingLocation(Choice):
    """
    Use the vanilla opening or experimental Bone Bottom start.

    With Ledge Grab randomization, Vanilla uses Bone Bottom instead.
    """

    display_name = "Starting Location"
    option_vanilla = 0
    option_bone_bottom = 1
    default = option_vanilla


class StartingCrest(Choice):
    """
    Choose Hornet's starting Crest when Crests are randomized.

    random selects one of the seven Crests.
    """

    display_name = "Starting Crest"
    option_hunter = 0
    option_wanderer = 1
    option_reaper = 2
    option_beast = 3
    option_architect = 4
    option_witch = 5
    option_shaman = 6
    default = "random"


class ForceNaked(Toggle):
    """
    Start cloakless without a Crest until you find one. Overrides Starting Crest.
    Experimental. Requires Crest Randomization set to anywhere.
    """

    display_name = "Force Naked"
    visibility = Visibility.none
    default = 0


class EarlyDash(Toggle):
    """
    Place Dash early when Skills are randomized.
    """

    display_name = "Early Dash"
    default = 1


class SplitDashAndSprint(Toggle):
    """
    Use separate Sprint and Dash items with Skills set to anywhere.
    """

    display_name = "Split Dash And Sprint"
    default = 0


class LedgegrabAbilityRando(Toggle):
    """
    EXPERIMENTAL FEATURE: Disables Hornets Ledge Grab Ability and must be found as item to acquire that ability, enable at own risk
    """

    display_name = "Ledgegrab Ability Rando"
    default = 0
    visibility = Visibility.none


class SwimAbilityRando(Toggle):
    """
    EXPERIMENTAL FEATURE: Disables Hornets Swim Ability and must be found as item to acquire that ability, enable at own risk
    """

    display_name = "Swim Ability Rando"
    default = 0
    visibility = Visibility.none


class NeedleUpgradeRandomization(GlobalRandomization):
    """
    Randomizes Plinney's four Needle upgrades.

    vanilla: leaves them at Plinney
    anywhere: mixes them into the global item pool
    """

    display_name = "Needle Upgrade Randomization"
    default = GlobalRandomization.option_vanilla


class PaleOilRandomization(GlobalRandomization):
    """
    Randomizes the three Pale Oils in the game.

    vanilla: leaves them where they normally are
    anywhere: mixes them into the global item pool
    """

    display_name = "Pale Oil Randomization"
    default = GlobalRandomization.option_vanilla


class AlphabetMode(Toggle):
    """
    Add Letter A through Letter Z to the item pool and hide unowned letters in game text.

    Text filtering only runs while the game language is English.
    This needs at least 26 randomized filler rewards.
    """

    display_name = "Alphabet Mode"
    default = 0


class TrailsEndRequirement(Choice):
    """
    Choose whether Trail's End uses 14 Shakra map-stock purchases or received maps.
    """

    display_name = "Trail's End Requirement"
    option_shakra_stock = 0
    option_owned_maps = 1
    default = option_shakra_stock


class IndividualRelicTurnIns(Toggle):
    """
    Make Scrounge's 15 relic and Cardinius's 6 cylinder deposits 
    individual AP checks instead of paying Rosaries.
    """

    display_name = "Individual Relic Turn-ins"
    default = 0


class ProficientCombat(Choice):
    """
    Choose the preferred combat requirements settings.

    Off: use the normal combat requirements.
    Goated: lower Needle, DPS and Crafting Kit requirements by one tier and Mask Shard requirements by four fragments.
    Hell: bypass combat requirements including combat movement.
    """

    display_name = "Proficient Combat"
    option_off = 0
    option_goated = 1
    option_hell = 2
    default = option_off


class ProficientMovement(Toggle):
    """
    Increase traversal difficulty by substituting parts of movement 
    requirements for traversal with frame-precise inputs or timings or 
    special usage of movement abilities.
    """

    display_name = "Proficient Movement"
    default = 0


class FleaBrewJumpLogic(Toggle):
    """
    Use Flea Brew's extra jump height to reach ledges and cross gaps.

    Its speed boost for the Weavenest Cindril secret room remains in logic
    with this option disabled.

    Requires Flea Brew and a crest with a usable red tool slot.
    """

    display_name = "Flea Brew Jump Logic"
    default = 0


class TechniqueDifficulty(Choice):
    option_none = 0
    option_easy = 1
    option_moderate = 2
    option_difficult = 3
    default = option_none


class SharpdartLogic(Toggle):
    """
    Use Sharpdart to cross gaps and extend jumps.

    When disabled, traversal never requires Sharpdart.
    """

    display_name = "Sharpdart Logic"
    default = 0


class ScuttlebraceLogic(TechniqueDifficulty):
    """
    Use Scuttlebrace dodges to extend jumps and reach ledges.

    None disables this technique. Higher settings also allow easier uses.
    """

    display_name = "Scuttlebrace Logic"


class HealStallLogic(TechniqueDifficulty):
    """
    Start binding in midair to briefly delay your fall and extend a jump.

    None disables this technique. Higher settings also allow easier uses.
    """

    display_name = "Heal Stall Logic"


class HazardRespawnLogic(TechniqueDifficulty):
    """
    Deliberately touch a hazard to return to a useful respawn point,
    allowing shortcuts across gaps or obstacles.

    None disables this technique. Higher settings also allow easier uses.
    """

    display_name = "Hazard Respawn Logic"


class RedToolStallLogic(TechniqueDifficulty):
    """
    Use Flea Brew, Flintslate, Plasmium Phial or Voltvessels in midair
    to briefly delay your fall and extend a jump.

    None disables these techniques. Higher settings also allow easier uses.
    """

    display_name = "Red Tool Stall Logic"


class DrillCrystalPogoLogic(TechniqueDifficulty):
    """
    Take damage to create a Memory Crystal, then use Delver's Drill
    to gain height from it. Both tools must fit on the same owned crest.

    None disables this technique. Higher settings also allow easier uses.
    """

    display_name = "Drill Crystal Pogo Logic"


class CrestPogoLogic(TechniqueDifficulty):
    """
    Use crest-specific pogo techniques to gain height or extend jumps.
    Covers pogo skips for every crest.

    None disables these techniques. Higher settings also allow easier uses.
    """

    display_name = "Crest Pogo Skip Logic"


class NeedleStrikeLogic(TechniqueDifficulty):
    """
    Use Needle Strike stalls and crest-specific charged attacks
    to delay your fall, extend jumps or gain height.

    None disables these techniques. 

    Higher settings also allow easier uses.
    """

    display_name = "Needle Strike Logic"


class EnemyPogoLogic(TechniqueDifficulty):
    """
    Use enemy pogo tricks to gain height or cross gaps beyond ordinary traversal.

    Normal enemy pogos remain available with this option set to None.

    Higher settings also allow easier tricks.
    """

    display_name = "Enemy Pogo Skip Logic"


class StartWithMaps(Toggle):
    """
    Start with every eligible map.
    """

    display_name = "Start With Maps"
    default = 1


class StartFullyMapped(Toggle):
    """
    Start with the full world map drawn, regardless of map ownership.
    This does not grant map items. Use Start With Maps to receive them.
    """

    display_name = "Start Fully Mapped"
    default = 1


class AutomaticCompass(Toggle):
    """
    Always show Hornet on maps without granting or equipping Compass.
    """

    display_name = "Automatic Compass"
    default = 1


class CheckMapMarkers(Choice):
    """
    Show enabled, unchecked Archipelago checks on the in-game map.
    """

    display_name = "Location Map Markers"
    option_off = 0
    option_mapped_rooms = 1
    option_owned_maps = 2
    option_all = 3
    default = option_all


class RandomizedBellMarkers(Toggle):
    """
    Move the five Grand Gate Bell markers to their randomized local checks.
    """

    display_name = "Randomized Bell Markers"
    default = 1


class RandomizedMelodyMarkers(Toggle):
    """
    Move Threefold Melody markers to their randomized local checks.
    """

    display_name = "Randomized Melody Markers"
    default = 1


class VogAreaHints(Range):
    """
    Number of area reports Vog can sell. Reports count remaining progression
    items for any player without revealing their names and update as you complete checks.
    """

    display_name = "Vog Area Hints"
    range_start = 0
    range_end = 30
    default = 0


class BellwayAccess(Choice):
    """
    Choose whether Bell Beast must be defeated before using Bellways.
    """

    display_name = "Bellway Access"
    option_bell_beast_required = 0
    option_randomized_stations = 1
    default = option_randomized_stations


class EnemyRosaryMultiplier(Choice):
    """
    Multiply Rosaries dropped by defeated enemies only.
    """

    display_name = "Enemy Rosary Multiplier"
    option_x1 = 0
    option_x1_5 = 1
    option_x2 = 2
    option_x3 = 3
    option_x5 = 4
    option_x10 = 5
    default = option_x2


class EnemyShardMultiplier(Choice):
    """
    Multiply Shell Shards dropped by defeated enemies only.
    """

    display_name = "Enemy Shell Shard Multiplier"
    option_x1 = 0
    option_x1_5 = 1
    option_x2 = 2
    option_x3 = 3
    option_x5 = 4
    option_x10 = 5
    default = option_x2


class PurchasePriceRandomization(Choice):
    """
    Choose how one purchase family derives its prices for this seed.
    """

    option_vanilla = 0
    option_free = 1
    option_shuffle = 2
    option_cheap = 3
    option_expensive = 4
    default = option_vanilla


class NormalShopPrices(PurchasePriceRandomization):
    """
    Randomize prices for ShopItem purchases other than maps and pins.
    """

    display_name = "Normal Shop Prices"


class BellwayPrices(PurchasePriceRandomization):
    """
    Randomize prices charged by Bellway toll machines.
    """

    display_name = "Bellway Prices"


class VentricaPrices(PurchasePriceRandomization):
    """
    Randomize prices charged by Ventrica toll machines.
    """

    display_name = "Ventrica Prices"


class BenchPrices(PurchasePriceRandomization):
    """
    Randomize bench unlock tolls and Underworks bench fees.
    """

    display_name = "Bench Prices"


class MiscellaneousPrices(PurchasePriceRandomization):
    """
    Randomize Pilgrim's Rest admission and pin gallery entry fees.
    """

    display_name = "Miscellaneous Prices"


class MapPrices(PurchasePriceRandomization):
    """
    Randomize prices for Shakra's area maps and Citadel map machines.
    """

    display_name = "Map Prices"


class PinPrices(PurchasePriceRandomization):
    """
    Randomize prices for Shakra's permanent map pins.
    """

    display_name = "Pin Prices"


class UpgradePrices(PurchasePriceRandomization):
    """
    Randomize the two paid Needle-upgrade service prices.
    """

    display_name = "Upgrade Prices"


class DonationPrices(PurchasePriceRandomization):
    """
    Randomize Rosary and Shell Shard Wish donation requirements.
    """

    display_name = "Donation Prices"


class VogHintPrices(PurchasePriceRandomization):
    """
    Randomize the price of Vog's area reports.
    """

    display_name = "Vog Hint Prices"


class FasterDialogue(Toggle):
    """
    Speed up ordinary NPC dialogue without skipping conversations.
    """

    display_name = "Faster Dialogue"
    default = 1


class FasterSilkheartAnimation(Toggle):
    """
    Collect boss Silkhearts on contact. 

    False keeps the vanilla pickup animation but skips the dream sequence.
    """

    display_name = "Faster Silkheart Animation"
    default = 0


class DeathLink(Toggle):
    """
    Share deaths with other death link enabled players.
    """

    display_name = "Death Link"
    default = 0


class DeathLinkCocoon(Choice):
    """
    Choose how received DeathLinks affect your death cocoon and Rosaries.

    vanilla: Received DeathLinks replace an existing cocoon and move your
    carried Rosaries into the new cocoon.
    cocoonless: Received DeathLinks leave your carried Rosaries and any
    existing cocoon untouched.
    cocoon: The first received DeathLink can create a normal cocoon. Later
    received DeathLinks leave that cocoon and your carried Rosaries untouched.

    Your own deaths always use the normal game behavior.
    This option has no effect when Death Link is disabled.
    """

    display_name = "Death Link Cocoon"
    option_vanilla = 0
    option_cocoonless = 1
    option_cocoon = 2
    default = 2


class SilkLink(Toggle):
    """
    Share only the base Spool's current Silk with other enabled Silksong players.
    """

    display_name = "Silk Link"
    default = 0


class RosaryLink(Toggle):
    """
    Share loose Rosary gains and costs with other enabled Silksong players.
    """

    display_name = "Rosary Link"
    default = 0


class ShellShardLink(Toggle):
    """
    Share base-pouch Shell Shard gains and costs with enabled Silksong players.
    """

    display_name = "Shell Shard Link"
    default = 0


class KnockbackLink(Toggle):
    """
    Share hit and Stagger Trap knockback with other enabled players.

    Incoming impacts use their direction at normal Stagger Trap strength.
    """

    display_name = "Knockback Link"
    default = 0


class TrapDisguises(Toggle):
    """
    Disguise traps as major items in shops, wishes and crest slots.

    Shop and wish icons are mirrored. Shop and crest-slot names contain small typos.
    """

    display_name = "Trap Disguises"
    default = 1


class TrapPercentage(Range):
    """
    Percent of eligible filler items in the random pool replaced by traps.

    If every trap weight is zero, no traps are added.
    """

    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapWeight(Range):
    """
    Relative trap frequency. Zero disables that trap type.
    """

    range_start = 0
    range_end = 100
    default = 25


class StaggerTrapWeight(TrapWeight):
    """
    Relative frequency of Stagger Traps, zero disables them.

    When staggered, Hornet receives knockback but takes no damage.
    """

    display_name = "Stagger Trap Weight"


class RosarySpillTrapWeight(TrapWeight):
    """
    Relative frequency of Rosary Spill Traps, zero disables them.
    """

    display_name = "Rosary Spill Trap Weight"


class DarknessTrapWeight(TrapWeight):
    """
    Relative frequency of Darkness Traps, zero disables them.

    The screen is darkened to a small area of light around Hornet for 20 seconds.
    """

    display_name = "Darkness Trap Weight"


class CursedCrestTrapWeight(TrapWeight):
    """
    Relative frequency of Cursed Crest Traps, zero disables them.

    Hornet is inflicted with the Cursed Crest for 90 seconds, as if she had done
    the Rite of Rebirth quest with Greyroot.
    """

    display_name = "Cursed Crest Trap Weight"


class MuckmaggotStatusTrapWeight(TrapWeight):
    """
    Relative frequency of Muckmaggot Status Traps, zero disables them.

    Hornet is afflicted with Muckmaggots as if she fell into Bilewater. Binding
    or using a bench removes them.
    """

    display_name = "Muckmaggot Status Trap Weight"


class NakedTrapWeight(TrapWeight):
    """
    Relative frequency of 90-second Naked Traps, zero disables them.

    Hornet is left naked as if she were in the Slab escape sequence for 90 seconds.
    """

    display_name = "Naked Trap Weight"


class LiteracyTrapWeight(TrapWeight):
    """
    Relative frequency of Literacy Traps, zero disables them.

    Interrupts with a randomly selected passage of pre-written text.
    Advance each dialogue box to regain control while the action continues around you.
    """

    display_name = "Literacy Trap Weight"

class ShaderTrapWeight(TrapWeight):
    """
    Relative frequency of Shader Traps, zero disables them.

    Applies a shader to the game camera with the potential shaders:
    Oil Painting, Grayscale
    """

    display_name = "Shader Trap Weight"


class SilkAndSoulPoints(Range):
    """
    Wish points required for Silk and Soul for the Act 3 goal. Other goals
    keep the vanilla 17-point requirement. Mandatory wishes and story
    requirements remain unchanged. Nuu's wish does not count in logic.
    Values above 23 are treated as 23, or 22 in Steel Soul.
    """
    display_name = "Silk and Soul Points"
    range_start = 0
    range_end = 23
    default = 17

    def __init__(self, value: int):
        super().__init__(min(value, self.range_end))


def get_silk_and_soul_points(options) -> int:
    if getattr(getattr(options, 'goal', None), 'current_key', None) != 'act_3':
        return 17
    maximum = 22 if getattr(getattr(options, 'game_mode', None), 'current_key', None) == 'steel_soul' else SilkAndSoulPoints.range_end
    return max(0, min(maximum, getattr(getattr(options, 'silk_and_soul_points', None), 'value', 17)))


class EntranceRandomization(Choice):
    """
    EXPERIMENTAL FEATURE. Couple room exits with matching directions.
    """
    display_name = "Entrance Randomization (Beta)"
    visibility = Visibility.none
    option_off = 0
    option_coupled = 1
    default = 0


class EntranceRandomizationScope(Choice):
    """
    Choose the coupled entrance pool. Full shuffles all supported connections.
    Interiors shuffles door/interior pairs. Within Areas shuffles connections
    inside each area and leaves area boundaries unchanged.
    """
    display_name = "Entrance Randomization Scope (Beta)"
    visibility = Visibility.none
    option_full = 0
    option_interiors = 1
    option_within_areas = 2
    default = 0


@dataclass
class SilksongOptions(PerGameCommonOptions):
    accessibility: SilksongAccessibility
    game_mode: GameMode
    goal: Goal
    spelling_bee_phrase: SpellingBeePhrase
    flea_hunt_count: FleaHuntCount
    starting_location: StartingLocation
    entrance_randomization: EntranceRandomization
    entrance_randomization_scope: EntranceRandomizationScope
    starting_crest: StartingCrest
    force_naked: ForceNaked
    start_inventory_from_pool: StartInventoryPool
    early_dash: EarlyDash
    split_dash_and_sprint: SplitDashAndSprint
    silk_and_soul_points: SilkAndSoulPoints
    ledgegrab_ability_rando: LedgegrabAbilityRando
    swim_ability_rando: SwimAbilityRando
    trails_end_requirement: TrailsEndRequirement
    enemy_pogo_logic: EnemyPogoLogic
    proficient_combat: ProficientCombat
    proficient_movement: ProficientMovement
    flea_brew_jump_logic: FleaBrewJumpLogic
    red_tool_stall_logic: RedToolStallLogic
    drill_crystal_pogo_logic: DrillCrystalPogoLogic
    crest_pogo_logic: CrestPogoLogic
    needle_strike_logic: NeedleStrikeLogic
    sharpdart_logic: SharpdartLogic
    scuttlebrace_logic: ScuttlebraceLogic
    heal_stall_logic: HealStallLogic
    hazard_respawn_logic: HazardRespawnLogic
    start_with_maps: StartWithMaps
    start_fully_mapped: StartFullyMapped
    automatic_compass: AutomaticCompass
    location_map_markers: CheckMapMarkers
    randomized_bell_markers: RandomizedBellMarkers
    randomized_melody_markers: RandomizedMelodyMarkers
    vog_area_hints: VogAreaHints
    bellway_access: BellwayAccess
    enemy_rosary_multiplier: EnemyRosaryMultiplier
    enemy_shard_multiplier: EnemyShardMultiplier
    normal_shop_prices: NormalShopPrices
    bellway_prices: BellwayPrices
    ventrica_prices: VentricaPrices
    bench_prices: BenchPrices
    miscellaneous_prices: MiscellaneousPrices
    map_prices: MapPrices
    pin_prices: PinPrices
    upgrade_prices: UpgradePrices
    donation_prices: DonationPrices
    vog_hint_prices: VogHintPrices
    faster_dialogue: FasterDialogue
    faster_silkheart_animation: FasterSilkheartAnimation
    quill_randomization: QuillRandomization
    compass_randomization: CompassRandomization
    skill_randomization: SkillRandomization
    tool_randomization: ToolRandomization
    silk_skill_randomization: SilkSkillRandomization
    silk_soar_begone: SilkSoarBegone
    crest_randomization: CrestRandomization
    eva_randomization: EvaRandomization
    soul_randomization: SoulRandomization
    old_heart_randomization: OldHeartRandomization
    everbloom_randomization: EverbloomRandomization
    memento_randomization: MementoRandomization
    twisted_bud_randomization: TwistedBudRandomization
    flea_randomization: FleaRandomization
    crest_slot_randomization: CrestSlotRandomization
    mask_shard_randomization: MaskShardRandomization
    spool_fragment_randomization: SpoolFragmentRandomization
    silk_heart_randomization: SilkHeartRandomization
    silk_heart_logic: SilkHeartLogic
    bellway_randomization: BellwayRandomization
    ventrica_randomization: VentricaRandomization
    map_randomization: MapRandomization
    needle_upgrade_randomization: NeedleUpgradeRandomization
    pale_oil_randomization: PaleOilRandomization
    melody_randomization: MelodyRandomization
    pin_randomization: PinRandomization
    relic_randomization: RelicRandomization
    crafting_kit_randomization: CraftingKitRandomization
    major_key_randomization: MajorKeyRandomization
    simple_key_randomization: SimpleKeyRandomization
    diving_bell_key_randomization: DivingBellKeyRandomization
    memory_locket_randomization: MemoryLocketRandomization
    craftmetal_randomization: CraftmetalRandomization
    mossberry_randomization: MossberryRandomization
    pollip_heart_randomization: PollipHeartRandomization
    silkeater_randomization: SilkeaterRandomization
    tool_pouch_randomization: ToolPouchRandomization
    lore_tablet_randomization: LoreTabletRandomization
    frayed_rosary_string_randomization: FrayedRosaryStringRandomization
    rosary_string_randomization: RosaryStringRandomization
    rosary_necklace_randomization: RosaryNecklaceRandomization
    heavy_rosary_necklace_randomization: HeavyRosaryNecklaceRandomization
    pale_rosary_necklace_randomization: PaleRosaryNecklaceRandomization
    shard_bundle_randomization: ShardBundleRandomization
    beast_shard_randomization: BeastShardRandomization
    pristine_core_randomization: PristineCoreRandomization
    rosary_cache_randomization: RosaryCacheRandomization
    shell_shard_cache_randomization: ShellShardCacheRandomization
    boss_souls: BossSouls
    npc_souls: NpcSouls
    enemy_souls: EnemySouls
    boss_sanity: BossSanity
    journal_randomization: JournalRandomization
    bell_shrine_sanity: BellShrineSanity
    wish_sanity: QuestSanity
    shuffle_wish_offers: ShuffleWishOffers
    wish_plando: WishPlando
    individual_relic_turn_ins: IndividualRelicTurnIns
    death_link: DeathLink
    death_link_cocoon: DeathLinkCocoon
    silk_link: SilkLink
    rosary_link: RosaryLink
    shell_shard_link: ShellShardLink
    knockback_link: KnockbackLink
    alphabet_mode: AlphabetMode
    trap_disguises: TrapDisguises
    trap_percentage: TrapPercentage
    stagger_trap_weight: StaggerTrapWeight
    rosary_spill_trap_weight: RosarySpillTrapWeight
    darkness_trap_weight: DarknessTrapWeight
    cursed_crest_trap_weight: CursedCrestTrapWeight
    muckmaggot_status_trap_weight: MuckmaggotStatusTrapWeight
    naked_trap_weight: NakedTrapWeight
    literacy_trap_weight: LiteracyTrapWeight
    shader_trap_weight: ShaderTrapWeight


silksong_option_groups = [
    OptionGroup("General/Goal Options", [
        ProgressionBalancing,
        SilksongAccessibility,
        GameMode,
        Goal,
        SpellingBeePhrase,
        BellwayAccess,
        FleaHuntCount,
        SilkAndSoulPoints,
        TrailsEndRequirement,
    ], start_collapsed=False),
    OptionGroup("Starting Options", [
        StartingLocation,
        StartingCrest,
        ForceNaked,
        StartWithMaps,
        StartFullyMapped,
        AutomaticCompass,
        CheckMapMarkers,
    ], start_collapsed=False),
    OptionGroup("Proficiency/Skip Options", [
        ProficientMovement,
        ProficientCombat,
        FleaBrewJumpLogic,
        RedToolStallLogic,
        DrillCrystalPogoLogic,
        EnemyPogoLogic,
        CrestPogoLogic,
        NeedleStrikeLogic,
        SharpdartLogic,
        ScuttlebraceLogic,
        HealStallLogic,
        HazardRespawnLogic,
    ], start_collapsed=True),
    OptionGroup("Randomization Options", [
        SplitDashAndSprint,
        RandomizedBellMarkers,
        RandomizedMelodyMarkers,
        QuillRandomization,
        CompassRandomization,
        SkillRandomization,
        ToolRandomization,
        SilkSkillRandomization,
        SilkSoarBegone,
        CrestRandomization,
        EvaRandomization,
        SoulRandomization,
        OldHeartRandomization,
        EverbloomRandomization,
        MementoRandomization,
        TwistedBudRandomization,
        FleaRandomization,
        CrestSlotRandomization,
        MaskShardRandomization,
        SpoolFragmentRandomization,
        SilkHeartRandomization,
        SilkHeartLogic,
        BellwayRandomization,
        VentricaRandomization,
        MapRandomization,
        NeedleUpgradeRandomization,
        PaleOilRandomization,
        MelodyRandomization,
        PinRandomization,
        RelicRandomization,
        CraftingKitRandomization,
        MajorKeyRandomization,
        SimpleKeyRandomization,
        DivingBellKeyRandomization,
        MemoryLocketRandomization,
        CraftmetalRandomization,
        MossberryRandomization,
        PollipHeartRandomization,
        SilkeaterRandomization,
        ToolPouchRandomization,
        LoreTabletRandomization,
        FrayedRosaryStringRandomization,
        RosaryStringRandomization,
        RosaryNecklaceRandomization,
        HeavyRosaryNecklaceRandomization,
        PaleRosaryNecklaceRandomization,
        RosaryCacheRandomization,
        ShardBundleRandomization,
        BeastShardRandomization,
        PristineCoreRandomization,
        ShellShardCacheRandomization,
        JournalRandomization,
        BossSanity,
        BellShrineSanity,
        QuestSanity,
        ShuffleWishOffers,
        WishPlando,
        IndividualRelicTurnIns,
        AlphabetMode,
    ], start_collapsed=True),
    OptionGroup("Costsanity", [
        NormalShopPrices,
        BellwayPrices,
        VentricaPrices,
        BenchPrices,
        MiscellaneousPrices,
        MapPrices,
        PinPrices,
        UpgradePrices,
        DonationPrices,
        VogHintPrices,
    ], start_collapsed=True),
    OptionGroup("BETA Features", [
        LedgegrabAbilityRando,
        SwimAbilityRando,
        EntranceRandomization,
        EntranceRandomizationScope,
    ], start_collapsed=True),
    OptionGroup("Link Options", [
        DeathLink,
        DeathLinkCocoon,
        SilkLink,
        RosaryLink,
        ShellShardLink,
        KnockbackLink,
    ], start_collapsed=True),
    OptionGroup("Miscellaneous", [
        EarlyDash,
        VogAreaHints,
        EnemyRosaryMultiplier,
        EnemyShardMultiplier,
        FasterDialogue,
        FasterSilkheartAnimation,
        TrapDisguises,
        TrapPercentage,
        StaggerTrapWeight,
        RosarySpillTrapWeight,
        DarknessTrapWeight,
        CursedCrestTrapWeight,
        MuckmaggotStatusTrapWeight,
        NakedTrapWeight,
        LiteracyTrapWeight,
        ShaderTrapWeight,
    ], start_collapsed=True),
]
