from typing import Dict
import dataclasses

from typing_extensions import override

from rule_builder.rules import (
    And,
    #Or,
    #AtLeast,
    #True_,
    #False_,
    Has,
    HasAll,
    HasAny,
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
    HasSuperHammer,
    HasUltraHammer,
    HasBoots,
    HasSuperBoots,
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanUseAbilityBow,
    CanUseAbilityWatt,
    CanUseAbilitySushie,
    CanUseAbilityLakilester,
    CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

from ...options import KentCKoopa

@dataclasses.dataclass()
class CanPassKentCKoopa(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        return (
            And(
                Has("STARSPIRIT", count=2),
                (HasBoots() | Has("Goombario")),
                options=[OptionFilter(
                    KentCKoopa,
                    KentCKoopa.option_Must_Defeat
                )],
                filtered_resolution=True,
            )
        ).resolve(world)

koopa_region_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "KR Koopa Village 1",
        "area_id": "6",
        "map_id": "0",
        "map_name": "Koopa Village 1",
        "events": {
            "StarPiece_NOK_1": None,
            "StarPiece_NOK_8": None,
            "RF_RadioTradeEvt1": Has("STARSPIRIT", count=1) & Has("RF_Ch1_Fuzzies_Banished"),
            "RF_RadioTradeEvt2": Has("STARSPIRIT", count=3) & Has("RF_RadioTradeEvt1Done"),
            "RF_RadioTradeEvt3": Has("STARSPIRIT", count=5) & Has("RF_RadioTradeEvt2Done"),
        },
        "locations": {
            "KR Koopa Village 1 Bush Far Left": None,
            "KR Koopa Village 1 Bush Left Front": None,
            "KR Koopa Village 1 Bush Infront Of Tree": None,
            "KR Koopa Village 1 Bush Second From Right": None,
            "KR Koopa Village 1 Bush Second From Left (Koopa Koot Favor)": Has("FAVOR_6_01_active"),
            "KR Koopa Village 1 Bush Far Right (Koopa Koot Favor)": Has("FAVOR_3_01_active"),
            "KR Koopa Village 1 Hidden Panel": CanFlipPanels(),
            "KR Koopa Village 1 Mort T. Letter Reward": CanUseAbilityParakarry() & Has("Letter to Mort T"),
            "KR Koopa Village 1 Koover Letter Reward 1": (
                HasAll("RF_Ch1_Fuzzies_Banished", "Letter to Koover 1")
                & CanUseAbilityParakarry()
            ),
            "KR Koopa Village 1 Koover Letter Reward 2": (
                HasAll("RF_Ch1_Fuzzies_Banished", "Letter to Koover 2")
                & CanUseAbilityParakarry()
            ),
            "KR Koopa Village 1 Shop Item 1": None,
            "KR Koopa Village 1 Shop Item 2": None,
            "KR Koopa Village 1 Shop Item 3": None,
            "KR Koopa Village 1 Shop Item 4": None,
            "KR Koopa Village 1 Shop Item 5": None,
            "KR Koopa Village 1 Shop Item 6": None,
        },
        "exits": {
            "KR Pleasant Crossroads Lower": None,
            "KR Koopa Village 2": None,
        }
    },
    {
        "region_name": "KR Koopa Village 2",
        "area_id": "6",
        "map_id": "1",
        "map_name": "Koopa Village 2",
        "events": {
            "FAVOR_1_01_done": HasAll("Koot Koopa Legends", "RF_Ch1_Fuzzies_Banished"),
            "FAVOR_1_02_done": Has("FAVOR_1_01_done") & HasAny("Sleepy Sheep", "AF_CanMakeSleepySheep"),
            "FAVOR_2_01_done": HasAll("FAVOR_1_02_done", "Koot Tape") & Has("STARSPIRIT", count=1),
            "FAVOR_2_02_done": HasAll("FAVOR_2_01_done", "AF_CanMakeKoopaTea"),
            "FAVOR_2_03_done": HasAll("FAVOR_2_02_done", "Luigi Autograph"),
            "FAVOR_3_01_done": HasAll("FAVOR_2_03_done", "Koot Empty Wallet") & Has("STARSPIRIT", count=2),
            "FAVOR_3_02_done": Has("FAVOR_3_01_done") & HasAny("Tasty Tonic", "AF_CanMakeTastyTonic"),
            "FAVOR_3_03_done": HasAll("FAVOR_3_02_done", "Merluvlee Autograph"),
            "FAVOR_4_01_done": (
                HasAll("FAVOR_3_03_done", "RF_CanReadToadTownNews")
                & Has("STARSPIRIT", count=3)
            ),
            "FAVOR_4_02_done": HasAll("FAVOR_4_01_done", "AF_CanMakeLifeShroom"),
            "FAVOR_4_03_done": HasAll("FAVOR_4_02_done", "AF_CanMakeNuttyCake"),
            "FAVOR_5_01_done": (
                HasAll("FAVOR_4_03_done", "MF_Ch1_RescuedStarSpirit")
                & CanUseAbilityBombette()
                & Has("STARSPIRIT", count=4)
            ),
            "FAVOR_5_02_done": HasAll("FAVOR_5_01_done", "Koot Old Photo"),
            "FAVOR_5_03_done": HasAll("FAVOR_5_02_done", "AF_CanMakeKoopasta"),
            "FAVOR_6_01_done": HasAll("FAVOR_5_03_done", "Koot Glasses") & Has("STARSPIRIT", count=5),
            "FAVOR_6_02_done": HasAll("FAVOR_6_01_done", "Lime"),
            "FAVOR_6_03_done": HasAll("FAVOR_6_02_done", "AF_CanMakeKookyCookie"),
            "FAVOR_7_01_done": HasAll("FAVOR_6_03_done", "Koot Package") & Has("STARSPIRIT", count=6),
            "FAVOR_7_02_done": HasAll("FAVOR_7_01_done", "Coconut"),
            "FAVOR_7_03_done": HasAll("FAVOR_7_02_done", "Koot Red Jar"),
            "FAVOR_1_01_active": Has("RF_Ch1_Fuzzies_Banished"),
            "FAVOR_2_01_active": Has("FAVOR_1_02_done") & Has("STARSPIRIT", count=1),
            "FAVOR_2_03_active": Has("FAVOR_2_02_done"),
            "FAVOR_3_01_active": Has("FAVOR_2_03_done") & Has("STARSPIRIT", count=2),
            "FAVOR_3_03_active": Has("FAVOR_3_02_done"),
            "FAVOR_5_02_active": Has("FAVOR_5_01_done"),
            "FAVOR_6_01_active": Has("FAVOR_5_03_done") & Has("STARSPIRIT", count=5),
            "FAVOR_7_01_active": Has("FAVOR_6_03_done") & Has("STARSPIRIT", count=6),
            "StarPiece_NOK_1": Has("RF_Ch1_Fuzzies_Banished"),
            "StarPiece_NOK_8": Has("RF_Ch1_Fuzzies_Banished"),
        },
        "locations": {
            "KR Koopa Village 2 Kolorado's Wife (Koopa Koot Favor)": Has("RF_Ch1_Fuzzies_Banished"),
            "KR Koopa Village 2 Push Block Puzzle": (
                CanClimbSteps()
                & CanHitFloatingBlocks()
                & Has("RF_Ch1_Fuzzies_Banished")
            ),
            "KR Koopa Village 2 Bush Far Left": None,
            "KR Koopa Village 2 Bush Far Right": None,
            "KR Koopa Village 2 Kooper Partner": Has("Kooper Shell"),
            "KR Koopa Village 2 Kolorado Artifact Reward": (
                Has("Artifact")
                & HasAny("RF_CanVisitDesertCamp", "RF_Ch2_SavedStarSpirit")
                & Has("RF_Ch1_Fuzzies_Banished")
            ),
            "KR Koopa Village 2 Kolorado Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Kolorado")
                & HasAny("RF_CanVisitDesertCamp", "RF_Ch2_SavedStarSpirit")
                & Has("RF_Ch1_Fuzzies_Banished")
            ),
            "KR Koopa Village 2 Koopa Koot Reward 1": Has("FAVOR_1_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 2": Has("FAVOR_1_02_done"),
            "KR Koopa Village 2 Koopa Koot Silver Credit": Has("FAVOR_1_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 3": Has("FAVOR_2_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 4": Has("FAVOR_2_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 5": Has("FAVOR_2_03_done"),
            "KR Koopa Village 2 Koopa Koot Reward 6": Has("FAVOR_3_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 7": Has("FAVOR_3_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 8": Has("FAVOR_3_03_done"),
            "KR Koopa Village 2 Koopa Koot Reward 9": Has("FAVOR_4_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 10": Has("FAVOR_4_02_done"),
            "KR Koopa Village 2 Koopa Koot Gold Credit": Has("FAVOR_4_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 11": Has("FAVOR_4_03_done"),
            "KR Koopa Village 2 Koopa Koot Reward 12": Has("FAVOR_5_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 13": Has("FAVOR_5_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 14": Has("FAVOR_5_03_done"),
            "KR Koopa Village 2 Koopa Koot Reward 15": Has("FAVOR_6_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 16": Has("FAVOR_6_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 17": Has("FAVOR_6_03_done"),
            "KR Koopa Village 2 Koopa Koot Reward 18": Has("FAVOR_7_01_done"),
            "KR Koopa Village 2 Koopa Koot Reward 19": Has("FAVOR_7_02_done"),
            "KR Koopa Village 2 Koopa Koot Reward 20": Has("FAVOR_7_03_done"),
        },
        "exits": {
            "KR Koopa Village 1": None,
            "KR Behind Koopa Village": None,
            "KR Koopa Village 2 Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
        }
    },
    {
        "region_name": "KR Koopa Village 2 Pipe",
        "area_id": "6",
        "map_id": "1",
        "map_name": "Koopa Village 2",
        "exits": {
            "TTT Warp Zone 1 (B1) Koopa Village Pipe": CanReenterVerticalPipes(),
            "KR Koopa Village 2": None,
        }
    },
    {
        "region_name": "KR Behind Koopa Village",
        "area_id": "6",
        "map_id": "2",
        "map_name": "Behind Koopa Village",
        "locations": {
            "KR Behind Koopa Village On Stump": (
                (CanUseAbilityKooper() | CanUseAbilityParakarry())
                & CanClimbSteps()
            ),
        },
        "exits": {
            "KR Koopa Village 2": None,
            "KR Fuzzy Forest": None,
        }
    },
    {
        "region_name": "KR Fuzzy Forest",
        "area_id": "6",
        "map_id": "3",
        "map_name": "Fuzzy Forest",
        "events": {
            "RF_Ch1_Fuzzies_Banished": HasHammer(),
        },
        "locations": {
            "KR Fuzzy Forest Fuzzy Battle Reward": HasHammer(),
        },
        "exits": {
            "KR Behind Koopa Village": None,
        }
    },
    {
        "region_name": "KR Pleasant Path Entry West",
        "area_id": "6",
        "map_id": "4",
        "map_name": "Pleasant Path Entry",
        "exits": {
            "TT Plaza District": None,
            "KR Pleasant Path Entry East": CanPassKentCKoopa(),
        }
    },
    {
        "region_name": "KR Pleasant Path Entry East",
        "area_id": "6",
        "map_id": "4",
        "map_name": "Pleasant Path Entry",
        "locations": {
            "KR Pleasant Path Entry Red Block Center": CanHitFloatingBlocks(),
            "KR Pleasant Path Entry Yellow Block Left": CanHitFloatingBlocks(),
            "KR Pleasant Path Entry Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "KR Pleasant Path Entry West": CanPassKentCKoopa(),
            "KR Pleasant Path Bridge West": None,
        }
    },
    {
        "region_name": "KR Pleasant Path Bridge West",
        "area_id": "6",
        "map_id": "5",
        "map_name": "Pleasant Path Bridge",
        "events": {
            "MF_NOK12_BuiltBridge": CanShakeTrees(),
        },
        "locations": {
            "KR Pleasant Path Bridge Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "KR Pleasant Path Entry East": None,
            "KR Pleasant Path Bridge East": Has("MF_NOK12_BuiltBridge"),
        }
    },
    {
        "region_name": "KR Pleasant Path Bridge East",
        "area_id": "6",
        "map_id": "5",
        "map_name": "Pleasant Path Bridge",
        "locations": {
            "KR Pleasant Path Bridge Kooper Island": CanUseAbilityKooper(),
        },
        "exits": {
            "KR Pleasant Path Bridge West": Has("MF_NOK12_BuiltBridge"),
            "KR Pleasant Path Bridge East Exit": CanClimbSteps(),
        }
    },
    {
        "region_name": "KR Pleasant Path Bridge East Exit",
        "area_id": "6",
        "map_id": "5",
        "map_name": "Pleasant Path Bridge",
        "locations": {
            "KR Pleasant Path Bridge Behind Fence": None,
            "KR Pleasant Path Bridge In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "KR Pleasant Crossroads Upper": None,
            "KR Pleasant Path Bridge East": None,
        }
    },
    {
        "region_name": "KR Pleasant Crossroads Upper",
        "area_id": "6",
        "map_id": "6",
        "map_name": "Pleasant Crossroads",
        "locations": {
            "KR Pleasant Crossroads Hidden Panel": CanFlipPanels(),
            "KR Pleasant Crossroads Behind Peg": None,
        },
        "exits": {
            "KR Pleasant Path Bridge East": None,
            "KR Path to Fortress 1 West Exit": None,
            "KR Pleasant Crossroads Lower": None,
        }
    },
    {
        "region_name": "KR Pleasant Crossroads Lower",
        "area_id": "6",
        "map_id": "6",
        "map_name": "Pleasant Crossroads",
        "locations": {
            "KR Pleasant Crossroads Brick Block Puzzle": (
                CanHitGroundedBlocks()
                & CanHitFloatingBlocks()
            )
        },
        "exits": {
            "KR Koopa Village 1": None,
            "KR Pleasant Crossroads Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "KR Path to Fortress 1 West Exit",
        "area_id": "6",
        "map_id": "7",
        "map_name": "Path to Fortress 1",
        "locations": {
            "KR Path to Fortress 1 Hidden Panel": CanFlipPanels(),
            "KR Path to Fortress 1 X On Ground 1": None,
            "KR Path to Fortress 1 X On Ground 2": None,
            "KR Path to Fortress 1 X On Ground 3": None,
            "KR Path to Fortress 1 X On Ground 4": None,
            "KR Path to Fortress 1 X On Ground 5": None,
        },
        "exits": {
            "KR Pleasant Crossroads Upper": None,
            "KR Path to Fortress 1 West": None,
            "KR Path to Fortress 1 On Block": CanUseAbilityKooper(),
        }
    },
    {
        "region_name": "KR Path to Fortress 1 On Block",
        "area_id": "6",
        "map_id": "7",
        "map_name": "Path to Fortress 1",
        "locations": {
            "KR Path to Fortress 1 On Brick Block": None,
        },
        "exits": {
            "KR Path to Fortress 1 West": None,
        }
    },
    {
        "region_name": "KR Path to Fortress 1 West",
        "area_id": "6",
        "map_id": "7",
        "map_name": "Path to Fortress 1",
        "events": {
            "MF_NOK14_BuiltBridge": CanUseAbilityKooper(),
        },
        "exits": {
            "KR Path to Fortress 1 East": Has("MF_NOK14_BuiltBridge"),
            "KR Path to Fortress 1 West Exit": CanClimbSteps(),
            "KR Path to Fortress 1 On Block": HasUltraBoots(),
        }
    },
    {
        "region_name": "KR Path to Fortress 1 East",
        "area_id": "6",
        "map_id": "7",
        "map_name": "Path to Fortress 1",
        "events": {
            "MF_NOK14_BuiltBridge": CanHitGroundedSwitches(),
        },
        "locations": {
            "KR Path to Fortress 1 Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "KR Path to Fortress 2": None,
            "KR Path to Fortress 1 West": Has("MF_NOK14_BuiltBridge") & CanClimbSteps(),
        }
    },
    {
        "region_name": "KR Path to Fortress 2",
        "area_id": "6",
        "map_id": "8",
        "map_name": "Path to Fortress 2",
        "locations": {
            "KR Path to Fortress 2 In Tree": CanShakeTrees(),
        },
        "exits": {
            "KR Path to Fortress 1 East": None,
            "KBF Fortress Exterior": None,
            "KR Path to Fortress 2 Lower Pipe": CanUseAbilityBombette() & CanClimbSteps(),
        }
    },
    {
        "region_name": "KR Path to Fortress 2 Lower Pipe",
        "area_id": "6",
        "map_id": "8",
        "map_name": "Path to Fortress 2",
        "exits": {
            "KR Path to Fortress 2": CanUseAbilityBombette(),
            "KR Path to Fortress 2 Upper Pipe": CanReenterVerticalPipes(),
        }
    },
    {
        "region_name": "KR Path to Fortress 2 Upper Pipe",
        "area_id": "6",
        "map_id": "8",
        "map_name": "Path to Fortress 2",
        "exits": {
            "KR Path to Fortress 2 Upper": None,
            "KR Path to Fortress 2 Lower Pipe": CanReenterVerticalPipes(),
        }
    },
    {
        "region_name": "KR Path to Fortress 2 Upper",
        "area_id": "6",
        "map_id": "8",
        "map_name": "Path to Fortress 2",
        "exits": {
            "KBF Fortress Exterior Upper": None,
            "KR Path to Fortress 2": None,
        }
    }
]
