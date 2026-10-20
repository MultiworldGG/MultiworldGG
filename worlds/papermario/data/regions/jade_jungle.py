from typing import Dict
import dataclasses

from typing_extensions import override

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    #True_,
    #False_,
    Has,
    HasAll,
    #HasAny,
    #HasAllCounts,
    #HasAnyCount,
    #HasFromList,
    #HasFromListUnique,
    #HasGroup,
    #HasGroupUnique,
    #CanReachLocation,
    #CanReachRegion,
    #CanReachEntrance,
    Rule,
    OptionFilter,
)

from .LogicHelpers import (
    HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    #CanUseAbilityKooper,
    #CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    CanUseAbilityWatt,
    CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

@dataclasses.dataclass()
class SavedAllYoshiKids(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (
            HasAll(
                "RF_SavedYoshiKid_1",
                "RF_SavedYoshiKid_2",
                "RF_SavedYoshiKid_3",
                "RF_SavedYoshiKid_4",
                "RF_SavedYoshiKid_5",
            )
        ).resolve(world)

jade_jungle_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "JJ Whale Cove",
        "area_id": "17",
        "map_id": "0",
        "map_name": "Whale Cove",
        "locations": {
            "JJ Whale Cove Over Flower 1": CanClimbSteps(),
            "JJ Whale Cove Over Flower 2": CanClimbSteps(),
            "JJ Whale Cove Behind Bush": None,
            "JJ Whale Cove In Palm Tree": CanShakeTrees(),
        },
        "exits": {
            "TT Riding the Whale": None,
            "JJ Beach": None,
            "JJ Whale Cove NE Exit": CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ Whale Cove NE Exit",
        "area_id": "17",
        "map_id": "0",
        "map_name": "Whale Cove",
        "exits": {
            "JJ SW Jungle (Super Block) SW": None,
            "JJ Whale Cove": CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ Beach",
        "area_id": "17",
        "map_id": "1",
        "map_name": "Beach",
        "locations": {
            "JJ Beach On The Rocks": CanClimbSteps(),
            "JJ Beach Over Flower 1": CanClimbSteps(),
            "JJ Beach Over Flower 2": CanClimbSteps(),
            "JJ Beach Hidden Block Left": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "JJ Beach Hidden Block Right": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "JJ Beach In Palm Tree 1": CanShakeTrees(),
            "JJ Beach In Palm Tree 2": CanShakeTrees(),
            "JJ Beach In Palm Tree 3": CanShakeTrees(),
            "JJ Beach In Palm Tree 4": CanShakeTrees(),
            "JJ Beach In Palm Tree 5": CanShakeTrees(),
            "JJ Beach In Palm Tree 6 One-Off": CanShakeTrees(),
            "JJ Beach In Palm Tree 6 Replenishing": CanShakeTrees(),
        },
        "exits": {
            "JJ Whale Cove": None,
            "JJ Village Cove": None,
        }
    },
    {
        "region_name": "JJ Village Cove",
        "area_id": "17",
        "map_id": "2",
        "map_name": "Village Cove",
        "events": {
            "RF_YoshiKidsMissing": None,
            "StarPiece_JAN_1": None,
            "StarPiece_JAN_8": None,
        },
        "locations": {
            "JJ Village Cove Hidden Panel": CanFlipPanels(),
            "JJ Village Cove Village Leader Reward": SavedAllYoshiKids(),
            "JJ Village Cove In Palm Tree Left": CanShakeTrees(),
            "JJ Village Cove In Palm Tree Right": CanShakeTrees(),
        },
        "exits": {
            "JJ Beach": None,
            "JJ Village Buildings": None,
        }
    },
    {
        "region_name": "JJ Village Buildings",
        "area_id": "17",
        "map_id": "3",
        "map_name": "Village Buildings",
        "events": {
            "RF_YoshiKidsMissing": None,
            "StarPiece_JAN_1": None,
            "StarPiece_JAN_8": None,
        },
        "locations": {
            "JJ Village Buildings Kolorado Volcano Vase Reward": (
                SavedAllYoshiKids()
                & HasAll("Volcano Vase", "MF_Ch5_RescuedStarSpirit")
            ),
            "JJ Village Buildings Yellow Yoshi Food Reward": (
                SavedAllYoshiKids()
                & HasAll("RF_CanVisitTayceT", "RF_CanCook", "MF_Ch5_RescuedStarSpirit")
            ),
            "JJ Village Buildings Red Yoshi Kid Letter Reward": (
                HasAll("RF_SavedYoshiKid_3", "Letter to Red Yoshi Kid")
                & CanUseAbilityParakarry()
            ),
            "JJ Village Buildings In Palm Tree": CanShakeTrees(),
            "JJ Village Buildings Shop Item 1": CanClimbSteps(),
            "JJ Village Buildings Shop Item 2": CanClimbSteps(),
            "JJ Village Buildings Shop Item 3": CanClimbSteps(),
            "JJ Village Buildings Shop Item 4": CanClimbSteps(),
            "JJ Village Buildings Shop Item 5": CanClimbSteps(),
            "JJ Village Buildings Shop Item 6": CanClimbSteps(),
        },
        "exits": {
            "JJ Village Cove": None,
            "JJ SE Jungle (Quake Hammer) East": None,
            "JJ Path to the Volcano": None,
            "JJ Village Buildings Pipe": Has("GF_TIK08_WarpPipe") & HasBoots(),
        }
    },
    {
        "region_name": "JJ Village Buildings Pipe",
        "area_id": "17",
        "map_id": "3",
        "map_name": "Village Buildings",
        "exits": {
            "TTT Second Level Entry (B2) Blue Pipe": CanReenterVerticalPipes(),
            "JJ Village Buildings": None,
        }
    },
    {
        "region_name": "JJ Sushi Tree",
        "area_id": "17",
        "map_id": "4",
        "map_name": "Sushi Tree",
        "locations": {
            "JJ Sushi Tree In Volcano Chest": Has("MF_Ch5_RescuedStarSpirit"),
            "JJ Sushi Tree On Island": CanUseAbilitySushie(),
            "JJ Sushi Tree In Island Tree": CanShakeTrees() & CanUseAbilitySushie(),
            "JJ Sushi Tree Sushie Partner": CanShakeTrees(),
        },
        "exits": {
            "JJ SE Jungle (Quake Hammer) East": None,
        }
    },
    {
        "region_name": "JJ SE Jungle (Quake Hammer) East",
        "area_id": "17",
        "map_id": "5",
        "map_name": "SE Jungle (Quake Hammer)",
        "locations": {
            "JJ SE Jungle (Quake Hammer) Red Block": CanUseAbilitySushie() & CanHitFloatingBlocks(),
            "JJ SE Jungle (Quake Hammer) Bush (Bottom Right)": None,
            "JJ SE Jungle (Quake Hammer) In Tree (Right)": CanShakeTrees(),
        },
        "exits": {
            "JJ Village Buildings": None,
            "JJ Sushi Tree": None,
            "JJ SW Jungle (Super Block) SW": CanUseAbilitySushie(),
            "JJ SE Jungle (Quake Hammer) West": Has("GF_JAN05_CreateLogBridge"),
        }
    },
    {
        "region_name": "JJ SE Jungle (Quake Hammer) West",
        "area_id": "17",
        "map_id": "5",
        "map_name": "SE Jungle (Quake Hammer)",
        "events": {
            "GF_JAN05_CreateLogBridge": HasHammer(),
            "RF_SavedYoshiKid_1": Has("RF_YoshiKidsMissing") & HasHammer(),
        },
        "locations": {
            "JJ SE Jungle (Quake Hammer) Bush (Bottom Left)": None,
        },
        "exits": {
            "JJ NE Jungle (Raven Statue) South": None,
            "JJ SE Jungle (Quake Hammer) East": Has("GF_JAN05_CreateLogBridge"),
        }
    },
    {
        "region_name": "JJ NE Jungle (Raven Statue) South",
        "area_id": "17",
        "map_id": "6",
        "map_name": "NE Jungle (Raven Statue)",
        "exits": {
            "JJ SE Jungle (Quake Hammer) West": None,
            "JJ NE Jungle (Raven Statue) East": CanUseAbilitySushie(),
            "JJ NE Jungle (Raven Statue) North": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ NE Jungle (Raven Statue) East",
        "area_id": "17",
        "map_id": "6",
        "map_name": "NE Jungle (Raven Statue)",
        "exits": {
            "JJ Small Jungle Ledge": None,
            "JJ NE Jungle (Raven Statue) South": CanUseAbilitySushie(),
            "JJ NE Jungle (Raven Statue) North": CanUseAbilitySushie(),
            "JJ NE Jungle (Raven Statue) West": Has("GF_JAN06_CreateLogBridge"),
        }
    },
    {
        "region_name": "JJ NE Jungle (Raven Statue) North",
        "area_id": "17",
        "map_id": "6",
        "map_name": "NE Jungle (Raven Statue)",
        "locations": {
            "JJ NE Jungle (Raven Statue) In Tree (Top Left)": CanShakeTrees(),
            "JJ NE Jungle (Raven Statue) Underwater": CanUseAbilitySushie(),
        },
        "exits": {
            "JJ Deep Jungle 1": Has("Jade Raven"),
            "JJ NE Jungle (Raven Statue) East": CanUseAbilitySushie(),
            "JJ NE Jungle (Raven Statue) South": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ NE Jungle (Raven Statue) West",
        "area_id": "17",
        "map_id": "6",
        "map_name": "NE Jungle (Raven Statue)",
        "events": {
            "GF_JAN06_CreateLogBridge": HasHammer(),
        },
        "exits": {
            "JJ NW Jungle (Large Ledge) SE": None,
            "JJ NE Jungle (Raven Statue) East": Has("GF_JAN06_CreateLogBridge"),
        }
    },
    {
        "region_name": "JJ Small Jungle Ledge",
        "area_id": "17",
        "map_id": "7",
        "map_name": "Small Jungle Ledge",
        "events": {
            "RF_SavedYoshiKid_2": Has("RF_YoshiKidsMissing"),
        },
        "locations": {
            "JJ Small Jungle Ledge In Tree": CanShakeTrees(),
        },
        "exits": {
            "JJ NE Jungle (Raven Statue) East": None,
        }
    },
    {
        "region_name": "JJ SW Jungle (Super Block) SW",
        "area_id": "17",
        "map_id": "8",
        "map_name": "SW Jungle (Super Block)",
        "events": {
            "RF_SavedYoshiKid_3": Has("RF_YoshiKidsMissing")
        },
        "locations": {
            "JJ SW Jungle (Super Block) Bush (Bottom Left)": None,
        },
        "exits": {
            "JJ Whale Cove NE Exit": None,
            "JJ SW Jungle (Super Block) NE": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ SW Jungle (Super Block) NE",
        "area_id": "17",
        "map_id": "8",
        "map_name": "SW Jungle (Super Block)",
        "locations": {
            "JJ SW Jungle (Super Block) Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "JJ SW Jungle (Super Block) Bush (Top Right)": None,
            "JJ SW Jungle (Super Block) In Tree (Top)": CanShakeTrees(),
            "JJ SW Jungle (Super Block) In Tree (Right)": CanShakeTrees(),
            "JJ SW Jungle (Super Block) Underwater 1": CanUseAbilitySushie(),
            "JJ SW Jungle (Super Block) Underwater 2": CanUseAbilitySushie(),
            "JJ SW Jungle (Super Block) Underwater 3": CanUseAbilitySushie(),
            "JJ SW Jungle (Super Block) In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "JJ NW Jungle (Large Ledge) SE": None,
            "JJ SW Jungle (Super Block) SW": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ NW Jungle (Large Ledge) SE",
        "area_id": "17",
        "map_id": "9",
        "map_name": "NW Jungle (Large Ledge)",
        "locations": {
            "JJ NW Jungle (Large Ledge) Bush 1": None,
            "JJ NW Jungle (Large Ledge) Bush 2": None,
            "JJ NW Jungle (Large Ledge) In Tree Right": CanShakeTrees(),
        },
        "exits": {
            "JJ SW Jungle (Super Block) NE": None,
            "JJ NE Jungle (Raven Statue) West": None,
            "JJ NW Jungle (Large Ledge) NW": CanUseAbilitySushie(),
            "JJ Western Dead End": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ NW Jungle (Large Ledge) NW",
        "area_id": "17",
        "map_id": "9",
        "map_name": "NW Jungle (Large Ledge)",
        "exits": {
            "JJ Western Dead End": CanUseAbilitySushie(),
            "JJ NW Jungle (Large Ledge) SE": CanUseAbilitySushie(),
            "JJ NW Jungle (Large Ledge) Ledge": CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ NW Jungle (Large Ledge) Ledge",
        "area_id": "17",
        "map_id": "9",
        "map_name": "NW Jungle (Large Ledge)",
        "locations": {
            "JJ NW Jungle (Large Ledge) In Tree On Ledge": CanShakeTrees(),
        },
        "exits": {
            "JJ NW Jungle (Large Ledge) Pipe": HasBoots(),
            "JJ NW Jungle (Large Ledge) NW": None,
        }
    },
    {
        "region_name": "JJ NW Jungle (Large Ledge) Pipe",
        "area_id": "17",
        "map_id": "9",
        "map_name": "NW Jungle (Large Ledge)",
        "exits": {
            "JJ Root Cavern": CanReenterVerticalPipes(),
            "JJ NW Jungle (Large Ledge) Ledge": None,
        }
    },
    {
        "region_name": "JJ Western Dead End",
        "area_id": "17",
        "map_id": "10",
        "map_name": "Western Dead End",
        "events": {
            "RF_SavedYoshiKid_4": Has("RF_YoshiKidsMissing") & CanUseAbilitySushie() & HasHammer(),
        },
        "locations": {
            "JJ Western Dead End Underwater": CanUseAbilitySushie(),
        },
        "exits": {
            "JJ NW Jungle (Large Ledge) SE": CanUseAbilitySushie(),
            "JJ NW Jungle (Large Ledge) NW": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "JJ Root Cavern",
        "area_id": "17",
        "map_id": "11",
        "map_name": "Root Cavern",
        "events": {
            "RF_SavedYoshiKid_5": Has("RF_YoshiKidsMissing") & CanUseAbilityWatt() & HasBoots(),
        },
        "exits": {
            "JJ NW Jungle (Large Ledge) Pipe": None,
        }
    },
    {
        "region_name": "JJ Deep Jungle 1",
        "area_id": "17",
        "map_id": "12",
        "map_name": "Deep Jungle 1",
        "locations": {
            "JJ Deep Jungle 1 In Tree (Vine)": HasBoots(),
            "JJ Deep Jungle 1 In Tree (Hit)": CanClimbSteps() & CanShakeTrees(),
            "JJ Deep Jungle 1 Hidden Block": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
        },
        "exits": {
            "JJ NE Jungle (Raven Statue) North": None,
            "JJ Deep Jungle 2 (Block Puzzle)": None,
        }
    },
    {
        "region_name": "JJ Deep Jungle 2 (Block Puzzle)",
        "area_id": "17",
        "map_id": "13",
        "map_name": "Deep Jungle 2 (Block Puzzle)",
        "locations": {
            "JJ Deep Jungle 2 (Block Puzzle) Hidden Block": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
            "JJ Deep Jungle 2 (Block Puzzle) In Tree (Left)": CanShakeTrees(),
        },
        "exits": {
            "JJ Deep Jungle 1": None,
            "JJ Deep Jungle 3": None,
        }
    },
    {
        "region_name": "JJ Deep Jungle 3",
        "area_id": "17",
        "map_id": "14",
        "map_name": "Deep Jungle 3",
        "locations": {
            "JJ Deep Jungle 3 Tree Vine Second Left": HasBoots(),
            "JJ Deep Jungle 3 Tree Vine Far Right": HasBoots(),
        },
        "exits": {
            "JJ Deep Jungle 2 (Block Puzzle)": None,
            "JJ Deep Jungle 4 (Ambush)": HasBoots(),
        }
    },
    {
        "region_name": "JJ Deep Jungle 4 (Ambush)",
        "area_id": "17",
        "map_id": "15",
        "map_name": "Deep Jungle 4 (Ambush)",
        "locations": {
            "JJ Deep Jungle 4 (Ambush) In Tree (Right)": CanShakeTrees(),
            "JJ Deep Jungle 4 (Ambush) Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "JJ Deep Jungle 3": None,
            "JJ Base of Great Tree West": None,
        }
    },
    {
        "region_name": "JJ Base of Great Tree West",
        "area_id": "17",
        "map_id": "16",
        "map_name": "Base of Great Tree",
        "events": {
            "MF_Ch5_RafaelMovedRoot": Has("MF_Ch5_TalkedToRafael"),
        },
        "exits": {
            "JJ Deep Jungle 4 (Ambush)": None,
            "JJ Lower Great Tree Interior Bottom Door": None,
            "JJ Base of Great Tree East": Has("MF_Ch5_TalkedToRafael"),
        }
    },
    {
        "region_name": "JJ Base of Great Tree East",
        "area_id": "17",
        "map_id": "16",
        "map_name": "Base of Great Tree",
        "exits": {
            "JJ Path to the Volcano": None,
            "JJ Base of Great Tree West": None,
        }
    },
    {
        "region_name": "JJ Lower Great Tree Interior Bottom Door",
        "area_id": "17",
        "map_id": "17",
        "map_name": "Lower Great Tree Interior",
        "exits": {
            "JJ Base of Great Tree West": None,
            "JJ Lower Great Tree Interior Upper Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ Lower Great Tree Interior Upper Door",
        "area_id": "17",
        "map_id": "17",
        "map_name": "Lower Great Tree Interior",
        "exits": {
            "JJ Great Tree Vine Ascent": None,
            "JJ Lower Great Tree Interior Bottom Door": None,
        }
    },
    {
        "region_name": "JJ Great Tree Vine Ascent",
        "area_id": "17",
        "map_id": "18",
        "map_name": "Great Tree Vine Ascent",
        "locations": {
            "JJ Great Tree Vine Ascent End Of Vine": None,
        },
        "exits": {
            "JJ Lower Great Tree Interior Upper Door": None,
            "JJ Upper Great Tree Interior Lower Door": None,
        }
    },
    {
        "region_name": "JJ Upper Great Tree Interior Lower Door",
        "area_id": "17",
        "map_id": "19",
        "map_name": "Upper Great Tree Interior",
        "exits": {
            "JJ Great Tree Vine Ascent": None,
            "JJ Upper Great Tree Interior Upper Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ Upper Great Tree Interior Upper Door",
        "area_id": "17",
        "map_id": "19",
        "map_name": "Upper Great Tree Interior",
        "exits": {
            "JJ Great Treetop Roost": None,
            "JJ Upper Great Tree Interior Lower Door": None,
        }
    },
    {
        "region_name": "JJ Path to the Volcano",
        "area_id": "17",
        "map_id": "20",
        "map_name": "Path to the Volcano",
        "events": {
            "MF_Ch5_ZiplineBuilt": Has("MF_Ch5_RafaelMovedRoot"),
            "STARSPIRIT_5": Has("MF_Ch5_FoundEscapeRoute"),
            "STARSPIRIT": Has("MF_Ch5_FoundEscapeRoute"),
            "MF_Ch5_RescuedStarSpirit": Has("MF_Ch5_FoundEscapeRoute"),
        },
        "locations": {
            "JJ Path to the Volcano Raphael Gift": Has("MF_Ch5_RafaelMovedRoot"),
            "JJ Path to the Volcano Behind Tree": None,
        },
        "exits": {
            "JJ Village Buildings": None,
            "JJ Base of Great Tree East": Has("MF_Ch5_RafaelMovedRoot"),
            "JJ Path to the Volcano Entrance": Has("MF_Ch5_ZiplineBuilt") & CanClimbSteps(),
        }
    },
    {
        "region_name": "JJ Path to the Volcano Entrance",
        "area_id": "17",
        "map_id": "20",
        "map_name": "Path to the Volcano",
        "exits": {
            "MLL Volcano Entrance": None,
            "JJ Path to the Volcano": Has("MF_Ch5_ZiplineBuilt"),
        }
    },
    {
        "region_name": "JJ Great Treetop Roost",
        "area_id": "17",
        "map_id": "21",
        "map_name": "Great Treetop Roost",
        "events": {
            "MF_Ch5_TalkedToRafael": None,
        },
        "exits": {
            "JJ Upper Great Tree Interior Upper Door": None,
            "JJ Base of Great Tree West": None,
        }
    }
]
