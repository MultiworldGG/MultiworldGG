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
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    #CanSeeHiddenBlocks,
    CanShakeTrees,
    #CanUseAbilityKooper,
    #CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    #CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    #CanClimbSteps,
    #CanReenterVerticalPipes,
)

dry_dry_outpost_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "DDO Outpost 1",
        "area_id": "9",
        "map_id": "0",
        "map_name": "Outpost 1",
        "events": {
            "RF_CanMeetMoustafa": Has("RF_CanUseDROCode") & Has("RF_MouserReturned"),
            "RF_MouserLeftShop": None,
            "StarPiece_DRO_1": None,
            "StarPiece_DRO_8": None,
        },
        "locations": {
            "DDO Outpost 1 In Red Tree": CanShakeTrees(),
            "DDO Outpost 1 Composer Lyrics Reward": Has("Lyrics"),
            "DDO Outpost 1 Store Legend": Has("FAVOR_7_02_done") & Has("RF_MouserReturned"),
            "DDO Outpost 1 Little Mouser Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Little Mouser")
                & Has("RF_MouserReturned")
            ),
            "DDO Outpost 1 Shop Item 1": Has("RF_MouserReturned"),
            "DDO Outpost 1 Shop Item 2": Has("RF_MouserReturned"),
            "DDO Outpost 1 Shop Item 3": Has("RF_MouserReturned"),
            "DDO Outpost 1 Shop Item 4": Has("RF_MouserReturned"),
            "DDO Outpost 1 Shop Item 5": Has("RF_MouserReturned"),
            "DDO Outpost 1 Shop Item 6": Has("RF_MouserReturned"),
        },
        "exits": {
            "DDD E3 Outside Outpost": None,
            "DDO Outpost 2": None,
            "DDO Outpost 1 Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
        }
    },
    {
        "region_name": "DDO Outpost 1 Pipe",
        "area_id": "9",
        "map_id": "0",
        "map_name": "Outpost 1",
        "exits": {
            "TTT Warp Zone 1 (B1) Outpost Pipe": None,
            "DDO Outpost 1": None,
        }
    },
    {
        "region_name": "DDO Outpost 2",
        "area_id": "9",
        "map_id": "1",
        "map_name": "Outpost 2",
        "events": {
            "RF_MouserReturned": Has("RF_MouserLeftShop"),
            "RF_CanUseDROCode": Has("Lemon"),
            "StarPiece_DRO_1": None,
            "StarPiece_DRO_8": None,
        },
        "locations": {
            "DDO Outpost 2 Merlee Request (Koopa Koot Favor)": (
                Has("GF_HOS06_MerluvleeRequestedCrystalBall")
                & HasBoots()
            ),
            "DDO Outpost 2 Moustafa Gift": Has("RF_CanMeetMoustafa") & HasBoots(),
            "DDO Outpost 2 Mr. E. Letter Reward": CanUseAbilityParakarry() & Has("Letter to Mr E"),
            "DDO Outpost 2 Hidden Panel": CanFlipPanels() & Has("RF_CanMeetMoustafa") & HasBoots(),
            "DDO Outpost 2 Toad House Roof": Has("RF_CanMeetMoustafa") & HasBoots(),
        },
        "exits": {
            "DDO Outpost 1": None,
        }
    }
]
