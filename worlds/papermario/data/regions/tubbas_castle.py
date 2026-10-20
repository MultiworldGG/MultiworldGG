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
    HasBoots,
    HasSuperBoots,
    #HasUltraBoots,
    #CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    #CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

tubbas_castle_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "TC Outside Tubbas Castle",
        "area_id": "15",
        "map_id": "0",
        "map_name": "Outside Tubbas Castle",
        "exits": {
            "GG Wasteland Ascent 2 East": None,
            "TC Great Hall 1F": None,
        }
    },
    {
        "region_name": "TC Great Hall 1F",
        "area_id": "15",
        "map_id": "1",
        "map_name": "Great Hall",
        "exits": {
            "TC Outside Tubbas Castle": None,
            "TC West Hall (1F)": CanUseAbilityBow(),
            "TC East Hall (1/2F) 1F": CanUseAbilityBow() & Has("Tubba Castle Key", count=1),
        }
    },
    {
        "region_name": "TC Great Hall 2F",
        "area_id": "15",
        "map_id": "1",
        "map_name": "Great Hall",
        "exits": {
            "TC West Hall (2F)": None,
            "TC East Hall (1/2F) 2F": None,
        }
    },
    {
        "region_name": "TC Great Hall 3F",
        "area_id": "15",
        "map_id": "1",
        "map_name": "Great Hall",
        "exits": {
            "TC Save Room (3F)": None,
            "TC Master Bedroom (3F)": None,
        }
    },
    {
        "region_name": "TC West Hall (1F)",
        "area_id": "15",
        "map_id": "2",
        "map_name": "West Hall (1F)",
        "exits": {
            "TC Table/Clock Room (1/2F) 1F": None,
            "TC Great Hall 1F": None,
            "TC Study (1F)": None,
            "TC Covered Tables Room (1F)": None,
        }
    },
    {
        "region_name": "TC Table/Clock Room (1/2F) 1F",
        "area_id": "15",
        "map_id": "3",
        "map_name": "Table/Clock Room (1/2F)",
        "exits": {
            "TC Stairs to Basement": None,
            "TC West Hall (1F)": None,
            "TC Stairs Above Basement": None,
        }
    },
    {
        "region_name": "TC Table/Clock Room (1/2F) 2F",
        "area_id": "15",
        "map_id": "3",
        "map_name": "Table/Clock Room (1/2F)",
        "locations": {
            "TC Table/Clock Room (1/2F) On Table": None,
        },
        "exits": {
            "TC Stairs to Third Floor": Has("Tubba Castle Key", count=2),
            "TC Table/Clock Room (1/2F) 1F": None,
            "TC West Hall (2F)": None,
            "TC Hidden Bedroom (2F)": None,
        }
    },
    {
        "region_name": "TC Stairs to Basement",
        "area_id": "15",
        "map_id": "4",
        "map_name": "Stairs to Basement",
        "locations": {
            "TC Stairs to Basement In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "TC Table/Clock Room (1/2F) 1F": None,
            "TC Tubba Basement Lower": None,
        }
    },
    {
        "region_name": "TC Stairs Above Basement",
        "area_id": "15",
        "map_id": "5",
        "map_name": "Stairs Above Basement",
        "exits": {
            "TC Table/Clock Room (1/2F) 1F": None,
            "TC Tubba Basement Upper": HasSuperBoots(),
        }
    },
    {
        "region_name": "TC Tubba Basement Upper",
        "area_id": "15",
        "map_id": "6",
        "map_name": "Basement",
        "locations": {
            "TC Basement In Chest": None,
        },
        "exits": {
            "TC Tubba Basement Lower": None,
        }
    },
    {
        "region_name": "TC Tubba Basement Lower",
        "area_id": "15",
        "map_id": "6",
        "map_name": "Basement",
        "exits": {
            "TC Stairs to Basement": None,
        }
    },
    {
        "region_name": "TC Study (1F)",
        "area_id": "15",
        "map_id": "7",
        "map_name": "Study (1F)",
        "locations": {
            "TC Study (1F) On Table": HasBoots(),
        },
        "exits": {
            "TC West Hall (1F)": None,
        }
    },
    {
        "region_name": "TC East Hall (1/2F) 2F",
        "area_id": "15",
        "map_id": "8",
        "map_name": "East Hall (1/2F)",
        "exits": {
            "TC Great Hall 2F": None,
            "TC East Hall (1/2F) 1F": CanUseAbilityBow(),
        }
    },
    {
        "region_name": "TC East Hall (1/2F) 1F",
        "area_id": "15",
        "map_id": "8",
        "map_name": "East Hall (1/2F)",
        "exits": {
            "TC Great Hall 1F": None,
            "TC East Hall (1/2F) 2F": CanUseAbilityBow(),
        }
    },
    {
        "region_name": "TC West Hall (2F)",
        "area_id": "15",
        "map_id": "9",
        "map_name": "West Hall (2F)",
        "exits": {
            "TC Table/Clock Room (1/2F) 2F": None,
            "TC Great Hall 2F": None,
            "TC Spike Trap Room (2F)": None,
            "TC Sealed Room (2F)": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "TC Sealed Room (2F)",
        "area_id": "15",
        "map_id": "10",
        "map_name": "Sealed Room (2F)",
        "events": {
            "GF_DGB10_BoardedFloor3": HasSuperBoots(),
        },
        "exits": {
            "TC West Hall (2F)": None,
            "TC Covered Tables Room (1F)": HasSuperBoots(),
            "TC Covered Tables Room (1F) On Table": HasSuperBoots(),
        }
    },
    {
        "region_name": "TC Covered Tables Room (1F)",
        "area_id": "15",
        "map_id": "11",
        "map_name": "Covered Tables Room (1F)",
        "exits": {
            "TC West Hall (1F)": None,
            "TC Sealed Room (2F)": Has("GF_DGB10_BoardedFloor3") & HasBoots(),
        }
    },
    {
        "region_name": "TC Covered Tables Room (1F) On Table",
        "area_id": "15",
        "map_id": "11",
        "map_name": "Covered Tables Room (1F)",
        "locations": {
            "TC Covered Tables Room (1F) On Table": CanUseAbilityParakarry(),
        },
        "exits": {
            "TC Covered Tables Room (1F)": None,
            "TC Sealed Room (2F)": Has("GF_DGB10_BoardedFloor3"),
        }
    },
    {
        "region_name": "TC Spike Trap Room (2F)",
        "area_id": "15",
        "map_id": "12",
        "map_name": "Spike Trap Room (2F)",
        "locations": {
            "TC Spike Trap Room (2F) In Chest": CanUseAbilityBow() | CanUseAbilityLakilester(),
        },
        "exits": {
            "TC West Hall (2F)": None,
        }
    },
    {
        "region_name": "TC Hidden Bedroom (2F)",
        "area_id": "15",
        "map_id": "13",
        "map_name": "Hidden Bedroom (2F)",
        "locations": {
            "TC Hidden Bedroom (2F) In Hidden Room": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 1": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 2": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 3": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 4": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 5": HasBoots() & CanUseAbilityParakarry(),
            "TC Hidden Bedroom (2F) On Bed 6": HasBoots() & CanUseAbilityParakarry(),
        },
        "exits": {
            "TC Table/Clock Room (1/2F) 2F": None,
        }
    },
    {
        "region_name": "TC Stairs to Third Floor",
        "area_id": "15",
        "map_id": "14",
        "map_name": "Stairs to Third Floor",
        "locations": {
            "TC Stairs to Third Floor Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "TC Table/Clock Room (1/2F) 2F": None,
            "TC West Hall (3F)": None,
        }
    },
    {
        "region_name": "TC West Hall (3F)",
        "area_id": "15",
        "map_id": "15",
        "map_name": "West Hall (3F)",
        "exits": {
            "TC Stairs to Third Floor": None,
            "TC Save Room (3F)": Has("Tubba Castle Key", count=3),
            "TC Sleeping Clubbas Room (3F)": None,
        }
    },
    {
        "region_name": "TC Sleeping Clubbas Room (3F)",
        "area_id": "15",
        "map_id": "16",
        "map_name": "Sleeping Clubbas Room (3F)",
        "locations": {
            "TC Sleeping Clubbas Room (3F) On Pedestal": CanClimbSteps(),
        },
        "exits": {
            "TC West Hall (3F)": None,
        }
    },
    {
        "region_name": "TC Save Room (3F)",
        "area_id": "15",
        "map_id": "17",
        "map_name": "Save Room (3F)",
        "exits": {
            "TC West Hall (3F)": None,
            "TC Great Hall 3F": None,
        }
    },
    {
        "region_name": "TC Master Bedroom (3F)",
        "area_id": "15",
        "map_id": "18",
        "map_name": "Master Bedroom (3F)",
        "events": {
            "MysticalKey": None,
        },
        "exits": {
            "TC Great Hall 3F": None,
        }
    }
]
