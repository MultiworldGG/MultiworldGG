from typing import Dict

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
    #OptionFilter,
)

from .LogicHelpers import (
    HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    CanUseAbilitySushie,
    CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

flower_fields_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "FLO Fields Center",
        "area_id": "19",
        "map_id": "0",
        "map_name": "Center",
        "events": {
            "RF_GrewBeanstalk": HasAll(
                "RF_Ch6_DestroyedPuffPuffMachine",
                "Magical Bean",
                "Fertile Soil",
                "Miracle Water",
            ) & CanClimbSteps(),
        },
        "exits": {
            "TT Plaza District": None,
            "FLO (NW) Bubble Flower East": None,
            "FLO (West) Path to Maze East": None,
            "FLO (SW) Path to Crystal Tree East": None,
            "FLO (NE) Elevators West": None,
            "FLO (East) Triple Tree Path": None,
            "FLO (SE) Briar Platforming West": None,
            "FLO Cloudy Climb": Has("RF_GrewBeanstalk"),
        }
    },
    {
        "region_name": "FLO (NE) Elevators West",
        "area_id": "19",
        "map_id": "11",
        "map_name": "(NE) Elevators",
        "locations": {
            "FLO (NE) Elevators Leftside Vine": (
                CanClimbSteps()
                | CanUseAbilityKooper()
                | CanUseAbilityLakilester()
            ),
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (NE) Elevators East": HasSuperBoots() & CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "FLO (NE) Elevators East",
        "area_id": "19",
        "map_id": "11",
        "map_name": "(NE) Elevators",
        "locations": {
            "FLO (NE) Elevators Stomp On Ledge": HasSuperBoots(),
            "FLO (NE) Elevators In SuperBlock": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "FLO (NE) Fallen Logs": None,
            "FLO (NE) Elevators West": HasSuperBoots() | CanUseAbilityLakilester(), #TODO check this
        }
    },
    {
        "region_name": "FLO (NE) Fallen Logs",
        "area_id": "19",
        "map_id": "12",
        "map_name": "(NE) Fallen Logs",
        "locations": {
            "FLO (NE) Fallen Logs Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "FLO (NE) Fallen Logs In The Flowers": None,
        },
        "exits": {
            "FLO (NE) Elevators East": None,
            "FLO (NE) Puff Puff Machine": None,
        }
    },
    {
        "region_name": "FLO (NE) Puff Puff Machine",
        "area_id": "19",
        "map_id": "13",
        "map_name": "(NE) Puff Puff Machine",
        "events": {
            "RF_Ch6_DestroyedPuffPuffMachine": HasHammer() | CanUseAbilityBombette(),
        },
        "exits": {
            "FLO (NE) Fallen Logs": None,
        }
    },
    {
        "region_name": "FLO (East) Triple Tree Path",
        "area_id": "19",
        "map_id": "4",
        "map_name": "(East) Triple Tree Path",
        "locations": {
            "FLO (East) Triple Tree Path Tree Puzzle Reward": CanShakeTrees(),
            "FLO (East) Triple Tree Path Leftmost Vine": None,
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (East) Petunia's Field": None,
        }
    },
    {
        "region_name": "FLO (East) Petunia's Field",
        "area_id": "19",
        "map_id": "1",
        "map_name": "(East) Petunia's Field",
        "locations": {
            "FLO (East) Petunia's Field Hidden Panel": CanFlipPanels(),
            "FLO (East) Petunia's Field Petunia Gift": None,
            "FLO (East) Petunia's Field In Tree 1": CanShakeTrees(),
            "FLO (East) Petunia's Field In Tree 2": CanShakeTrees(),
        },
        "exits": {
            "FLO (East) Triple Tree Path": None,
            "FLO (East) Old Well": None,
        }
    },
    {
        "region_name": "FLO (East) Old Well",
        "area_id": "19",
        "map_id": "16",
        "map_name": "(East) Old Well",
        "locations": {
            "FLO (East) Old Well Well Reward": Has("Blue Berry"),
        },
        "exits": {
            "FLO (East) Petunia's Field": None,
        }
    },
    {
        "region_name": "FLO (SE) Briar Platforming West",
        "area_id": "19",
        "map_id": "3",
        "map_name": "(SE) Briar Platforming",
        "events": {
            "GF_FLO08_GaveYellowBerry": Has("Yellow Berry"),
        },
        "locations": {
            "FLO (SE) Briar Platforming Left Side Vine": None,
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (SE) Briar Platforming East": (
                Has("Yellow Berry")
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester())
            ),
        }
    },
    {
        "region_name": "FLO (SE) Briar Platforming East",
        "area_id": "19",
        "map_id": "3",
        "map_name": "(SE) Briar Platforming",
        "locations": {
            "FLO (SE) Briar Platforming In The Flowers": None,
            "FLO (SE) Briar Platforming In Tree 1": CanShakeTrees(),
            "FLO (SE) Briar Platforming In Tree 2": CanShakeTrees(),
            "FLO (SE) Briar Platforming In SuperBlock": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "FLO (SE) Water Level Room West": None,
            "FLO (SE) Briar Platforming West": (
                Has("GF_FLO08_GaveYellowBerry")
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester())
            ),
        }
    },
    {
        "region_name": "FLO (SE) Water Level Room West",
        "area_id": "19",
        "map_id": "18",
        "map_name": "(SE) Water Level Room",
        "locations": {
            "FLO (SE) Water Level Room Yellow Block": CanHitFloatingBlocks(),
            "FLO (SE) Water Level Room In Tree 1": (
                CanShakeTrees()
                & CanUseAbilitySushie()
                & Has("RF_Ch6_ReturnedWaterStone")
            ),
            "FLO (SE) Water Level Room In Tree 2": (
                CanShakeTrees()
                & CanUseAbilitySushie()
                & Has("RF_Ch6_ReturnedWaterStone")
            ),
        },
        "exits": {
            "FLO (SE) Briar Platforming East": None,
            "FLO (SE) Water Level Room East": (
                (CanClimbSteps() | Has ("RF_Ch6_ReturnedWaterStone"))
                & (CanClimbSteps() | CanUseAbilitySushie())
            ),
        }
    },
    {
        "region_name": "FLO (SE) Water Level Room East",
        "area_id": "19",
        "map_id": "18",
        "map_name": "(SE) Water Level Room",
        "locations": {
            "FLO (SE) Water Level Room Hidden Panel": CanFlipPanels(),
            "FLO (SE) Water Level Room Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "FLO (SE) Lily's Fountain": None,
            "FLO (SE) Water Level Room West": (
                (CanClimbSteps() | Has("RF_Ch6_ReturnedWaterStone"))
                & (CanClimbSteps() | CanUseAbilitySushie())
            ),
        }
    },
    {
        "region_name": "FLO (SE) Lily's Fountain",
        "area_id": "19",
        "map_id": "5",
        "map_name": "(SE) Lily's Fountain",
        "events": {
            "RF_Ch6_ReturnedWaterStone": Has("Water Stone")
        },
        "locations": {
            "FLO (SE) Lily's Fountain Lily Reward For WaterStone": Has("Water Stone"),
            "FLO (SE) Lily's Fountain In Tree": CanShakeTrees(),
        },
        "exits": {
            "FLO (SE) Water Level Room West": None,
        }
    },
    {
        "region_name": "FLO (SW) Path to Crystal Tree East",
        "area_id": "19",
        "map_id": "19",
        "map_name": "(SW) Path to Crystal Tree",
        "events": {
            "GF_FLO25_GaveRedBerry": Has("Red Berry"),
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (SW) Path to Crystal Tree West": Has("GF_FLO25_GaveRedBerry"),
        }
    },
    {
        "region_name": "FLO (SW) Path to Crystal Tree West",
        "area_id": "19",
        "map_id": "19",
        "map_name": "(SW) Path to Crystal Tree",
        "locations": {
            "FLO (SW) Path to Crystal Tree Hidden Panel": CanFlipPanels(),
            "FLO (SW) Path to Crystal Tree Central Vine": None,
            "FLO (SW) Path to Crystal Tree In Tree 1": CanShakeTrees(),
            "FLO (SW) Path to Crystal Tree In Tree 2": CanShakeTrees(),
        },
        "exits": {
            "FLO (SW) Posie and Crystal Tree": None,
            "FLO (SW) Path to Crystal Tree East": Has("GF_FLO25_GaveRedBerry"),
        }
    },
    {
        "region_name": "FLO (SW) Posie and Crystal Tree",
        "area_id": "19",
        "map_id": "2",
        "map_name": "(SW) Posie and Crystal Tree",
        "locations": {
            "FLO (SW) Posie and Crystal Tree Posie Gift 2": None,
            "FLO (SW) Posie and Crystal Tree Posie Gift 1": None,
        },
        "exits": {
            "FLO (SW) Path to Crystal Tree West": None,
        }
    },
    {
        "region_name": "FLO (West) Path to Maze East",
        "area_id": "19",
        "map_id": "17",
        "map_name": "(West) Path to Maze",
        "events": {
            "GF_FLO23_GaveBlueBerry": Has("Blue Berry"),
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (West) Path to Maze West": Has("GF_FLO23_GaveBlueBerry"),
        }
    },
    {
        "region_name": "FLO (West) Path to Maze West",
        "area_id": "19",
        "map_id": "17",
        "map_name": "(West) Path to Maze",
        "locations": {
            "FLO (West) Path to Maze Upper Hidden Block": CanSeeHiddenBlocks() & HasBoots(),
            "FLO (West) Path to Maze Lower Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "FLO (West) Maze East": None,
            "FLO (West) Path to Maze East": Has("GF_FLO23_GaveBlueBerry"),
        }
    },
    {
        "region_name": "FLO (West) Maze East",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Path to Maze West": None,
            "FLO (West) Maze Pipe 1": HasBoots(),
            "FLO (West) Maze Pipe 2": HasBoots(),
            "FLO (West) Maze Pipe 3": HasBoots(),
            "FLO (West) Maze Pipe 4": HasBoots(),
            "FLO (West) Maze Pipe 5": HasBoots(),
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 1",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 4": CanReenterVerticalPipes(),
            "FLO (West) Maze East": None,
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 2",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 5": CanReenterVerticalPipes(),
            "FLO (West) Maze East": None,
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 3",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 6": CanReenterVerticalPipes(),
            "FLO (West) Maze East": None,
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 4",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 1": CanReenterVerticalPipes(),
            "FLO (West) Maze East": None,
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 5",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 2": CanReenterVerticalPipes(),
            "FLO (West) Maze East": None,
        }
    },
    {
        "region_name": "FLO (West) Maze Pipe 6",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "exits": {
            "FLO (West) Maze Pipe 3": CanReenterVerticalPipes(),
            "FLO (West) Maze West": None
        }
    },
    {
        "region_name": "FLO (West) Maze West",
        "area_id": "19",
        "map_id": "6",
        "map_name": "(West) Maze",
        "locations": {
            "FLO (West) Maze In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "FLO (West) Rosie's Trellis": None,
            "FLO (West) Maze Pipe 6": HasBoots(),
        }
    },
    {
        "region_name": "FLO (West) Rosie's Trellis",
        "area_id": "19",
        "map_id": "7",
        "map_name": "(West) Rosie's Trellis",
        "locations": {
            "FLO (West) Rosie's Trellis Rosie Gift": Has("Crystal Berry"),
        },
        "exits": {
            "FLO (West) Maze West": None,
        }
    },
    {
        "region_name": "FLO (NW) Bubble Flower East",
        "area_id": "19",
        "map_id": "9",
        "map_name": "(NW) Bubble Flower",
        "locations": {
            "FLO (NW) Bubble Flower Right Vine": None,
        },
        "exits": {
            "FLO Fields Center": None,
            "FLO (NW) Bubble Flower West": Has("Bubble Berry") | CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "FLO (NW) Bubble Flower West",
        "area_id": "19",
        "map_id": "9",
        "map_name": "(NW) Bubble Flower",
        "locations": {
            "FLO (NW) Bubble Flower On Ledge": CanClimbSteps(),
        },
        "exits": {
            "FLO (NW) Lakilester": None,
            "FLO (NW) Bubble Flower East": CanUseAbilityLakilester() | CanClimbSteps(),
        }
    },
    {
        "region_name": "FLO (NW) Lakilester",
        "area_id": "19",
        "map_id": "8",
        "map_name": "(NW) Lakilester",
        "locations": {
            "FLO (NW) Lakilester Cage Under Rock": CanUseAbilityBombette() & CanClimbSteps(),
            "FLO (NW) Lakilester In The Flowers": None,
            "FLO (NW) Lakilester Lakilester Partner": Has("RF_Ch6_SpokeWithTheSun"),
        },
        "exits": {
            "FLO (NW) Bubble Flower West": None,
            "FLO (NW) Sun Tower": None,
        }
    },
    {
        "region_name": "FLO (NW) Sun Tower",
        "area_id": "19",
        "map_id": "10",
        "map_name": "(NW) Sun Tower",
        "events": {
            "RF_Ch6_SpokeWithTheSun": CanUseAbilityBombette(),
        },
        "exits": {
            "FLO (NW) Lakilester": None,
        }
    },
    {
        "region_name": "FLO Cloudy Climb",
        "area_id": "19",
        "map_id": "14",
        "map_name": "Cloudy Climb",
        "locations": {
            "FLO Cloudy Climb On Cloud": CanClimbSteps() | CanUseAbilityKooper(),
        },
        "exits": {
            "FLO Huff N Puff Room": None,
            "FLO Fields Center": CanClimbSteps() & Has("RF_GrewBeanstalk"),
        }
    },
    {
        "region_name": "FLO Huff N Puff Room",
        "area_id": "19",
        "map_id": "15",
        "map_name": "Huff N Puff Room",
        "events": {
            "STARSPIRIT_6": CanClimbSteps(),
            "STARSPIRIT": CanClimbSteps(),
        },
        "exits": {
            "FLO Cloudy Climb": None,
        }
    }
]
