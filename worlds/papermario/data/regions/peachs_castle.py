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
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    #CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

peachs_castle_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "PC Entry Hall (1F)",
        "area_id": "4",
        "map_id": "4",
        "map_name": "Entry Hall (1F)",
        "exits": {
            "PCG Hijacked Castle Entrance": None,
            "PC Upper Hall (2F)": None,
            "PC Inactive Quiz-Off (1F)": None,
            "PC Kitchen (1F)": None,
            "PC Guest Room (1F)": None,
        }
    },
    {
        "region_name": "PC Upper Hall (2F)",
        "area_id": "4",
        "map_id": "5",
        "map_name": "Upper Hall (2F)",
        "exits": {
            "PC Entry Hall (1F)": None,
            "PC Stairs Hallway (3F)": None,
            "PC Library (2F)": None,
            "PC Passage Outlet (2F)": None,
            "PC Peach's Room (2F)": None,
            "PC Storeroom (2F)": None,
            "PC Dining Room (2F)": None,
        }
    },
    {
        "region_name": "PC Stairs Hallway (3F)",
        "area_id": "4",
        "map_id": "6",
        "map_name": "Stairs Hallway (3F)",
        "exits": {
            "PC Upper Hall (2F)": None,
            "PC Window Hallway (4F)": None,
        }
    },
    {
        "region_name": "PC Window Hallway (4F)",
        "area_id": "4",
        "map_id": "7",
        "map_name": "Window Hallway (4F)",
        "exits": {
            "PC Stairs Hallway (3F)": Has("Star Beam"),
            "PC Double Staircase (4F)": Has("Star Beam"),
        }
    },
    {
        "region_name": "PC Peach's Room (2F)",
        "area_id": "4",
        "map_id": "8",
        "map_name": "Peach's Room (2F)",
        "exits": {
            "PC Upper Hall (2F)": None,
            "PC Balcony (2F)": None,
        }
    },
    {
        "region_name": "PC Passage Outlet (2F)",
        "area_id": "4",
        "map_id": "9",
        "map_name": "Passage Outlet (2F)",
        "exits": {
            "PC Upper Hall (2F)": None,
        }
    },
    {
        "region_name": "PC Library (2F)",
        "area_id": "4",
        "map_id": "10",
        "map_name": "Library (2F)",
        "locations": {
            "PC Library (2F) Upper Level": CanClimbSteps(),
            "PC Library (2F) Between Bookshelves": None,
        },
        "exits": {
            "PC Upper Hall (2F)": None,
        }
    },
    {
        "region_name": "PC Storeroom (2F)",
        "area_id": "4",
        "map_id": "11",
        "map_name": "Storeroom (2F)",
        "locations": {
            "PC Storeroom (2F) On The Ground": None,
        },
        "exits": {
            "PC Upper Hall (2F)": None,
        }
    },
    {
        "region_name": "PC Dining Room (2F)",
        "area_id": "4",
        "map_id": "12",
        "map_name": "Dining Room (2F)",
        "exits": {
            "PC Upper Hall (2F)": None,
        }
    },
    {
        "region_name": "PC Kitchen (1F)",
        "area_id": "4",
        "map_id": "13",
        "map_name": "Kitchen (1F)",
        "exits": {
            "PC Entry Hall (1F)": None,
        }
    },
    {
        "region_name": "PC Guest Room (1F)",
        "area_id": "4",
        "map_id": "14",
        "map_name": "Guest Room (1F)",
        "locations": {
            "PC Guest Room (1F) In Chest": None,
        },
        "exits": {
            "PC Entry Hall (1F)": None,
        }
    },
    {
        "region_name": "PC Inactive Quiz-Off (1F)",
        "area_id": "4",
        "map_id": "15",
        "map_name": "Inactive Quiz-Off (1F)",
        "exits": {
            "PC Entry Hall (1F)": None,
        }
    },
    {
        "region_name": "PC Double Staircase (4F)",
        "area_id": "4",
        "map_id": "16",
        "map_name": "Double Staircase (4F)",
        "exits": {
            "PC Window Hallway (4F)": None,
            "PC Rooftop (5F)": None,
        }
    },
    {
        "region_name": "PC Rooftop (5F)",
        "area_id": "4",
        "map_id": "17",
        "map_name": "Rooftop (5F)",
        "exits": {
            "PC Double Staircase (4F)": None,
            "PC Tower Staircase (5F)": None,
        }
    },
    {
        "region_name": "PC Tower Staircase (5F)",
        "area_id": "4",
        "map_id": "18",
        "map_name": "Tower Staircase (5F)",
        "exits": {
            "PC Rooftop (5F)": None,
            "PC Final Boss Arena (6F)": None,
        }
    },
    {
        "region_name": "PC Final Boss Arena (6F)",
        "area_id": "4",
        "map_id": "19",
        "map_name": "Final Boss Arena (6F)",
        "events": {
            "STARROD": Has("Star Beam"),
        },
        "exits": {
            "PC Tower Staircase (5F)": None,
        }
    },
    {
        "region_name": "PC Balcony (2F)",
        "area_id": "4",
        "map_id": "20",
        "map_name": "Balcony (2F)",
        "exits": {
            "PC Peach's Room (2F)": None,
        }
    }
]
