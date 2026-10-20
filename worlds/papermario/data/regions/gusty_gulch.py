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
    #OptionFilter,
)

from .LogicHelpers import (
    #HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    #HasBoots,
    HasSuperBoots,
    #HasUltraBoots,
    #CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    #CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

from ...options import OpenPrologue

gusty_gulch_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "GG Wasteland Ascent 1 West",
        "area_id": "14",
        "map_id": "0",
        "map_name": "Wasteland Ascent 1",
        "locations": {
            "GG Wasteland Ascent 1 On Rock": CanUseAbilityKooper(),
            "GG Wasteland Ascent 1 Yellow Block 1": CanHitFloatingBlocks(),
        },
        "exits": {
            "GG Ghost Town 2": None,
            "GG Wasteland Ascent 1 East": CanClimbSteps(),
        }
    },
    {
        "region_name": "GG Wasteland Ascent 1 East",
        "area_id": "14",
        "map_id": "0",
        "map_name": "Wasteland Ascent 1",
        "locations": {
            "GG Wasteland Ascent 1 Infront Of Branch": None,
            "GG Wasteland Ascent 1 Yellow Block 2": CanHitFloatingBlocks(),
            "GG Wasteland Ascent 1 Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "GG Wasteland Ascent 2 West": None,
            "GG Wasteland Ascent 1 West": None,
        }
    },
    {
        "region_name": "GG Ghost Town 1",
        "area_id": "14",
        "map_id": "1",
        "map_name": "Ghost Town 1",
        "locations": {
            "GG Ghost Town 1 From Boo (Koopa Koot Favor)": Has("FAVOR_7_01_active"),
            "GG Ghost Town 1 Yellow Block In House": CanHitFloatingBlocks(),
        },
        "exits": {
            "GG Windmill Exterior": None,
            "GG Ghost Town 2": None,
        }
    },
    {
        "region_name": "GG Wasteland Ascent 2 West",
        "area_id": "14",
        "map_id": "2",
        "map_name": "Wasteland Ascent 2",
        "exits": {
            "GG Wasteland Ascent 1 East": None,
            "GG Wasteland Ascent 2 East": CanUseAbilityParakarry(),
        }
    },
    {
        "region_name": "GG Wasteland Ascent 2 East",
        "area_id": "14",
        "map_id": "2",
        "map_name": "Wasteland Ascent 2",
        "locations": {
            "GG Wasteland Ascent 2 Behind Rock": None,
            "GG Wasteland Ascent 2 Yellow Block Left": CanHitFloatingBlocks(),
            "GG Wasteland Ascent 2 Yellow Block Right": CanHitFloatingBlocks(),
            "GG Wasteland Ascent 2 In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "TC Outside Tubbas Castle": None,
            "GG Wasteland Ascent 2 West": None,
        }
    },
    {
        "region_name": "GG Ghost Town 2",
        "area_id": "14",
        "map_id": "3",
        "map_name": "Ghost Town 2",
        "exits": {
            "GG Ghost Town 1": None,
            "GG Wasteland Ascent 1 West": None,
        }
    },
    {
        "region_name": "GG Windmill Exterior",
        "area_id": "14",
        "map_id": "4",
        "map_name": "Windmill Exterior",
        "events": {
            "STARSPIRIT_3": Has("RF_Ch3_HeartFledFirstTunnel"),
            "STARSPIRIT": Has("RF_Ch3_HeartFledFirstTunnel"),
        },
        "exits": {
            "GG Ghost Town 1": None,
            "FOR Exit to Gusty Gulch East": None,
            "GG Windmill Interior": Has("MysticalKey"),
        }
    },
    {
        "region_name": "GG Windmill Interior",
        "area_id": "14",
        "map_id": "5",
        "map_name": "Windmill Interior",
        "exits": {
            "GG Windmill Exterior": None,
            "GG Windmill Tunnel Entry": HasSuperBoots(),
        }
    },
    {
        "region_name": "GG Windmill Tunnel Entry",
        "area_id": "14",
        "map_id": "6",
        "map_name": "Windmill Tunnel Entry",
        "exits": {
            "GG Tunnel 1": None,
            "GG Windmill Interior": CanClimbSteps(),
        }
    },
    {
        "region_name": "GG Tunnel 1",
        "area_id": "14",
        "map_id": "7",
        "map_name": "Tunnel 1",
        "exits": {
            "GG Windmill Tunnel Entry": None,
            "GG Tunnel 2": None,
        }
    },
    {
        "region_name": "GG Tubba's Heart Chamber",
        "area_id": "14",
        "map_id": "8",
        "map_name": "Tubba's Heart Chamber",
        "events": {
            "RF_Ch3_HeartFledFirstTunnel": None,
        },
        "exits": {
            "GG Tunnel 3": None,
        }
    },
    {
        "region_name": "GG Tunnel 2",
        "area_id": "14",
        "map_id": "9",
        "map_name": "Tunnel 2",
        "exits": {
            "GG Tunnel 1": None,
            "GG Tunnel 3": None,
        }
    },
    {
        "region_name": "GG Tunnel 3",
        "area_id": "14",
        "map_id": "10",
        "map_name": "Tunnel 3",
        "exits": {
            "GG Tunnel 2": None,
            "GG Tubba's Heart Chamber": None,
        }
    }
]
