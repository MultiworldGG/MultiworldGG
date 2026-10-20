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
    HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    #HasBoots,
    HasSuperBoots,
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    #CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

crystal_palace_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "CP Palace Entrance South",
        "area_id": "21",
        "map_id": "0",
        "map_name": "Entrance",
        "exits": {
            "SR Shiver Mountain Peaks": None,
            "CP Entry Hall South": None,
        }
    },
    {
        "region_name": "CP Palace Entrance North",
        "area_id": "21",
        "map_id": "0",
        "map_name": "Entrance",
        "exits": {
            "CP Entry Hall North": None,
            "CP Star Piece Cave": None,
        }
    },
    {
        "region_name": "CP Entry Hall South",
        "area_id": "21",
        "map_id": "1",
        "map_name": "Entry Hall",
        "exits": {
            "CP Palace Entrance South": None,
            "CP Palace Save Room Upper": None,
            "CP Blue Mirror Hall 1 South": Has("Blue Key") & HasSuperBoots(),
            "CP Red Mirror Hall": Has("Red Key"),
        }
    },
    {
        "region_name": "CP Entry Hall North",
        "area_id": "21",
        "map_id": "1",
        "map_name": "Entry Hall",
        "exits": {
            "CP Blue Mirror Hall 1 North": Has("Blue Key") & HasSuperBoots(),
            "CP Red Mirror Hall": Has("Red Key"),
            "CP Reflected Save Room Upper": None,
            "CP Palace Entrance North": None,
        }
    },
    {
        "region_name": "CP Palace Save Room Upper",
        "area_id": "21",
        "map_id": "2",
        "map_name": "Save Room",
        "exits": {
            "CP Entry Hall South": None,
            "CP Blue Key Hall": None,
            "CP Palace Save Room Lower": Has("GF_PRA04_BoardedFloor"),
        }
    },
    {
        "region_name": "CP Palace Save Room Lower",
        "area_id": "21",
        "map_id": "2",
        "map_name": "Save Room",
        "exits": {
            "CP Red Key Hall": None,
            "CP Palace Save Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "CP Reflected Save Room Upper",
        "area_id": "21",
        "map_id": "3",
        "map_name": "Reflected Save Room",
        "events": {
            "GF_PRA04_BoardedFloor": HasSuperBoots(),
        },
        "locations": {
            "CP Reflected Save Room Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "CP Entry Hall North": None,
            "CP Shooting Star Hall": None,
            "CP Reflected Save Room Lower": HasSuperBoots(),
        }
    },
    {
        "region_name": "CP Reflected Save Room Lower",
        "area_id": "21",
        "map_id": "3",
        "map_name": "Reflected Save Room",
        "exits": {
            "CP P-Down, D-Up Hall": None,
            "CP Reflected Save Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "CP Blue Key Room",
        "area_id": "21",
        "map_id": "4",
        "map_name": "Blue Key Room",
        "locations": {
            "CP Blue Key Room In Chest": CanClimbSteps(),
        },
        "exits": {
            "CP Blue Key Hall": None
        }
    },
    {
        "region_name": "CP Shooting Star Room",
        "area_id": "21",
        "map_id": "5",
        "map_name": "Shooting Star Room",
        "locations": {
            "CP Shooting Star Room On The Ground": CanClimbSteps(),
        },
        "exits": {
            "CP Shooting Star Hall": None
        }
    },
    {
        "region_name": "CP Red Key Hall",
        "area_id": "21",
        "map_id": "6",
        "map_name": "Red Key Hall",
        "exits": {
            "CP Palace Save Room Lower": HasHammer(),
            "CP Red Key Room": CanUseAbilityBombette() & HasHammer()
        }
    },
    {
        "region_name": "CP P-Down, D-Up Hall",
        "area_id": "21",
        "map_id": "7",
        "map_name": "P-Down, D-Up Hall",
        "exits": {
            "CP Reflected Save Room Lower": None,
            "CP P-Down, D-Up Room": None
        }
    },
    {
        "region_name": "CP Red Key Room",
        "area_id": "21",
        "map_id": "8",
        "map_name": "Red Key Room",
        "locations": {
            "CP Red Key Room In Chest": CanClimbSteps(),
        },
        "exits": {
            "CP Red Key Hall": None
        }
    },
    {
        "region_name": "CP P-Down, D-Up Room",
        "area_id": "21",
        "map_id": "9",
        "map_name": "P-Down, D-Up Room",
        "locations": {
            "CP P-Down, D-Up Room In Chest": CanClimbSteps(),
        },
        "exits": {
            "CP P-Down, D-Up Hall": None
        }
    },
    {
        "region_name": "CP Blue Mirror Hall 1 South",
        "area_id": "21",
        "map_id": "10",
        "map_name": "Blue Mirror Hall 1",
        "exits": {
            "CP Entry Hall South": None,
            "CP Blue Mirror Hall 2": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "CP Blue Mirror Hall 1 North",
        "area_id": "21",
        "map_id": "10",
        "map_name": "Blue Mirror Hall 1",
        "exits": {
            "CP Blue Mirror Hall 2": CanUseAbilityBombette(),
            "CP Entry Hall North": None,
        }
    },
    {
        "region_name": "CP Blue Mirror Hall 2",
        "area_id": "21",
        "map_id": "11",
        "map_name": "Blue Mirror Hall 2",
        "locations": {
            "CP Blue Mirror Hall 2 In MultiCoinBlock Front": CanSeeHiddenBlocks(),
            "CP Blue Mirror Hall 2 In MultiCoinBlock Back": CanSeeHiddenBlocks(),
        },
        "exits": {
            "CP Blue Mirror Hall 1 North": CanUseAbilityBombette(),
            "CP Blue Mirror Hall 1 South": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "CP Star Piece Cave",
        "area_id": "21",
        "map_id": "12",
        "map_name": "Star Piece Cave",
        "locations": {
            "CP Star Piece Cave On The Ground": None,
        },
        "exits": {
            "CP Palace Entrance North": None,
        }
    },
    {
        "region_name": "CP Red Mirror Hall",
        "area_id": "21",
        "map_id": "13",
        "map_name": "Red Mirror Hall",
        "exits": {
            "CP Entry Hall North": None,
            "CP Bridge Mirror Hall North": None,
            "CP Bridge Mirror Hall South": None,
            "CP Entry Hall South": None,
        }
    },
    {
        "region_name": "CP Bridge Mirror Hall South",
        "area_id": "21",
        "map_id": "14",
        "map_name": "Bridge Mirror Hall",
        "events": {
            "MF_PRA_18_DefeatedClubbas": None,
        },
        "exits": {
            "CP Red Mirror Hall": None,
        }
    },
    {
        "region_name": "CP Bridge Mirror Hall North",
        "area_id": "21",
        "map_id": "14",
        "map_name": "Bridge Mirror Hall",
        "exits": {
            "CP Turnstyle Room North": Has("MF_PRA_18_DefeatedClubbas"),
            "CP Red Mirror Hall": None
        }
    },
    {
        "region_name": "CP Reflection Mimic Room",
        "area_id": "21",
        "map_id": "15",
        "map_name": "Reflection Mimic Room",
        "exits": {
            "CP Triple Dip Room South": HasHammer(),
            "CP Mirrored Door Room South": CanUseAbilityKooper() & HasHammer(),
        }
    },
    {
        "region_name": "CP Mirrored Door Room South",
        "area_id": "21",
        "map_id": "16",
        "map_name": "Mirrored Door Room",
        "exits": {
            "CP Reflection Mimic Room": None,
            "CP Huge Statue Room Upper": None,
            "CP Hidden Bridge Room South West": None,
        }
    },
    {
        "region_name": "CP Mirrored Door Room North",
        "area_id": "21",
        "map_id": "16",
        "map_name": "Mirrored Door Room",
        "exits": {
            "CP Hidden Bridge Room North West": None,
            "CP Small Statue Room Upper": None,
        }
    },
    {
        "region_name": "CP Huge Statue Room Upper",
        "area_id": "21",
        "map_id": "17",
        "map_name": "Huge Statue Room",
        "locations": {
            "CP Huge Statue Room Hidden Panel": CanFlipPanels(),
            "CP Huge Statue Room Yellow Block": HasUltraBoots(),
        },
        "exits": {
            "CP Mirrored Door Room South": None,
            "CP Huge Statue Room Lower": Has("MF_PRA_22_FoundHiddenRoomUnderStatue"),
        }
    },
    {
        "region_name": "CP Huge Statue Room Lower",
        "area_id": "21",
        "map_id": "17",
        "map_name": "Huge Statue Room",
        "exits": {
            "CP Palace Key Hall": None,
            "CP Huge Statue Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "CP Small Statue Room Upper",
        "area_id": "21",
        "map_id": "18",
        "map_name": "Small Statue Room",
        "events": {
            "MF_PRA_22_FoundHiddenRoomUnderStatue": None,
        },
        "locations": {
            "CP Small Statue Room Hidden Panel": CanFlipPanels(),
            "CP Small Statue Room Hidden Block": HasUltraBoots() & CanSeeHiddenBlocks(),
        },
        "exits": {
            "CP Mirrored Door Room North": None,
            "CP Small Statue Room Lower": None,
        }
    },
    {
        "region_name": "CP Small Statue Room Lower",
        "area_id": "21",
        "map_id": "18",
        "map_name": "Small Statue Room",
        "exits": {
            "CP P-Up, D-Down Hall": None,
            "CP Small Statue Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "CP Palace Key Room",
        "area_id": "21",
        "map_id": "19",
        "map_name": "Palace Key Room",
        "locations": {
            "CP Palace Key Room In Chest": CanClimbSteps(),
        },
        "exits": {
            "CP Palace Key Hall": None,
        }
    },
    {
        "region_name": "CP P-Up, D-Down Room",
        "area_id": "21",
        "map_id": "20",
        "map_name": "P-Up, D-Down Room",
        "locations": {
            "CP P-Up, D-Down Room In Chest": CanClimbSteps(),
        },
        "exits": {
            "CP P-Up, D-Down Hall": None,
        }
    },
    {
        "region_name": "CP Hidden Bridge Room South West",
        "area_id": "21",
        "map_id": "21",
        "map_name": "Hidden Bridge Room",
        "events": {
            "RF_PRA_29_ExtendedBridge": Has("RF_PRA_29_ExtendedBridge") | CanUseAbilityKooper(),
        },
        "exits": {
            "CP Mirrored Door Room South": None,
            "CP Hidden Bridge Room South East": Has("RF_PRA_29_ExtendedBridge"),
        }
    },
    {
        "region_name": "CP Hidden Bridge Room South East",
        "area_id": "21",
        "map_id": "21",
        "map_name": "Hidden Bridge Room",
        "events": {
            "RF_PRA_29_ExtendedBridge": Has("RF_PRA_29_ExtendedBridge") | CanHitGroundedSwitches(),
        },
        "exits": {
            "CP Mirror Hole Room": None,
            "CP Hidden Bridge Room South West": Has("RF_PRA_29_ExtendedBridge"),
        }
    },
    {
        "region_name": "CP Hidden Bridge Room North East",
        "area_id": "21",
        "map_id": "21",
        "map_name": "Hidden Bridge Room",
        "events": {
            "RF_PRA_29_ExtendedBridge": Has("RF_PRA_29_ExtendedBridge") | CanHitGroundedSwitches(),
        },
        "exits": {
            "CP Mirror Hole Room": None,
            "CP Hidden Bridge Room North West": None,
        }
    },
    {
        "region_name": "CP Hidden Bridge Room North West",
        "area_id": "21",
        "map_id": "21",
        "map_name": "Hidden Bridge Room",
        "events": {
            "RF_PRA_29_ExtendedBridge": Has("RF_PRA_29_ExtendedBridge") | CanUseAbilityKooper(),
        },
        "exits": {
            "CP Mirrored Door Room North": None,
            "CP Hidden Bridge Room North East": Has("RF_PRA_29_ExtendedBridge"),
        }
    },
    {
        "region_name": "CP Dino Puzzle Room",
        "area_id": "21",
        "map_id": "22",
        "map_name": "Dino Puzzle Room",
        "exits": {
            "CP Palace Boss Antechamber": None,
            "CP Mirror Hole Room": None,
        }
    },
    {
        "region_name": "CP Crystal Summit",
        "area_id": "21",
        "map_id": "23",
        "map_name": "Crystal Summit",
        "events": {
            "STARSPIRIT_7": None,
            "STARSPIRIT": None,
        },
        "exits": {
            "CP Palace Boss Antechamber": None,
        }
    },
    {
        "region_name": "CP Turnstyle Room North",
        "area_id": "21",
        "map_id": "24",
        "map_name": "Turnstyle Room",
        "exits": {
            "CP Triple Dip Room North": CanUseAbilityBombette(),
            "CP Turnstyle Room South": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "CP Turnstyle Room South",
        "area_id": "21",
        "map_id": "24",
        "map_name": "Turnstyle Room",
        "exits": {
            "CP Triple Dip Room South": CanUseAbilityBombette(),
            "CP Turnstyle Room North": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "CP Mirror Hole Room",
        "area_id": "21",
        "map_id": "25",
        "map_name": "Mirror Hole Room",
        "exits": {
            "CP Hidden Bridge Room North East": None,
            "CP Dino Puzzle Room": Has("Crystal Palace Key"),
            "CP Hidden Bridge Room South East": None,
        }
    },
    {
        "region_name": "CP Triple Dip Room North",
        "area_id": "21",
        "map_id": "26",
        "map_name": "Triple Dip Room",
        "locations": {
            "CP Triple Dip Room In Chest": None,
        },
        "exits": {
            "CP Turnstyle Room North": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "CP Triple Dip Room South",
        "area_id": "21",
        "map_id": "26",
        "map_name": "Triple Dip Room",
        "exits": {
            "CP Turnstyle Room South": None,
            "CP Reflection Mimic Room": None,
        }
    },
    {
        "region_name": "CP Palace Key Hall",
        "area_id": "21",
        "map_id": "27",
        "map_name": "Palace Key Hall",
        "exits": {
            "CP Huge Statue Room Lower": None,
            "CP Palace Key Room": None,
        }
    },
    {
        "region_name": "CP P-Up, D-Down Hall",
        "area_id": "21",
        "map_id": "28",
        "map_name": "P-Up, D-Down Hall",
        "exits": {
            "CP Small Statue Room Lower": None,
            "CP P-Up, D-Down Room": None,
        }
    },
    {
        "region_name": "CP Blue Key Hall",
        "area_id": "21",
        "map_id": "29",
        "map_name": "Blue Key Hall",
        "exits": {
            "CP Palace Save Room Upper": None,
            "CP Blue Key Room": None,
        }
    },
    {
        "region_name": "CP Shooting Star Hall",
        "area_id": "21",
        "map_id": "30",
        "map_name": "Shooting Star Hall",
        "exits": {
            "CP Reflected Save Room Upper": None,
            "CP Shooting Star Room": None,
        }
    },
    {
        "region_name": "CP Palace Boss Antechamber",
        "area_id": "21",
        "map_id": "31",
        "map_name": "Boss Antechamber",
        "exits": {
            "CP Dino Puzzle Room": None,
            "CP Crystal Summit": None,
        }
    }
]
