from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    True_,
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
    #HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
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
    CanClimbSteps,
    #CanReenterVerticalPipes,
    CanOpenStarWay,
    HasStarBeamRequirements,
)

from ...options import BowserCastleMode, SeedGoal

shooting_star_summit_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "SSS Shooting Star Path",
        "area_id": "5",
        "map_id": "0",
        "map_name": "Shooting Star Path",
        "locations": {
            "SSS Shooting Star Path Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "PCG Ruined Castle Grounds": None,
            "SSS Merluvlee's House": None,
            "SSS Shooting Star Path East Upper Exit": CanClimbSteps(),
        }
    },
    {
        "region_name": "SSS Shooting Star Path East Upper Exit",
        "area_id": "5",
        "map_id": "0",
        "map_name": "Shooting Star Path",
        "exits": {
            "SSS Shooting Star Summit": None,
            "SSS Shooting Star Path": None,
        }
    },
    {
        "region_name": "SSS Shooting Star Summit Base",
        "area_id": "5",
        "map_id": "1",
        "map_name": "Shooting Star Summit",
        "locations": {
            "SSS Shooting Star Summit Behind The Summit": None,
        },
        "exits": {
            "SSS Shooting Star Path East Upper Exit": None,
            "SSS Shooting Star Summit": CanClimbSteps(),
        }
    },
    {
        "region_name": "SSS Shooting Star Summit",
        "area_id": "5",
        "map_id": "1",
        "map_name": "Shooting Star Summit",
        "events": {
            "STARROD": CanOpenStarWay(
                options=[OptionFilter(
                    SeedGoal,
                    SeedGoal.option_Open_Star_Way,
                )],
                filtered_resolution=False,
            )
        },
        "locations": {
            "SSS Shooting Star Summit Hidden Panel": CanClimbSteps() & CanFlipPanels(),
        },
        "exits": {
            "SSS Star Way": CanOpenStarWay(
                options=[OptionFilter(
                    SeedGoal,
                    SeedGoal.option_Defeat_Bowser,
                )],
                filtered_resolution=False,
            ),
            "SSS Shooting Star Summit Base": None,
        }
    },
    {
        "region_name": "SSS Merluvlee's House",
        "area_id": "5",
        "map_id": "6",
        "map_name": "Merluvlee's House",
        "events": {
            "GF_HOS06_MerluvleeRequestedCrystalBall": Has("FAVOR_3_03_active")
        },
        "locations": {
            "SSS Merluvlee's House Hidden Panel": CanFlipPanels(),
            "SSS Merluvlee's House Merluvlee Koopa Koot Favor": HasAll(
                "FAVOR_3_03_active",
                "Crystal Ball",
            ),
            "SSS Merluvlee's House Merlow Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Merlow")
            ),
            "SSS Merluvlee's House Merlow's Badges 1": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 2": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 3": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 4": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 5": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 6": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 7": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 8": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 9": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 10": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 11": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 12": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 13": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 14": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Badges 15": CanClimbSteps() & Has("Star Piece", count=30),
            "SSS Merluvlee's House Merlow's Rewards 1": CanClimbSteps() & Has("Star Piece", count=10),
            "SSS Merluvlee's House Merlow's Rewards 2": CanClimbSteps() & Has("Star Piece", count=23),
            "SSS Merluvlee's House Merlow's Rewards 3": CanClimbSteps() & Has("Star Piece", count=35),
            "SSS Merluvlee's House Merlow's Rewards 4": CanClimbSteps() & Has("Star Piece", count=47),
            "SSS Merluvlee's House Merlow's Rewards 5": CanClimbSteps() & Has("Star Piece", count=57),
            "SSS Merluvlee's House Merlow's Rewards 6": CanClimbSteps() & Has("Star Piece", count=68),
        },
        "exits": {
            "SSS Shooting Star Path": None,
        }
    }
]
