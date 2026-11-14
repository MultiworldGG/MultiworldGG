import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, OptionSet, DeathLink, PerGameCommonOptions



class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class ExpMultiplierOption(Range):
    """Multiplies stat gain by specified amount"""
    display_name = "Exp Multiplier"
    min_value = 1
    range_start = 1
    range_end = 10
    default = 1

class EnsureEarlyStatCapOption(DefaultOnToggle):
    """Places a Stat Cap in the first properity point location"""
    display_name = "Ensure Early Stat Cap"    

class GoalOption(Choice):
    """Sets the goal for the game"""
    display_name = "Goal"
    default = 0
    option_prosperity = 0
    option_digitamamon = 1   

class RequiredProsperityOption(Range):
    """Sets the required prosperity points to complete the game"""
    display_name = "Required Prosperity Points"
    min_value = 1
    range_start = 1
    range_end = 100
    default = 100

class ProgressiveStatOption(DefaultOnToggle):
    """Enables Progressive Stat gain caps"""
    display_name = "Progressive Stat Caps"

class EasyMonochromonOption(DefaultOnToggle):
    """Always win the Monochromon Minigame"""
    display_name = "Easy Monochromon"
    
class FastDrimogemonOption(DefaultOnToggle):
    """Makes Drimogen dig in 1 day instead of 10"""
    display_name = "Fast Drimogemon"

class IncludeCardLocationsOption(DefaultOnToggle):
    """Include card locations in the randomization pool"""
    display_name = "Include Card Locations"

class TabbedChartOption(DefaultOnToggle):
    """Replace the evolution chart with the tabbed chart that has room for the extra Digimon."""
    display_name = "Tabbed Evolution Chart"


class MegaChartPageOption(DefaultOnToggle):
    """Add a Mega page to the tabbed chart (Machinedramon and other Megas move there).
    Only applies when the tabbed chart is on."""
    display_name = "Mega Chart Page"


ALL_CUSTOM_DIGIMON = frozenset(["snowagumon", "panjyamon", "blackagumon", "metalgreymon_orange", "blackgreymon", "icedevimon", "hyogamon", "dokunemon", "metaletemon", "myotismon", "warumonzaemon", "goburimon", "gotsumon", "flarerizamon", "darkrizamon", "otamamon", "tentomon", "gekomon", "guardromon", "tankmon", "mastertyrannomon", "demimeramon", "machinedramon"])


class ExcludedCustomDigimonOption(OptionSet):
    """Custom Digimon (recolours and NPC forms) to leave OUT of this game. All of them are in by
    default; list the ones you do not want, or "all" to disable every custom Digimon."""
    display_name = "Excluded Custom Digimon"
    valid_keys = ALL_CUSTOM_DIGIMON | {"all"}
    default = frozenset()


class RecruitSoulsOption(DefaultOnToggle):
    """Recruitable Digimon only appear in the world once you have received their Soul item.
    When off, every Soul is pre-granted by the game patch and recruits appear as in vanilla."""
    display_name = "Recruit Souls"



class EnemysanityOption(DefaultOnToggle):
    """Enemysanity: one location per wild Digimon species, checked the first
    time you win a fight against one of them."""
    display_name = "Enemysanity"

class IncludeShopLocationsOption(DefaultOnToggle):
    """Shopsanity: 27 one-time "AP Item" purchases in the item shops (two per shopkeeper), the Gear
    Savanna shop and ShogunGekomon's merit shop."""
    display_name = "Include Shop Locations"

class IncludeChestLocationsOption(DefaultOnToggle):
    """Include chest locations in the randomization pool"""
    display_name = "Include Chest Locations"

class RandomStarterOption(Choice):
    """Randomise the 2 starter digimon options
    Vanilla = Agumon and Gabumon are the starters
    All = Any digimon can be a starter
    Rookie = Only rookie digimon can be a starter"""
    display_name = "Random starter digimon"
    option_vanilla = 0
    option_all = 1
    option_rookie = 2
    default = 2

class RandomTechniqueOption(Choice):
    """Randomise the techniques that digimon learn
    Vanilla = Digimon techniques are unchanged
    Enabled = Techniques are randomised"""
    display_name = "Random techniques"
    option_vanilla = 0
    option_enabled = 1
    default = 1

@dataclass
class DigimonWorldOption(PerGameCommonOptions):
    goal: GoalOption
    early_statcap: EnsureEarlyStatCapOption
    required_prosperity: RequiredProsperityOption
    guaranteed_items: GuaranteedItemsOption
    exp_multiplier: ExpMultiplierOption
    progressive_stats: ProgressiveStatOption
    random_starter: RandomStarterOption
    random_techniques: RandomTechniqueOption
    fast_drimogemon: FastDrimogemonOption
    easy_monochromon: EasyMonochromonOption
    include_card_locations: IncludeCardLocationsOption
    include_chest_locations: IncludeChestLocationsOption
    include_shop_locations: IncludeShopLocationsOption
    enemysanity: EnemysanityOption
    recruit_souls: RecruitSoulsOption
    tabbed_chart: TabbedChartOption
    mega_chart_page: MegaChartPageOption
    excluded_custom_digimon: ExcludedCustomDigimonOption
