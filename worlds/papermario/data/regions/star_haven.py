from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    True_,
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
    OptionFilter,
)

from .LogicHelpers import (
    #HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    #CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    #CanUseAbilityKooper,
    #CanUseAbilityBombette,
    #CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    #CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
    #CanOpenStarWay,
    HasStarBeamRequirements,
)

from ...options import BowserCastleMode

star_haven_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "SSS Star Way",
        "area_id": "5",
        "map_id": "2",
        "map_name": "Star Way",
        "exits": {
            "SSS Shooting Star Summit": None,
            "SSS Star Haven": None,
        }
    },
    {
        "region_name": "SSS Star Haven",
        "area_id": "5",
        "map_id": "3",
        "map_name": "Star Haven",
        "events": {
            "Star_Piece_HOS_1": None,
            "Star_Piece_HOS_8": None,
        },
        "locations": {
            "SSS Star Haven Shop Item 1": HasBoots(),
            "SSS Star Haven Shop Item 2": HasBoots(),
            "SSS Star Haven Shop Item 3": HasBoots(),
            "SSS Star Haven Shop Item 4": HasBoots(),
            "SSS Star Haven Shop Item 5": HasBoots(),
            "SSS Star Haven Shop Item 6": HasBoots(),
        },
        "exits": {
            "SSS Star Way": None,
            "SSS Outside the Sanctuary": None,
        }
    },
    {
        "region_name": "SSS Outside the Sanctuary",
        "area_id": "5",
        "map_id": "4",
        "map_name": "Outside the Sanctuary",
        "exits": {
            "SSS Star Haven": None,
            "SSS Star Sanctuary": None,
        }
    },
    {
        "region_name": "SSS Star Sanctuary",
        "area_id": "5",
        "map_id": "5",
        "map_name": "Star Sanctuary",
        "locations": {
            "SSS Star Sanctuary Gift of the Stars": CanClimbSteps() & HasStarBeamRequirements(),
        },
        "exits": {
            "SSS Outside the Sanctuary": None,
            "SSS Star Sanctuary Starship": CanClimbSteps(),
        }
    },
    {
        "region_name": "SSS Star Sanctuary Starship",
        "area_id": "5",
        "map_id": "5",
        "map_name": "Star Sanctuary",
        "exits": {
            "SSS Riding Star Ship Scene": None,
            "SSS Star Sanctuary": None
        }
    },
    {
        "region_name": "SSS Riding Star Ship Scene",
        "area_id": "5",
        "map_id": "8",
        "map_name": "Riding Star Ship Scene",
        "exits": {
            "SSS Star Sanctuary Starship": None,
            "BC Ship Enter/Exit Scenes": True_(
                options=[OptionFilter(
                    BowserCastleMode,
                    BowserCastleMode.option_Boss_Rush,
                    operator="ne",
                )],
                filtered_resolution=False,
            ),
            "BC Fake Peach Hallway": True_(
                options=[OptionFilter(
                    BowserCastleMode,
                    BowserCastleMode.option_Boss_Rush,
                )],
                filtered_resolution=False,
            ),
        }
    }
]
