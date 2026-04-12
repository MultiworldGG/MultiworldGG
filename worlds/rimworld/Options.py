import typing
from dataclasses import dataclass
from Options import Option, Choice, PerGameCommonOptions, Range

max_research_locations = 200

class BasicResearchLocationCount(Range):
    """
    The number of basic research locations in the game. These will only require the basic research bench.
    """
    display_name = "Basic Research Location Count"
    range_start = 10
    range_end = max_research_locations
    default = 35

class HiTechResearchLocationCount(Range):
    """
    The number of hi-tech research locations in the game. These will only require the hi-tech research bench (which requires Microelectronics.)
    """
    display_name = "Hi-Tech Research Location Count"
    range_start = 0
    range_end = max_research_locations
    default = 35

class MultiAnalyzerResearchLocationCount(Range):
    """
    The number of multi-analyzer research locations in the game. These will only require the hi-tech research bench and the multi-analyzer (and the research for them.)
    """
    display_name = "Multi-Analyzer Research Location Count"
    range_start = 0
    range_end = max_research_locations
    default = 35

class ResearchBaseCost(Range):
    """
    The amount of research points required to research research locations.
    """
    display_name = "Research Base Cost"
    range_start = 10
    range_end = 8000
    default = 500

class ResearchMaxPrerequisites(Range):
    """
    The max number of prerequisites for the generated Archipelago research. The higher this is, the more restricted your selection of research will be.
    """
    display_name = "Research Max Prerequisites"
    range_start = 0
    range_end = 3
    default = 3

class CraftLocationCount(Range):
    """
    The number of craft locations in the game. These locations require crafting two random items together.
    """
    display_name = "Craft Location Count"
    range_start = 0
    range_end = max_research_locations * 2
    default = 51

class RaidLocationCount(Range):
    """
    The number of raid locations in the game. These locations require defeating a target enemy, one of which will carry a location item in its inventory in each raid.
    """
    display_name = "Raid Location Count"
    range_start = 0
    range_end = max_research_locations * 2
    default = 10

class TradeLocationCount(Range):
    """
    The number of trade locations in the game. These locations require trading with a caravan or settlement for a location item.
    """
    display_name = "Trade Location Count"
    range_start = 0
    range_end = max_research_locations
    default = 10

class RaidTrapCount(Range):
    """
    The guaranteed number of raid traps in the game.
    """
    display_name = "Raid Trap Count"
    range_start = 0
    range_end = 100
    default = 0

class ColonistItemCount(Range):
    """
    The number of colonists that will get sent as items in the game. Note: If you wind up with more than ~20 colonists, you may have performance issues.
    """
    display_name = "Colonist Item Count"
    range_start = 0
    range_end = 50
    default = 5

class PlayerNamesAsColonistItems(Choice):
    """
    If enabled, random player names from the multiworld will be used for colonist nicknames
    """
    display_name = "Use Player Names for Colonist Items"
    option_disabled = 0
    option_enabled = 1
    default = 0

class PercentFillerAsTraps(Range):
    """
    The chance random filler will become trap items, like raids.
    """
    display_name = "Craft Location Count"
    range_start = 0
    range_end = 100
    default = 20

class VictoryCondition(Choice):
    """
    The way to win. Choosing "any" will ensure one of these is considered "in-logic." They also require a "basic" set of research that isn't strictly required to win, so royalty will consider pianos and noble apparel in logic, while anomaly will consider basic bioferrite research in logic. The monument victory condition will require building a room with special archipelago statues and some number of randomized room conditions.
    """
    display_name = "Victory Condition"
    option_any = 0
    option_ship_launch = 1
    option_royalty = 2
    option_archonexus = 3
    option_anomaly = 4
    option_monument = 5
    default = 1

class MonumentStatueCount(Range):
    """
    If the monument victory condition is enabled, this specifies how many Archipelago statues will be required to create a monument and win the game.
    """
    display_name = "Monument Statue Count"
    range_start = 1
    range_end = 30
    default = 5

class ExtraMonumentStatueCount(Range):
    """
    If the monument victory condition is enabled, this specifies how many extra monument statues will be in the pool, allowing the player an easier victory.
    """
    display_name = "Extra Monument Statue Count"
    range_start = 0
    range_end = 30
    default = 0

class MonumentOtherBuildingRequirementCount(Range):
    """
    If the monument victory condition is enabled, this specifies how many non-statue building requirements will be required to create a monument and win the game.
    """
    display_name = "Monument Other Building Requirement Count"
    range_start = 0
    range_end = 20
    default = 5

class MonumentWealthRequirement(Range):
    """
    If the monument victory condition is enabled, this specifies how much wealth is required in the monument room to win.
    """
    range_start = 0
    range_end = 350000
    default = 10000

class RoyaltyEnabled(Choice):
    """
    Enable the Royalty DLC. If you disable any DLC in yaml and enable it in client, all research will be researchable and excluded from the generator.
    """
    display_name = "Royalty Enabled"
    option_disabled = 0
    option_enabled = 1
    default = 1

class IdeologyEnabled(Choice):
    """
    Enable the Ideology DLC. If you disable any DLC in yaml and enable it in client, all research will be researchable and excluded from the generator.
    """
    display_name = "Ideology Enabled"
    option_disabled = 0
    option_enabled = 1
    default = 1

class BiotechEnabled(Choice):
    """
    Enable the Biotech DLC. If you disable any DLC in yaml and enable it in client, all research will be researchable and excluded from the generator.
    """
    display_name = "Biotech Enabled"
    option_disabled = 0
    option_enabled = 1
    default = 1

class AnomalyEnabled(Choice):
    """
    Enable the Anomaly DLC. If you disable any DLC in yaml and enable it in client, all research will be researchable and excluded from the generator.
    """
    display_name = "Anomoly Enabled"
    option_disabled = 0
    option_enabled = 1
    default = 1

class OdysseyEnabled(Choice):
    """
    Enable the Odyssey DLC. If you disable any DLC in yaml and enable it in client, all research will be researchable and excluded from the generator.
    """
    display_name = "Odyssey Enabled"
    option_disabled = 0
    option_enabled = 1
    default = 0

class StartingResearchLevel(Choice):
    """
    If "none" is selected, the player will have access to NO research, regardless of starting scenario. Tribal and Crashlanded will give the player those starting research (regardless of starting scenario.)
    """
    display_name = "Starting Research Level"
    option_none = 0
    option_tribal = 1
    option_crashlanded = 2
    default = 0

class BonusResearchItems(Range):
    """
    How many bonus items will you receive when a research (that unlocks items) is received. For example, if this is set to 2, you may receive a jacket and a flophat when you receive Complex Clothing. If set to -1, you'll receive one of everything, otherwise, you'll receive any number at random (note: This means setting it to higher than 1 may result in getting, say, 5 Harps when you receive Harp.)
    """
    display_name = "Bonus Research Items"
    range_start = -1
    range_end = 10
    default = 0

class ResearchScoutType(Choice):
    """
    How research project scouting works - this will show you what items research projects will send. "None" will show no information for all research. "Summary" options will show the player name and item type (Chris's progressive item). "Fullitem" options will show player name and item name (Chris's progressive item, Master Sword). "Available" options will show only if the research can be started now. "All" options will hint all research.
    """
    option_none = 0
    option_summary_available = 1
    option_fullitem_available = 2
    option_summary_all = 3
    option_fullitem_all = 4
    default = 2

class ResearchScoutSecretTraps(Choice):
    """
    If turned on, the game will lie about scouted trap items. If the scout type shows the player and item name, all traps will be replaced by a random progression item from another player (instead of showing Alex's freeze trap, it will show Chris's Master Sword.) If the scout type only shows item type, it will simply show traps as progression items.
    """
    option_off = 0
    option_on = 1
    default = 0

class NeolithicItemWeight(Range):
    """
    How likely it will be that low/no-tech items are chosen for crafting locations. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Neolithic Item Weight"
    range_start = 0
    range_end = 100
    default = 60

class MedievalItemWeight(Range):
    """
    How likely it will be that low-tech items are chosen for crafting locations. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Medieval Item Weight"
    range_start = 0
    range_end = 100
    default = 60

class IndustrialItemWeight(Range):
    """
    How likely it will be that mid-tech items are chosen for crafting locations. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Industrial Item Weight"
    range_start = 0
    range_end = 100
    default = 30

class SpacerItemWeight(Range):
    """
    How likely it will be that high-tech items are chosen for crafting locations. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Spacer Item Weight"
    range_start = 0
    range_end = 100
    default = 10

class HardToMakeItemWeight(Range):
    """
    How likely it will be that complicated items are chosen for crafting locations. These items usually require specific/unique investment, like multiple advanced components and the like. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Hard To Make Item Weight"
    range_start = 0
    range_end = 100
    default = 1

class AnomalyItemWeight(Range):
    """
    How likely it will be that Anomaly-specific items are chosen for crafting locations. These items will often require bioferrite, and investment into the anomaly expansion to craft. Higher weights make this category more likely. 0 will exempt it from the list. Note that these categories are slightly different than the vanilla "Tech Level," to help account for how challenging they are to craft.
    """
    display_name = "Anomaly Item Weight"
    range_start = 0
    range_end = 100
    default = 10

@dataclass
class RimworldOptions(PerGameCommonOptions):
    BasicResearchLocationCount: BasicResearchLocationCount
    HiTechResearchLocationCount: HiTechResearchLocationCount
    MultiAnalyzerResearchLocationCount: MultiAnalyzerResearchLocationCount
    ResearchBaseCost: ResearchBaseCost
    ResearchMaxPrerequisites: ResearchMaxPrerequisites
    CraftLocationCount: CraftLocationCount
    RaidLocationCount: RaidLocationCount
    TradeLocationCount: TradeLocationCount
    RaidTrapCount: RaidTrapCount
    ColonistItemCount: ColonistItemCount
    PlayerNamesAsColonistItems: PlayerNamesAsColonistItems
    PercentFillerAsTraps: PercentFillerAsTraps
    VictoryCondition: VictoryCondition
    MonumentStatueCount: MonumentStatueCount
    ExtraMonumentStatueCount: ExtraMonumentStatueCount
    MonumentOtherBuildingRequirementCount: MonumentOtherBuildingRequirementCount
    MonumentWealthRequirement: MonumentWealthRequirement
    RoyaltyEnabled: RoyaltyEnabled
    IdeologyEnabled: IdeologyEnabled
    BiotechEnabled: BiotechEnabled
    AnomalyEnabled: AnomalyEnabled
    OdysseyEnabled: OdysseyEnabled
    StartingResearchLevel: StartingResearchLevel
    BonusResearchItems: BonusResearchItems
    ResearchScoutType: ResearchScoutType
    ResearchScoutSecretTraps: ResearchScoutSecretTraps
    NeolithicItemWeight: NeolithicItemWeight
    MedievalItemWeight: MedievalItemWeight
    IndustrialItemWeight: IndustrialItemWeight
    SpacerItemWeight: SpacerItemWeight
    HardToMakeItemWeight: HardToMakeItemWeight
    AnomalyItemWeight: AnomalyItemWeight
    

rimworld_options: typing.Dict[str, type(Option)] = {
    **{
        option.__name__: option
        for option in {
            BasicResearchLocationCount, HiTechResearchLocationCount, MultiAnalyzerResearchLocationCount,
            ResearchBaseCost, ResearchMaxPrerequisites, CraftLocationCount, RaidLocationCount, TradeLocationCount,
            PlayerNamesAsColonistItems, VictoryCondition, RoyaltyEnabled, IdeologyEnabled, BiotechEnabled,
            AnomalyEnabled, OdysseyEnabled, StartingResearchLevel, BonusResearchItems, ResearchScoutType,
            ResearchScoutSecretTraps
        }
    }
}