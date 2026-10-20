from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    #True_,
    #False_,
    #Has,
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

#from .LogicHelpers import (
#    HasHammer,
#    HasSuperHammer,
#    HasUltraHammer,
#    HasBoots,
#    HasSuperBoots,
#    HasUltraBoots,
#    CanFlipPanels,
#    CanSeeHiddenBlocks,
#    CanShakeTrees,
#    CanUseAbilityKooper,
#    CanUseAbilityBombette,
#    CanUseAbilityParakarry,
#    CanUseAbilityBow,
#    CanUseAbilityWatt,
#    CanUseAbilitySushie,
#    CanUseAbilityLakilester,
#    CanHitGroundedBlocks,
#    CanHitFloatingBlocks,
#    CanHitGroundedSwitches,
#    CanClimbSteps,
#    CanReenterVerticalPipes,
#)

minigames_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "MGM Playroom Lobby",
        "area_id": "25",
        "map_id": "0",
        "map_name": "Playroom Lobby",
        "exits": {
            "TT Station District Pipe": None,
        }
    }
]

