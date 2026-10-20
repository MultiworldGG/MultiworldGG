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

koopa_bros_fortress_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "KBF Fortress Exterior",
        "area_id": "7",
        "map_id": "0",
        "map_name": "Fortress Exterior",
        "exits": {
            "KR Path to Fortress 2": None,
            "KBF Left Tower 1F": None,
        }
    },
    {
        "region_name": "KBF Fortress Exterior South",
        "area_id": "7",
        "map_id": "0",
        "map_name": "Fortress Exterior",
        "exits": {
            "KBF Right Tower": None,
        }
    },
    {
        "region_name": "KBF Fortress Exterior East",
        "area_id": "7",
        "map_id": "0",
        "map_name": "Fortress Exterior",
        "locations": {
            "KBF Fortress Exterior Chest Behind Fortress": None,
        },
        "exits": {
            "KBF Right Tower": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "KBF Fortress Exterior Upper",
        "area_id": "7",
        "map_id": "0",
        "map_name": "Fortress Exterior",
        "locations": {
            "KBF Fortress Exterior Chest On Ledge": None,
        },
        "exits": {
            "KR Path to Fortress 2 Upper": None,
        }
    },
    {
        "region_name": "KBF Left Tower 1F",
        "area_id": "7",
        "map_id": "1",
        "map_name": "Left Tower",
        "locations": {
            "KBF Left Tower Koopa Troopa Reward": None,
        },
        "exits": {
            "KBF Fortress Exterior": None,
            "KBF Left Stairway 1F": Has("Koopa Fortress Key", count=1),
        }
    },
    {
        "region_name": "KBF Left Tower 2F",
        "area_id": "7",
        "map_id": "1",
        "map_name": "Left Tower",
        "events": {
            "MF_TRD01_RaisedStairs": CanHitGroundedSwitches(),
        },
        "exits": {
            "KBF Left Stairway 2F": None,
            "KBF Left Tower 3F": Has("MF_TRD01_RaisedStairs"),
        }
    },
    {
        "region_name": "KBF Left Tower 3F",
        "area_id": "7",
        "map_id": "1",
        "map_name": "Left Tower",
        "locations": {
            "KBF Left Tower Top Of Tower": CanClimbSteps(),
        },
        "exits": {
            "KBF Left Tower 2F": Has("MF_TRD01_RaisedStairs"),
            "KBF Fortress Battlement West Door": None,
        }
    },
    {
        "region_name": "KBF Left Stairway 1F",
        "area_id": "7",
        "map_id": "2",
        "map_name": "Left Stairway",
        "exits": {
            "KBF Left Tower 1F": None,
            "KBF Central Hall 1F": None,
            "KBF Left Stairway 1F Platform": Has("MF_TRD02_LoweredStairs") & HasBoots(),
            "KBF Left Stairway 2F": Has("MF_TRD02_LoweredStairs") & HasBoots(),
        }
    },
    {
        "region_name": "KBF Left Stairway 2F",
        "area_id": "7",
        "map_id": "2",
        "map_name": "Left Stairway",
        "events": {
            "MF_TRD02_LoweredStairs": CanHitGroundedBlocks(),
        },
        "exits": {
            "KBF Left Tower 2F": Has("Koopa Fortress Key", count=4),
            "KBF Central Hall 2F Left Door": None,
            "KBF Left Stairway 1F": Has("MF_TRD02_LoweredStairs"),
            "KBF Left Stairway 1F Platform": Has("MF_TRD02_LoweredStairs") & CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Left Stairway 1F Platform",
        "area_id": "7",
        "map_id": "2",
        "map_name": "Left Stairway",
        "events": {
            "RF_TRD_02_OpenedLeftJail": CanUseAbilityBombette(),
        },
        "exits": {
            "KBF Central Hall 1F Left Jail": Has("RF_TRD_02_OpenedLeftJail"),
            "KBF Left Stairway 1F": None,
            "KBF Left Stairway 2F": Has("MF_TRD02_LoweredStairs") & CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Central Hall 1F Left Jail",
        "area_id": "7",
        "map_id": "3",
        "map_name": "Central Hall",
        "locations": {
            "KBF Central Hall Left Cell": None,
        },
        "exits": {
            "KBF Left Stairway 1F Platform": CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Central Hall 1F",
        "area_id": "7",
        "map_id": "3",
        "map_name": "Central Hall",
        "locations": {
            "KBF Central Hall Center Cell": None,
            "KBF Central Hall Right Cell": CanUseAbilityBombette(),
        },
        "exits": {
            "KBF Left Stairway 1F": None,
            "KBF Right Starway 1F": None,
        }
    },
    {
        "region_name": "KBF Central Hall 2F Left Door",
        "area_id": "7",
        "map_id": "3",
        "map_name": "Central Hall",
        "exits": {
            "KBF Left Stairway 2F": CanClimbSteps(),
            "KBF Central Hall 2F Right Door": (
                CanClimbSteps()
                & (CanUseAbilityKooper() | CanUseAbilityParakarry())
            ),
            "KBF Central Hall 1F": None,
        }
    },
    {
        "region_name": "KBF Central Hall 2F Right Door",
        "area_id": "7",
        "map_id": "3",
        "map_name": "Central Hall",
        "exits": {
            "KBF Right Starway 2F": CanClimbSteps(),
            "KBF Central Hall 2F Left Door": (
                CanClimbSteps()
                & (CanUseAbilityKooper() | CanUseAbilityParakarry())
            ),
            "KBF Central Hall 1F": None,
        }
    },
    {
        "region_name": "KBF Right Starway 1F",
        "area_id": "7",
        "map_id": "4",
        "map_name": "Right Starway",
        "events": {
            "MF_TRD04_LoweredStairs": CanHitGroundedSwitches(),
        },
        "exits": {
            "KBF Central Hall 1F": None,
            "KBF Right Tower": Has("Koopa Fortress Key", count=2),
            "KBF Right Starway B1F": Has("MF_TRD04_LoweredStairs"),
        }
    },
    {
        "region_name": "KBF Right Starway B1F",
        "area_id": "7",
        "map_id": "4",
        "map_name": "Right Starway",
        "events": {
            "MF_TRD04_LoweredStairs": None,
        },
        "exits": {
            "KBF Dungeon Trap": None,
            "KBF Fortress Jail Outer": None,
            "KBF Right Starway 1F": Has("MF_TRD04_LoweredStairs") & CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Right Starway 2F",
        "area_id": "7",
        "map_id": "4",
        "map_name": "Right Starway",
        "exits": {
            "KBF Central Hall 2F Right Door": Has("Koopa Fortress Key", count=3),
            "KBF Right Tower": None,
        }
    },
    {
        "region_name": "KBF Right Tower",
        "area_id": "7",
        "map_id": "5",
        "map_name": "Right Tower",
        "exits": {
            "KBF Right Starway 1F": None,
            "KBF Fortress Exterior South": None,
            "KBF Fortress Exterior East": CanUseAbilityBombette(),
            "KBF Right Starway 2F": None,
            "KBF Fortress Jail Inner": CanHitFloatingBlocks(),
        }
    },
    {
        "region_name": "KBF Fortress Jail Outer",
        "area_id": "7",
        "map_id": "6",
        "map_name": "Jail",
        "exits": {
            "KBF Right Starway B1F": None,
            "KBF Fortress Jail Inner": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "KBF Fortress Jail Inner",
        "area_id": "7",
        "map_id": "6",
        "map_name": "Jail",
        "locations": {
            "KBF Jail Bombette Partner": None
        },
        "exits": {
            "KBF Fortress Jail Outer": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "KBF Dungeon Trap",
        "area_id": "7",
        "map_id": "7",
        "map_name": "Dungeon Trap",
        "exits": {
            "KBF Right Starway B1F": None,
            "KBF Dungeon Fire Room": None,
        }
    },
    {
        "region_name": "KBF Dungeon Fire Room",
        "area_id": "7",
        "map_id": "8",
        "map_name": "Dungeon Fire Room",
        "locations": {
            "KBF Dungeon Fire Room On The Ground": CanClimbSteps(),
        },
        "exits": {
            "KBF Dungeon Trap": None,
        }
    },
    {
        "region_name": "KBF Fortress Battlement West Door",
        "area_id": "7",
        "map_id": "9",
        "map_name": "Battlement",
        "exits": {
            "KBF Left Tower 3F": None,
            "KBF Fortress Battlement": CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Fortress Battlement East Door",
        "area_id": "7",
        "map_id": "9",
        "map_name": "Battlement",
        "exits": {
            "KBF Boss Battle Room": None,
            "KBF Fortress Battlement": CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Fortress Battlement",
        "area_id": "7",
        "map_id": "9",
        "map_name": "Battlement",
        "exits": {
            "KBF Fortress Battlement Rock": None,
            "KBF Fortress Battlement West Door": CanClimbSteps(),
            "KBF Fortress Battlement East Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "KBF Fortress Battlement Rock",
        "area_id": "7",
        "map_id": "9",
        "map_name": "Battlement",
        "locations": {
            "KBF Battlement Block Behind Rock": CanUseAbilityBombette() & CanHitFloatingBlocks(),
        },
        "exits": {
            "KBF Fortress Battlement": HasBoots(),
        }
    },
    {
        "region_name": "KBF Boss Battle Room",
        "area_id": "7",
        "map_id": "10",
        "map_name": "Boss Battle Room",
        "events": {
            # primitive battle logic
            "STARSPIRIT_1": HasHammer() | Has("Bombette") | Has("Watt"),
            "STARSPIRIT": HasHammer() | Has("Bombette") | Has("Watt"),
            "MF_Ch1_RescuedStarSpirit": HasHammer() | Has("Bombette") | Has("Watt"),
        },
        "exits": {
            "KBF Fortress Battlement East Door": None,
        }
    }
]
