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
    #HasSuperBoots,
    #HasUltraBoots,
    #CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    #CanUseAbilityKooper,
    #CanUseAbilityBombette,
    #CanUseAbilityParakarry,
    #CanUseAbilityBow,
    CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    #CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    #CanClimbSteps,
    #CanReenterVerticalPipes,
)

inside_the_whale_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "ITW Whale Mouth",
        "area_id": "3",
        "map_id": "0",
        "map_name": "Whale Mouth",
        "exits": {
            "TT Port District": None,
            "ITW Whale Stomach": None,
        }
    },
    {
        "region_name": "ITW Whale Stomach",
        "area_id": "3",
        "map_id": "1",
        "map_name": "Whale Stomach",
        "events": {
            "RF_CanRideWhale": CanUseAbilityWatt(),
        },
        "exits": {
            "ITW Whale Mouth": None,
            "TT Port District": Has("RF_CanRideWhale"),
        }
    }
]
