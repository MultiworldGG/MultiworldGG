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
    #CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    #CanClimbSteps,
    CanReenterVerticalPipes,
)

from ...options import OpenForest

forever_forest_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "FOR Flower Sounds",
        "area_id": "12",
        "map_id": "0",
        "map_name": "Flower Sounds",
        "exits": {
            "FOR Exit to Toad Town": None,
            "FOR Stump Eyes Entrance": None,
        }
    },
    {
        "region_name": "FOR Stump Eyes",
        "area_id": "12",
        "map_id": "1",
        "map_name": "Stump Eyes",
        "events": {
            "RF_ForestPass": None
        },
        "exits": {
            "FOR Flowers (Oaklie)": None,
            "FOR Stump Eyes Entrance": None,
            "FOR Flower Sounds": None,
        }
    },
    {
        "region_name": "FOR Stump Eyes Entrance",
        "area_id": "12",
        "map_id": "1",
        "map_name": "Stump Eyes",
        "exits": {
            "FOR Flower Sounds": None,
            "FOR Stump Eyes": Has(
                "Forest Pass",
                options=[OptionFilter(
                    OpenForest,
                    False
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "FOR Flowers (Oaklie)",
        "area_id": "12",
        "map_id": "2",
        "map_name": "Flowers (Oaklie)",
        "exits": {
            "FOR Flower Sounds": None,
            "FOR Tree Face (Bub-ulb)": None,
            "FOR Stump Eyes": None,
        }
    },
    {
        "region_name": "FOR Tree Face (Bub-ulb)",
        "area_id": "12",
        "map_id": "3",
        "map_name": "Tree Face (Bub-ulb)",
        "locations": {
            "FOR Tree Face (Bub-ulb) Bub-ulb Gift": None,
        },
        "exits": {
            "FOR Mushrooms (Path Splits)": None,
            "FOR Flower Sounds": None,
            "FOR Flowers (Oaklie)": None,
        }
    },
    {
        "region_name": "FOR Mushrooms (Path Splits)",
        "area_id": "12",
        "map_id": "4",
        "map_name": "Mushrooms (Path Splits)",
        "exits": {
            "FOR Flower Sounds": None,
            "FOR Flowers Vanish": None,
            "FOR Tree Face (Bub-ulb)": None,
            "FOR Bee Hive (HP Plus)": None,
        }
    },
    {
        "region_name": "FOR Flowers Vanish",
        "area_id": "12",
        "map_id": "5",
        "map_name": "Flowers Vanish",
        "exits": {
            "FOR Laughing Rock": None,
            "FOR Flower Sounds": None,
            "FOR Mushrooms (Path Splits)": None,
        }
    },
    {
        "region_name": "FOR Laughing Rock",
        "area_id": "12",
        "map_id": "6",
        "map_name": "Laughing Rock",
        "exits": {
            "FOR Flowers Appear (FP Plus)": None,
            "FOR Flower Sounds": None,
            "FOR Flowers Vanish": None,
            "FOR Outside Boo's Mansion": None,
        }
    },
    {
        "region_name": "FOR Bee Hive (HP Plus)",
        "area_id": "12",
        "map_id": "7",
        "map_name": "Bee Hive (HP Plus)",
        "locations": {
            "FOR Bee Hive (HP Plus) Central Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "FOR Flower Sounds": None,
            "FOR Mushrooms (Path Splits)": None,
        }
    },
    {
        "region_name": "FOR Flowers Appear (FP Plus)",
        "area_id": "12",
        "map_id": "8",
        "map_name": "Flowers Appear (FP Plus)",
        "locations": {
            "FOR Flowers Appear (FP Plus) Central Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "FOR Laughing Rock": None,
            "FOR Flower Sounds": None,
        }
    },
    {
        "region_name": "FOR Exit to Toad Town",
        "area_id": "12",
        "map_id": "9",
        "map_name": "Exit to Toad Town",
        "exits": {
            "TT Southern District": None,
            "FOR Flower Sounds": None,
        }
    },
    {
        "region_name": "FOR Outside Boo's Mansion",
        "area_id": "12",
        "map_id": "10",
        "map_name": "Outside Boo's Mansion",
        "locations": {
            "FOR Outside Boo's Mansion Yellow Block": CanHitFloatingBlocks(),
            "FOR Outside Boo's Mansion In Bush (Back Right)": None
        },
        "exits": {
            "FOR Laughing Rock": Has("Forest Pass") | Has("RF_ForestPass"),
            "FOR Exit to Gusty Gulch West": None,
            "FOR Outside Boo's Mansion Pipe": Has("GF_TIK09_WarpPipe") & HasBoots(),
            "FOR Outside Boo's Mansion Steps": HasBoots(),
        }
    },
    {
        "region_name": "FOR Outside Boo's Mansion Steps",
        "area_id": "12",
        "map_id": "10",
        "map_name": "Outside Boo's Mansion",
        "exits": {
            "FOR Outside Boo's Mansion": None,
            "BM Foyer 1F": None,
        }
    },
    {
        "region_name": "FOR Outside Boo's Mansion Pipe",
        "area_id": "12",
        "map_id": "10",
        "map_name": "Outside Boo's Mansion",
        "exits": {
            "TTT Warp Zone 2 (B2) Pipe": CanReenterVerticalPipes(),
            "FOR Outside Boo's Mansion": None,
        }
    },
    {
        "region_name": "FOR Exit to Gusty Gulch West",
        "area_id": "12",
        "map_id": "11",
        "map_name": "Exit to Gusty Gulch",
        "exits": {
            "FOR Outside Boo's Mansion": None,
            "FOR Exit to Gusty Gulch East": Has("RF_OpenedGustyGulch"),
        }
    },
    {
        "region_name": "FOR Exit to Gusty Gulch East",
        "area_id": "12",
        "map_id": "11",
        "map_name": "Exit to Gusty Gulch",
        "locations": {
            "FOR Exit to Gusty Gulch Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "GG Windmill Exterior": None,
            "FOR Exit to Gusty Gulch West": Has("RF_OpenedGustyGulch"),
        }
    }
]
