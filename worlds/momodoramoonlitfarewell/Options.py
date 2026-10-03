from Options import Choice, Toggle, Range, PerGameCommonOptions
from dataclasses import dataclass

class Deathlink(Toggle):
    """Link all player deaths together. If you die, all other players in the session (with Deathlink enabled) also die. This works the same the other way around."""
    display_name = "Deathlink"
    default = 0

class OpenSpringleafPath(Toggle):
    """Remove Demon Strings and Wind Barriers in Springleaf Path to enable entering other areas before getting Awakened Sacred Leaf/Sacred Anemone.\nOther areas with Demon Strings will still require Awakened Sacred Leaf to open them."""
    display_name = "Open Springleaf Path"
    default = 1

class BellHover(Toggle):
    """Consider Bell Hover as a possible strat for world generation.\nBell Hover is done by using the Healing Bell (at most 3 times) when reaching the peak of a jump to gain extra height.\nThis strat is used to access certain areas without having the correct skill (i.e. Demon Frontier without Wall Jump)"""
    display_name = "Bell Hover Generation"
    default: 0

class LunarCrystalBranch(Toggle):
    """Add the Lunar Crystal Branches (the white things that give you money when destroyed) as item location checks."""
    display_name = "Lunar Crystal Branch Shuffle"
    default: 0

class RandomizeKeyItems(Toggle):
    """Add Key Items needed for progression to the randomization pool and as location checks.\nThese items are: Gold Moonlit Dust, Silver Moonlit Dust and Windmill Key."""
    display_name = "Randomize Key items"
    default: 0

class OracleSigil(Toggle):
    """Add the Oracle Sigil to the item pool and as a location check.\nThe Oracle location check requires to free all 30 Lumen Fairies."""
    display_name = "Add Oracle Sigil"
    default = 0

class Companionsanity(Toggle):
    """Add Companions to the item pool and as item location checks.\nNote: Dora and Lineth companions are not locations checks or part of the itempool (coding jank)."""
    display_name = "Companionsanity"
    default = 0

class ProgressiveFinalBossKeys(Toggle):
    """Add 4 progressive keys required to open the door to the Selin boss fight to the randomization pool. \nWith this enabled, it's not required to defeat all four of Selin's Shades to unlock the door."""
    display_name = "Progressive Selin Door Keys"
    default = 0

class ProgressiveDamageUpgrade(Toggle):
    """Add the Heavenly Lilies as item location checks, as well as adding progressive damage upgrade to the itempool."""
    display_name = "Lilysanity"
    default = 0

class ProgressiveBerryUpgrade(Toggle):
    """Add all berry types as item location checks, as well as adding progressive health, magic, stamina and black berry upgrades to the itempool."""
    display_name = "Berrysanity"
    default = 0

class ProgressiveLumenFairies(Toggle):
    """Add the Lumen Fairies as item location checks, as well as adding progressive Lumen Fairies to the itempool\nYou need a total of 30 Lumen Fairies to unlock the Oracle Sigil item or location check."""
    display_name = "Fairysanity"
    default = 0

class VictoryCondition(Choice):
    """Choose which boss must be defeated to be considered as having completed the game."""
    display_name = "Victory Condition"
    option_Moon_God_Selin = 0
    option_Dora = 1
    default = 0
# class FastTravel(Choice):
#     """Whether to start with Fast Travel, add it to the randomization pool, or keep it vanilla (Unlocking Fast Travel is still a location check)"""
#     display_name = "Fast Travel Choice"
#     option_vanilla = 0
#     option_start_with = 1
#     option_add_to_item_pool = 2
#     default = 2

@dataclass
class MomodoraOptions(PerGameCommonOptions):
    Deathlink: Deathlink
    OpenSpringleafPath: OpenSpringleafPath
    BellHoverGeneration: BellHover
    LunarCrystalBranchShuffle: LunarCrystalBranch
    RandomizeKeyItems: RandomizeKeyItems
    OracleSigil: OracleSigil
    Berrysanity: ProgressiveBerryUpgrade
    Lilysanity: ProgressiveDamageUpgrade
    Fairysanity: ProgressiveLumenFairies
    Companionsanity: Companionsanity
    SelinDoorKeysanity: ProgressiveFinalBossKeys
    VictoryCondition: VictoryCondition
    # fast_travel: FastTravel