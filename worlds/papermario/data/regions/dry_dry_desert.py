from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    #True_,
    #False_,
    Has,
    #HasAll,
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
)

from .LogicHelpers import (
    #HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    #HasBoots,
    #HasSuperBoots,
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    CanUseAbilityKooper,
    #CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

dry_dry_desert_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "DDD N3W3",
        "area_id": "10",
        "map_id": "0",
        "map_name": "N3W3",
        "locations": {
            "DDD N3W3 Yellow Block Left": CanHitGroundedBlocks(),
            "DDD N3W3 Yellow Block Right": CanHitGroundedBlocks(),
        },
        "exits": {
            "DDD N3W2": None,
            "DDD N2W3": None,
        }
    },
    {
        "region_name": "DDD N3W2",
        "area_id": "10",
        "map_id": "1",
        "map_name": "N3W2",
        "exits": {
            "DDD N3W3": None,
            "DDD N3W1 Ruins Entrance": None,
            "DDD N2W2": None,
        }
    },
    {
        "region_name": "DDD N3W1 Ruins Entrance",
        "area_id": "10",
        "map_id": "2",
        "map_name": "N3W1 Ruins Entrance",
        "events": {
            "RF_RadioTradeEvt2Done": Has("RF_RadioTradeEvt2") & Has("AF_CanMakeNuttyCake")
        },
        "locations": {
            "DDD N3W1 Ruins Entrance Radio Trade Event 2 Reward": Has("RF_RadioTradeEvt2") & Has("AF_CanMakeNuttyCake")
        },
        "exits": {
            "DDD N3W2": None,
            "DDD N3": None,
            "DDD N2W1": None,
            "DDR Ruins Entrance": Has("Pulse Stone"),
        }
    },
    {
        "region_name": "DDD N3",
        "area_id": "10",
        "map_id": "3",
        "map_name": "N3",
        "exits": {
            "DDD N3W1 Ruins Entrance": None,
            "DDD N3E1": None,
            "DDD N2": None,
        }
    },
    {
        "region_name": "DDD N3E1",
        "area_id": "10",
        "map_id": "4",
        "map_name": "N3E1",
        "exits": {
            "DDD N3": None,
            "DDD N3E2 Pokey Army": None,
            "DDD N2E1 (Tweester A)": None,
        }
    },
    {
        "region_name": "DDD N3E2 Pokey Army",
        "area_id": "10",
        "map_id": "5",
        "map_name": "N3E2 Pokey Army",
        "locations": {
            "DDD N3E2 Pokey Army Behind Cactus": None
        },
        "exits": {
            "DDD N3E1": None,
            "DDD N3E3": None,
            "DDD N2E2": None,
        }
    },
    {
        "region_name": "DDD N3E3",
        "area_id": "10",
        "map_id": "6",
        "map_name": "N3E3",
        "locations": {
            "DDD N3E3 In Tree": CanShakeTrees(),
            "DDD N3E3 In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD N3E2 Pokey Army": None,
            "DDD N2E3": None
        }
    },
    {
        "region_name": "DDD N2W3",
        "area_id": "10",
        "map_id": "7",
        "map_name": "N2W3",
        "locations": {
            "DDD N2W3 Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks() & CanClimbSteps(),
        },
        "exits": {
            "DDD N2W2": None,
            "DDD N3W3": None,
            "DDD N1W3 Special Block": None,
        }
    },
    {
        "region_name": "DDD N2W2",
        "area_id": "10",
        "map_id": "8",
        "map_name": "N2W2",
        "exits": {
            "DDD N2W3": None,
            "DDD N2W1": None,
            "DDD N3W2": None,
            "DDD N1W2": None,
        }
    },
    {
        "region_name": "DDD N2W1",
        "area_id": "10",
        "map_id": "9",
        "map_name": "N2W1",
        "exits": {
            "DDD N2W2": None,
            "DDD N2": None,
            "DDD N3W1 Ruins Entrance": None,
            "DDD N1W1": None,
        }
    },
    {
        "region_name": "DDD N2",
        "area_id": "10",
        "map_id": "10",
        "map_name": "N2",
        "exits": {
            "DDD N2W1": None,
            "DDD N2E1 (Tweester A)": None,
            "DDD N3": None,
            "DDD N1 (Tweester B)": None,
        }
    },
    {
        "region_name": "DDD N2E1 (Tweester A)",
        "area_id": "10",
        "map_id": "11",
        "map_name": "N2E1 (Tweester A)",
        "locations": {
            "DDD N2E1 (Tweester A) Yellow Block Left": CanHitGroundedBlocks(),
            "DDD N2E1 (Tweester A) Yellow Block Right": CanHitGroundedBlocks(),
            "DDD N2E1 (Tweester A) In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD N2": None,
            "DDD N2E2": None,
            "DDD N3E1": None,
            "DDD N1E1 Palm Trio": None,
            "DDD N3E2 Pokey Army": None,
        }
    },
    {
        "region_name": "DDD N2E2",
        "area_id": "10",
        "map_id": "12",
        "map_name": "N2E2",
        "exits": {
            "DDD N2E1 (Tweester A)": None,
            "DDD N2E3": None,
            "DDD N3E2 Pokey Army": None,
            "DDD N1E2": None,
        }
    },
    {
        "region_name": "DDD N2E3",
        "area_id": "10",
        "map_id": "13",
        "map_name": "N2E3",
        "exits": {
            "DDD N2E2": None,
            "DDD N3E3": None,
            "DDD N1E3": None,
        }
    },
    {
        "region_name": "DDD N1W3 Special Block",
        "area_id": "10",
        "map_id": "14",
        "map_name": "N1W3 Special Block",
        "locations": {
            "DDD N1W3 Special Block Hit Block": CanHitGroundedBlocks() & CanHitFloatingBlocks(),
            "DDD N1W3 Special Block Hit Block Plenty": CanHitGroundedBlocks() & CanHitFloatingBlocks(),
            "DDD N1W3 Special Block Hit Block Very Much": CanHitGroundedBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD N1W2": None,
            "DDD N2W3": None,
            "DDD W3 Kolorado's Camp": None,
        }
    },
    {
        "region_name": "DDD N1W2",
        "area_id": "10",
        "map_id": "15",
        "map_name": "N1W2",
        "exits": {
            "DDD N1W3 Special Block": None,
            "DDD N1W1": None,
            "DDD N2W2": None,
            "DDD W2": None,
        }
    },
    {
        "region_name": "DDD N1W1",
        "area_id": "10",
        "map_id": "16",
        "map_name": "N1W1",
        "locations": {
            "DDD N1W1 Yellow Block 1": CanHitGroundedBlocks(),
            "DDD N1W1 Yellow Block 2": CanHitGroundedBlocks(),
            "DDD N1W1 Yellow Block 3": CanHitGroundedBlocks(),
            "DDD N1W1 Yellow Block 4": CanHitGroundedBlocks(),
            "DDD N1W1 Yellow Block Center": CanHitGroundedBlocks(),
        },
        "exits": {
            "DDD N1W2": None,
            "DDD N1 (Tweester B)": None,
            "DDD N2W1": None,
            "DDD W1": None,
        }
    },
    {
        "region_name": "DDD N1 (Tweester B)",
        "area_id": "10",
        "map_id": "17",
        "map_name": "N1 (Tweester B)",
        "exits": {
            "DDD N1W1": None,
            "DDD N1E1 Palm Trio": None,
            "DDD N2": None,
            "DDD Center (Tweester C)": None,
            "DDD N2E1 (Tweester A)": None,
        }
    },
    {
        "region_name": "DDD N1E1 Palm Trio",
        "area_id": "10",
        "map_id": "18",
        "map_name": "N1E1 Palm Trio",
        "locations": {
            "DDD N1E1 Palm Trio Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD N1 (Tweester B)": None,
            "DDD N1E2": None,
            "DDD N2E1 (Tweester A)": None,
            "DDD E1 Nomadimouse": None,
        }
    },
    {
        "region_name": "DDD N1E2",
        "area_id": "10",
        "map_id": "19",
        "map_name": "N1E2",
        "locations": {
            "DDD N1E2 In MultiCoinBlock Center": CanHitFloatingBlocks(),
            "DDD N1E2 In MultiCoinBlock Bottom Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD N1E1 Palm Trio": None,
            "DDD N1E3": None,
            "DDD N2E2": None,
            "DDD E2": None,
        }
    },
    {
        "region_name": "DDD N1E3",
        "area_id": "10",
        "map_id": "20",
        "map_name": "N1E3",
        "locations": {
            "DDD N1E3 In Tree": CanShakeTrees(),
        },
        "exits": {
            "DDD N1E2": None,
            "DDD N2E3": None,
            "DDD E3 Outside Outpost": None
        }
    },
    {
        "region_name": "DDD W3 Kolorado's Camp",
        "area_id": "10",
        "map_id": "21",
        "map_name": "W3 Kolorado's Camp",
        "events": {
            "RF_CanVisitDesertCamp": None
        },
        "locations": {
            "DDD W3 Kolorado's Camp In Tree": Has("RF_Ch2_SavedStarSpirit") & CanShakeTrees(),
        },
        "exits": {
            "DDD Desert Rugged Entrance East": None,
            "DDD W2": None,
            "DDD N1W3 Special Block": None,
            "DDD S1W3": None,
        }
    },
    {
        "region_name": "DDD W2",
        "area_id": "10",
        "map_id": "22",
        "map_name": "W2",
        "exits": {
            "DDD W3 Kolorado's Camp": None,
            "DDD W1": None,
            "DDD N1W2": None,
            "DDD S1W2 (Tweester D)": None,
        }
    },
    {
        "region_name": "DDD W1",
        "area_id": "10",
        "map_id": "23",
        "map_name": "W1",
        "exits": {
            "DDD W2": None,
            "DDD Center (Tweester C)": None,
            "DDD N1W1": None,
            "DDD S1W1": None,
        }
    },
    {
        "region_name": "DDD Center (Tweester C)",
        "area_id": "10",
        "map_id": "24",
        "map_name": "Center (Tweester C)",
        "locations": {
            "DDD Center (Tweester C) Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "DDD W1": None,
            "DDD E1 Nomadimouse": None,
            "DDD N1 (Tweester B)": None,
            "DDD S1": None,
            "DDD N1E1 Palm Trio": None,
        }
    },
    {
        "region_name": "DDD E1 Nomadimouse",
        "area_id": "10",
        "map_id": "25",
        "map_name": "E1 Nomadimouse",
        "locations": {
            "DDD E1 Nomadimouse Nomadimouse Letter Reward": CanUseAbilityParakarry() & Has("Letter to Nomadimouse"),
            "DDD E1 Nomadimouse In Tree": CanShakeTrees(),
        },
        "exits": {
            "DDD Center (Tweester C)": None,
            "DDD E2": None,
            "DDD N1E1 Palm Trio": None,
            "DDD S1E1": None,
        }
    },
    {
        "region_name": "DDD E2",
        "area_id": "10",
        "map_id": "26",
        "map_name": "E2",
        "locations": {
            "DDD E2 In Tree Far Left": CanShakeTrees(),
        },
        "exits": {
            "DDD E1 Nomadimouse": None,
            "DDD E3 Outside Outpost": None,
            "DDD N1E2": None,
            "DDD S1E2 Small Bluffs": None,
        }
    },
    {
        "region_name": "DDD E3 Outside Outpost",
        "area_id": "10",
        "map_id": "27",
        "map_name": "E3 Outside Outpost",
        "locations": {
            "DDD E3 Outside Outpost In Tree (Far Left)": CanShakeTrees(),
            "DDD E3 Outside Outpost In Tree (Second From Left)": CanShakeTrees(),
            "DDD E3 Outside Outpost In Tree (Fourth From Right)": CanShakeTrees(),
            "DDD E3 Outside Outpost In Tree (Far Right)": CanShakeTrees(),
        },
        "exits": {
            "DDD E2": None,
            "DDO Outpost 1": None,
            "DDD N1E3": None,
            "DDD S1E3 North of Oasis": None,
        }
    },
    {
        "region_name": "DDD S1W3",
        "area_id": "10",
        "map_id": "28",
        "map_name": "S1W3",
        "locations":{
            "DDD S1W3 In MultiCoinBlock Top Left": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD S1W2 (Tweester D)": None,
            "DDD W3 Kolorado's Camp": None,
            "DDD S2W3": None,
        }
    },
    {
        "region_name": "DDD S1W2 (Tweester D)",
        "area_id": "10",
        "map_id": "29",
        "map_name": "S1W2 (Tweester D)",
        "exits": {
            "DDD S1W3": None,
            "DDD S1W1": None,
            "DDD W2": None,
            "DDD S2W2": None,
            "DDD W1": None,
        }
    },
    {
        "region_name": "DDD S1W1",
        "area_id": "10",
        "map_id": "30",
        "map_name": "S1W1",
        "exits": {
            "DDD S1W2 (Tweester D)": None,
            "DDD S1": None,
            "DDD W1": None,
            "DDD S2W1": None,
        }
    },
    {
        "region_name": "DDD S1",
        "area_id": "10",
        "map_id": "31",
        "map_name": "S1",
        "locations": {
            "DDD S1 Yellow Block": CanHitGroundedBlocks(),
        },
        "exits": {
            "DDD S1W1": None,
            "DDD S1E1": None,
            "DDD Center (Tweester C)": None,
            "DDD S2": None,
        }
    },
    {
        "region_name": "DDD S1E1",
        "area_id": "10",
        "map_id": "32",
        "map_name": "S1E1",
        "exits": {
            "DDD S1": None,
            "DDD S1E2 Small Bluffs": None,
            "DDD E1 Nomadimouse": None,
            "DDD S2E1 Blue Cactus": None,
        }
    },
    {
        "region_name": "DDD S1E2 Small Bluffs",
        "area_id": "10",
        "map_id": "33",
        "map_name": "S1E2 Small Bluffs",
        "locations": {
            "DDD S1E2 Small Bluffs On Brick Block": (
                (CanUseAbilityKooper() | HasUltraBoots())
                & (CanClimbSteps() | HasUltraBoots())
            ),
        },
        "exits": {
            "DDD S1E1": None,
            "DDD S1E3 North of Oasis": None,
            "DDD E2": None,
            "DDD S2E2 West of Oasis": None,
        }
    },
    {
        "region_name": "DDD S1E2 Small Bluffs On Bluff",
        "area_id": "10",
        "map_id": "33",
        "map_name": "S1E2 Small Bluffs",
        "locations": {
            "DDD S1E2 Small Bluffs Ontop Of Bluffs": None,
        },
        "exits": {
            "DDD S1E2 Small Bluffs": None,
        }
    },
    {
        "region_name": "DDD S1E3 North of Oasis",
        "area_id": "10",
        "map_id": "34",
        "map_name": "S1E3 North of Oasis",
        "locations": {
            "DDD S1E3 North of Oasis Hidden Block": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
            "DDD S1E3 North of Oasis Yellow Block": CanHitGroundedBlocks(),
            "DDD S1E3 North of Oasis Tree Bottom Left": CanShakeTrees(),
        },
        "exits": {
            "DDD S1E2 Small Bluffs": None,
            "DDD E3 Outside Outpost": None,
            "DDD S2E3 Oasis": None,
        }
    },
    {
        "region_name": "DDD S2W3",
        "area_id": "10",
        "map_id": "35",
        "map_name": "S2W3",
        "exits": {
            "DDD S2W2": None,
            "DDD S1W3": None,
            "DDD S3W3": None,
        }
    },
    {
        "region_name": "DDD S2W2",
        "area_id": "10",
        "map_id": "36",
        "map_name": "S2W2",
        "exits": {
            "DDD S2W3": None,
            "DDD S2W1": None,
            "DDD S1W2 (Tweester D)": None,
            "DDD S3W2 Hidden AttackFX": None,
        }
    },
    {
        "region_name": "DDD S2W1",
        "area_id": "10",
        "map_id": "37",
        "map_name": "S2W1",
        "locations": {
            "DDD S2W1 In MultiCoinBlock Top": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD S2W2": None,
            "DDD S2": None,
            "DDD S1W1": None,
            "DDD S3W1": None,
        }
    },
    {
        "region_name": "DDD S2",
        "area_id": "10",
        "map_id": "38",
        "map_name": "S2",
        "exits": {
            "DDD S2W1": None,
            "DDD S2E1 Blue Cactus": None,
            "DDD S1": None,
            "DDD S3": None,
        }
    },
    {
        "region_name": "DDD S2E1 Blue Cactus",
        "area_id": "10",
        "map_id": "39",
        "map_name": "S2E1 Blue Cactus",
        "exits": {
            "DDD S2": None,
            "DDD S2E2 West of Oasis": None,
            "DDD S1E1": None,
            "DDD S3E1": None,
            "DDD S1E2 Small Bluffs On Bluff": None,
        }
    },
    {
        "region_name": "DDD S2E2 West of Oasis",
        "area_id": "10",
        "map_id": "40",
        "map_name": "S2E2 West of Oasis",
        "locations": {
            "DDD S2E2 West of Oasis Behind Bush": None,
            "DDD S2E2 West of Oasis In Tree": CanShakeTrees(),
            "DDD S2E2 West of Oasis In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD S2E1 Blue Cactus": None,
            "DDD S2E3 Oasis": None,
            "DDD S1E2 Small Bluffs": None,
            "DDD S3E2": None,
        }
    },
    {
        "region_name": "DDD S2E3 Oasis",
        "area_id": "10",
        "map_id": "41",
        "map_name": "S2E3 Oasis",
        "locations": {
            "DDD S2E3 Oasis In Fruit Tree (Left)": CanShakeTrees(),
            "DDD S2E3 Oasis In Fruit Tree (Right)": CanShakeTrees(),
            "DDD S2E3 Oasis In Tree (Far Left)": CanShakeTrees(),
            "DDD S2E3 Oasis In Tree (Front Right)": CanShakeTrees(),
            "DDD S2E3 Oasis In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD S2E2 West of Oasis": None,
            "DDD S1E3 North of Oasis": None,
            "DDD S3E3 South of Oasis": None,
        }
    },
    {
        "region_name": "DDD S3W3",
        "area_id": "10",
        "map_id": "42",
        "map_name": "S3W3",
        "exits": {
            "DDD S3W2 Hidden AttackFX": None,
            "DDD S2W3": None,
        }
    },
    {
        "region_name": "DDD S3W2 Hidden AttackFX",
        "area_id": "10",
        "map_id": "43",
        "map_name": "S3W2 Hidden AttackFX",
        "locations": {
            "DDD S3W2 Hidden AttackFX Hidden Block": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
        },
        "exits": {
            "DDD S3W3": None,
            "DDD S3W1": None,
            "DDD S2W2": None,
        }
    },
    {
        "region_name": "DDD S3W1",
        "area_id": "10",
        "map_id": "44",
        "map_name": "S3W1",
        "exits": {
            "DDD S3W2 Hidden AttackFX": None,
            "DDD S3": None,
            "DDD S2W1": None,
        }
    },
    {
        "region_name": "DDD S3",
        "area_id": "10",
        "map_id": "45",
        "map_name": "S3",
        "exits": {
            "DDD S3W1": None,
            "DDD S3E1": None,
            "DDD S2": None,
        }
    },
    {
        "region_name": "DDD S3E1",
        "area_id": "10",
        "map_id": "46",
        "map_name": "S3E1",
        "locations": {
            "DDD S3E1 Yellow Block": CanHitGroundedBlocks(),
        },
        "exits": {
            "DDD S3": None,
            "DDD S3E2": None,
            "DDD S2E1 Blue Cactus": None,
        }
    },
    {
        "region_name": "DDD S3E2",
        "area_id": "10",
        "map_id": "47",
        "map_name": "S3E2",
        "exits": {
            "DDD S3E1": None,
            "DDD S3E3 South of Oasis": None,
            "DDD S2E2 West of Oasis": None,
        }
    },
    {
        "region_name": "DDD S3E3 South of Oasis",
        "area_id": "10",
        "map_id": "48",
        "map_name": "S3E3 South of Oasis",
        "locations": {
            "DDD S3E3 South of Oasis In Tree (Far Right)": CanShakeTrees(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Top Left": CanHitFloatingBlocks(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Top Right": CanHitFloatingBlocks(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Left": CanHitFloatingBlocks(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Right": CanHitFloatingBlocks(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Left": CanHitFloatingBlocks(),
            "DDD S3E3 South of Oasis In MultiCoinBlock Bottom Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDD S3E2": None,
            "DDD S2E3 Oasis": None,
        }
    },
    {
        "region_name": "DDD Desert Rugged Entrance West",
        "area_id": "10",
        "map_id": "49",
        "map_name": "Entrance",
        "exits": {
            "MR Suspension Bridge East": None,
            "DDD Desert Rugged Entrance East": None,
        }
    },
    {
        "region_name": "DDD Desert Rugged Entrance East",
        "area_id": "10",
        "map_id": "49",
        "map_name": "Entrance",
        "exits": {
            "DDD Desert Rugged Entrance West": CanClimbSteps(),
            "DDD W3 Kolorado's Camp": None,
        }
    }
]
