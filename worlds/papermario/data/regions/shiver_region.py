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
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

shiver_region_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "SR Shiver City Mayor Area",
        "area_id": "20",
        "map_id": "0",
        "map_name": "Shiver City Mayor Area",
        "events": {
            "RF_Ch7_MurderMysteryStarted": None,
            "RF_Ch7_MurderMysterySolved": Has("RF_Ch7_SpokeWithHerringway"),
            "StarPiece_SAM_1": None,
            "StarPiece_SAM_8": None,
        },
        "locations": {
            "SR Shiver City Mayor Area Hidden Panel": CanFlipPanels() & Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Mayor Area Mayor Penguin Gift": (
                HasAll("RF_Ch7_MurderMysterySolved", "RF_Ch7_GotSnowmanScarf")
            ),
            "SR Shiver City Mayor Area Mayor Penguin Letter Reward": (
                CanUseAbilityParakarry() & Has("Letter to Mayor Penguin")
            ),
            "SR Shiver City Mayor Area Chest In House": HasBoots(),
        },
        "exits": {
            "SR Shiver City Center": None,
        }
    },
    {
        "region_name": "SR Shiver City Center",
        "area_id": "20",
        "map_id": "1",
        "map_name": "Shiver City Center",
        "events": {
            "StarPiece_SAM_1": None,
            "StarPiece_SAM_8": None,
        },
        "locations": {
            "SR Shiver City Center Toad House Breakfast": None,
            "SR Shiver City Center Snowmen Gift 1": Has("MF_SAM_04_UnlockedShiverMountain"),
            "SR Shiver City Center Snowmen Gift 2": Has("MF_SAM_04_UnlockedShiverMountain"),
            "SR Shiver City Center Snowmen Gift 3": Has("MF_SAM_04_UnlockedShiverMountain"),
            "SR Shiver City Center Snowmen Gift 4": Has("MF_SAM_04_UnlockedShiverMountain"),
            "SR Shiver City Center Snowmen Gift 5": Has("MF_SAM_04_UnlockedShiverMountain"),
            "SR Shiver City Center Shop Item 1": Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Center Shop Item 2": Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Center Shop Item 3": Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Center Shop Item 4": Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Center Shop Item 5": Has("RF_Ch7_MurderMysterySolved"),
            "SR Shiver City Center Shop Item 6": Has("RF_Ch7_MurderMysterySolved"),
        },
        "exits": {
            "SR Shiver City Mayor Area": None,
            "SR Shiver City Pond Area": None,
            "SR Shiver City Center Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "SR Shiver City Center Pipe",
        "area_id": "20",
        "map_id": "1",
        "map_name": "Shiver City Center",
        "exits": {
            "TTT Frozen Room (B3) East Pipe": CanReenterVerticalPipes(),
            "SR Shiver City Center": None,
        }
    },
    {
        "region_name": "SR Road to Shiver Snowfield",
        "area_id": "20",
        "map_id": "2",
        "map_name": "Road to Shiver Snowfield",
        "exits": {
            "SR Shiver City Pond Area": None,
            "SR Shiver Snowfield": None,
        }
    },
    {
        "region_name": "SR Shiver Snowfield",
        "area_id": "20",
        "map_id": "3",
        "map_name": "Shiver Snowfield",
        "events": {
            "MF_SAM_04_UnlockedShiverMountain": HasAll("Snowman Bucket", "Snowman Scarf"),
        },
        "locations": {
            "SR Shiver Snowfield Hidden Panel": CanFlipPanels(),
            "SR Shiver Snowfield In Tree Left": HasHammer(),
            "SR Shiver Snowfield Behind Tree Right": None,
        },
        "exits": {
            "SR Road to Shiver Snowfield": None,
            "SR Path to Starborn Valley West": None,
            "SR Shiver Mountain Passage West": Has("MF_SAM_04_UnlockedShiverMountain"),
        }
    },
    {
        "region_name": "SR Path to Starborn Valley West",
        "area_id": "20",
        "map_id": "4",
        "map_name": "Path to Starborn Valley",
        "locations": {
            "SR Path to Starborn Valley Behind Icicle": None,
        },
        "exits": {
            "SR Shiver Snowfield": None,
            "SR Path to Starborn Valley East": CanClimbSteps(),
        }
    },
    {
        "region_name": "SR Path to Starborn Valley East",
        "area_id": "20",
        "map_id": "4",
        "map_name": "Path to Starborn Valley",
        "locations": {
            "SR Path to Starborn Valley Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SR Starborn Valley": None,
            "SR Path to Starborn Valley West": None,
        }
    },
    {
        "region_name": "SR Starborn Valley",
        "area_id": "20",
        "map_id": "5",
        "map_name": "Starborn Valley",
        "events": {
            "RF_Ch7_GotSnowmanScarf": CanClimbSteps(),
        },
        "locations": {
            "SR Starborn Valley Merle Gift": CanClimbSteps(),
            "SR Starborn Valley Frost T. Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Frost T")
            ),
        },
        "exits": {
            "SR Path to Starborn Valley East": None,
        }
    },
    {
        "region_name": "SR Shiver Mountain Passage West",
        "area_id": "20",
        "map_id": "6",
        "map_name": "Shiver Mountain Passage",
        "exits": {
            "SR Shiver Snowfield": None,
            "SR Shiver Mountain Passage East": HasSuperBoots(),
        }
    },
    {
        "region_name": "SR Shiver Mountain Passage East",
        "area_id": "20",
        "map_id": "6",
        "map_name": "Shiver Mountain Passage",
        "locations": {
            "SR Shiver Mountain Passage Hidden Block": CanSeeHiddenBlocks() & HasUltraBoots(),
        },
        "exits": {
            "SR Shiver Mountain Hills West": None,
            "SR Shiver Mountain Passage West": HasSuperBoots(),
        }
    },
    {
        "region_name": "SR Shiver Mountain Hills West",
        "area_id": "20",
        "map_id": "7",
        "map_name": "Shiver Mountain Hills",
        "events": {
            "RF_DefeatedFirstDuplighost": CanUseAbilityKooper() & HasHammer(),
        },
        "locations": {
            "SR Shiver Mountain Hills Bottom Path": CanClimbSteps(),
        },
        "exits": {
            "SR Shiver Mountain Passage East": None,
            "SR Shiver Mountain Hills East": CanClimbSteps() & Has("RF_DefeatedFirstDuplighost"),
        }
    },
    {
        "region_name": "SR Shiver Mountain Hills East",
        "area_id": "20",
        "map_id": "7",
        "map_name": "Shiver Mountain Hills",
        "events": {
            "RF_DefeatedFirstDuplighost": HasHammer(),
        },
        "locations": {
            "SR Shiver Mountain Hills In SuperBlock": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SR Shiver Mountain Tunnel": None,
            "SR Shiver Mountain Hills West": CanClimbSteps() | Has("RF_DefeatedFirstDuplighost"),
        }
    },
    {
        "region_name": "SR Shiver Mountain Tunnel",
        "area_id": "20",
        "map_id": "8",
        "map_name": "Shiver Mountain Tunnel",
        "locations": {
            "SR Shiver Mountain Tunnel Socket 1": None,
            "SR Shiver Mountain Tunnel Socket 2": None,
            "SR Shiver Mountain Tunnel Socket 3": None,
        },
        "exits": {
            "SR Shiver Mountain Hills East": None,
            "SR Shiver Mountain Peaks Bottom": None,
        }
    },
    {
        "region_name": "SR Shiver Mountain Peaks Bottom",
        "area_id": "20",
        "map_id": "9",
        "map_name": "Shiver Mountain Peaks",
        "exits": {
            "SR Shiver Mountain Tunnel": None,
            "SR Shiver Mountain Peaks": Has("Star Stone") & CanClimbSteps(),
            "SR Merlar's Sanctuary": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "SR Shiver Mountain Peaks",
        "area_id": "20",
        "map_id": "9",
        "map_name": "Shiver Mountain Peaks",
        "locations": {
            "SR Shiver Mountain Peaks Red Block": CanHitFloatingBlocks(),
            "SR Shiver Mountain Peaks Left Ledge": None,
        },
        "exits": {
            "CP Palace Entrance South": None,
            "SR Shiver Mountain Peaks Bottom": None,
        }
    },
    {
        "region_name": "SR Shiver City Pond Area",
        "area_id": "20",
        "map_id": "10",
        "map_name": "Shiver City Pond Area",
        "events": {
            "RF_Ch7_SpokeWithHerringway": (
                Has("Warehouse Key")
                & Has("RF_Ch7_MurderMysteryStarted")
                & HasBoots()
            ),
            "StarPiece_SAM_1": None,
            "StarPiece_SAM_8": None,
        },
        "locations": {
            "SR Shiver City Pond Area In Frozen Pond": (
                (CanUseAbilityBombette() | HasSuperBoots())
                & CanUseAbilitySushie()
                & Has("RF_Ch7_MurderMysteryStarted")
            ),
        },
        "exits": {
            "SR Shiver City Center": None,
            "SR Road to Shiver Snowfield": Has("RF_Ch7_MurderMysterySolved"),
        }
    },
    {
        "region_name": "SR Merlar's Sanctuary",
        "area_id": "20",
        "map_id": "11",
        "map_name": "Merlar's Sanctuary",
        "locations": {
            "SR Merlar's Sanctuary On Pedestal": CanClimbSteps(),
        },
        "exits": {
            "SR Shiver Mountain Peaks Bottom": None,
        }
    }
]
