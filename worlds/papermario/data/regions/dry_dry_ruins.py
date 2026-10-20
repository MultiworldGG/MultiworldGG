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
    OptionFilter,
)

from .LogicHelpers import (
    #HasHammer,
    HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    #CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    #CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

from ...options import GearShuffleMode

dry_dry_ruins_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "DDR Ruins Entrance",
        "area_id": "11",
        "map_id": "0",
        "map_name": "Entrance",
        "exits": {
            "DDD N3W1 Ruins Entrance": None,
            "DDR Sarcophagus Hall 1": None,
        }
    },
    {
        "region_name": "DDR Sarcophagus Hall 1",
        "area_id": "11",
        "map_id": "1",
        "map_name": "Sarcophagus Hall 1",
        "locations": {
            "DDR Sarcophagus Hall 1 In Sarcophagus": None,
        },
        "exits": {
            "DDR Ruins Entrance": None,
            "DDR Sarcophagus Hall 1 Upper Door": CanClimbSteps(),
            "DDR Sarcophagus Hall 1 Lower Door": None,
        }
    },
    {
        "region_name": "DDR Sarcophagus Hall 1 Upper Door",
        "area_id": "11",
        "map_id": "1",
        "map_name": "Sarcophagus Hall 1",
        "exits": {
            "DDR Sand Drainage Room 1 2F": Has("Ruins Key", count=1),
            "DDR Sarcophagus Hall 1": None,
        }
    },
    {
        "region_name": "DDR Sarcophagus Hall 1 Lower Door",
        "area_id": "11",
        "map_id": "1",
        "map_name": "Sarcophagus Hall 1",
        "exits": {
            "DDR Sand Drainage Room 1 1F": None,
            "DDR Sarcophagus Hall 1": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 1 2F",
        "area_id": "11",
        "map_id": "2",
        "map_name": "Sand Drainage Room 1",
        "events": {
            "MF_ISK03_DrainedFirstSandRoom": CanClimbSteps(),
        },
        "exits": {
            "DDR Sarcophagus Hall 1 Upper Door": None,
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 1 1F",
        "area_id": "11",
        "map_id": "2",
        "map_name": "Sand Drainage Room 1",
        "locations": {
            "DDR Sand Drainage Room 1 On The Ground": (
                CanClimbSteps()
                | Has("MF_ISK03_DrainedFirstSandRoom")
            ),
        },
        "exits": {
            "DDR Sarcophagus Hall 1 Lower Door": None,
            "DDR Descending Stairs 1 1F": Has("MF_ISK03_DrainedFirstSandRoom") & HasBoots(),
        }
    },
    {
        "region_name": "DDR Descending Stairs 1 1F",
        "area_id": "11",
        "map_id": "3",
        "map_name": "Descending Stairs 1",
        "exits": {
            "DDR Sand Drainage Room 1 1F": None,
            "DDR Sand Drainage Room 2 1F": None,
            "DDR Descending Stairs 1 B2F Door": None,
            "DDR Descending Stairs 1 2F Door": CanUseAbilityParakarry(),
            "DDR Descending Stairs 1 B1F Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Descending Stairs 1 B2F Door",
        "area_id": "11",
        "map_id": "3",
        "map_name": "Descending Stairs 1",
        "exits": {
            "DDR Sarcophagus Hall 2 East Door": Has("Ruins Key", count=2),
            "DDR Descending Stairs 1 1F": CanClimbSteps(),
            "DDR Descending Stairs 1 B1F Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Descending Stairs 1 2F Door",
        "area_id": "11",
        "map_id": "3",
        "map_name": "Descending Stairs 1",
        "exits": {
            "DDR Sand Drainage Room 2 2F": CanUseAbilityBombette(),
            "DDR Descending Stairs 1 1F": None,
        }
    },
    {
        "region_name": "DDR Descending Stairs 1 B1F Door",
        "area_id": "11",
        "map_id": "3",
        "map_name": "Descending Stairs 1",
        "exits": {
            "DDR Pyramid Stone Room": None,
            "DDR Descending Stairs 1 1F": CanClimbSteps(),
            "DDR Descending Stairs 1 B2F Door": None,
        }
    },
    {
        "region_name": "DDR Pyramid Stone Room",
        "area_id": "11",
        "map_id": "4",
        "map_name": "Pyramid Stone Room",
        "locations": {
            "DDR Pyramid Stone Room On Pedestal": (
                (Has("RF_ISK09_OpenedHammerChest") | HasSuperHammer())
                & CanClimbSteps()
            ),
        },
        "exits": {
            "DDR Descending Stairs 1 B1F Door": None,
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 2 2F",
        "area_id": "11",
        "map_id": "5",
        "map_name": "Sand Drainage Room 2",
        "events": {
            "MF_ISK06_DrainedSecondSandRoom": CanClimbSteps(),
        },
        "locations": {
            "DDR Sand Drainage Room 2 In The Sand": Has("MF_ISK06_DrainedSecondSandRoom"),
        },
        "exits": {
            "DDR Descending Stairs 1 2F Door": None,
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 2 1F",
        "area_id": "11",
        "map_id": "5",
        "map_name": "Sand Drainage Room 2",
        "locations": {
            "DDR Sand Drainage Room 2 On Ledge": Has("MF_ISK06_DrainedSecondSandRoom"),
        },
        "exits": {
            "DDR Descending Stairs 1 1F": None,
        }
    },
    {
        "region_name": "DDR Sarcophagus Hall 2 East Door",
        "area_id": "11",
        "map_id": "6",
        "map_name": "Sarcophagus Hall 2",
        "exits": {
            "DDR Descending Stairs 1 B2F Door": None,
            "DDR Sarcophagus Hall 2": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Sarcophagus Hall 2",
        "area_id": "11",
        "map_id": "6",
        "map_name": "Sarcophagus Hall 2",
        "locations": {
            "DDR Sarcophagus Hall 2 Pokey Gauntlet Reward": CanHitFloatingBlocks(),
            "DDR Sarcophagus Hall 2 Behind Hammer Block": (
                (Has("RF_ISK09_OpenedHammerChest") | HasSuperHammer())
                & CanClimbSteps()
            ),
        },
        "exits": {
            "DDR Descending Stairs 2 B2F East Door": Has("Ruins Key", count=3),
            "DDR Sarcophagus Hall 2 East Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Descending Stairs 2 B2F East Door",
        "area_id": "11",
        "map_id": "7",
        "map_name": "Descending Stairs 2",
        "exits": {
            "DDR Descending Stairs 2 B2F West Door": CanUseAbilityParakarry(),
            "DDR Descending Stairs 2 B3F": CanClimbSteps(),
            "DDR Sarcophagus Hall 2": None,
        }
    },
    {
        "region_name": "DDR Descending Stairs 2 B2F West Door",
        "area_id": "11",
        "map_id": "7",
        "map_name": "Descending Stairs 2",
        "exits": {
            "DDR Super Hammer Room": None,
        }
    },
    {
        "region_name": "DDR Descending Stairs 2 B3F",
        "area_id": "11",
        "map_id": "7",
        "map_name": "Descending Stairs 2",
        "exits": {
            "DDR Vertical Shaft B3F": CanUseAbilityBombette(),
            "DDR Stone Puzzle Room": None,
            "DDR Descending Stairs 2 B2F East Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Super Hammer Room",
        "area_id": "11",
        "map_id": "8",
        "map_name": "Super Hammer Room",
        "events": {
            "RF_ISK09_OpenedHammerChest": CanClimbSteps( # unreachable if vanilla gear
                options=[OptionFilter(
                    GearShuffleMode,
                    GearShuffleMode.option_Vanilla
                )],
                filtered_resolution=False,
            )
        },
        "locations": {
            "DDR Super Hammer Room Hidden Chest": CanClimbSteps(),
            "DDR Super Hammer Room In Big Chest": CanClimbSteps(),
        },
        "exits": {
            "DDR Descending Stairs 2 B2F West Door": None,
        }
    },
    {
        "region_name": "DDR Vertical Shaft B3F",
        "area_id": "11",
        "map_id": "9",
        "map_name": "Vertical Shaft",
        "exits": {
            "DDR Descending Stairs 2 B3F": CanUseAbilityBombette(),
            "DDR Vertical Shaft B5F": None,
        }
    },
    {
        "region_name": "DDR Vertical Shaft B5F",
        "area_id": "11",
        "map_id": "9",
        "map_name": "Vertical Shaft",
        "locations": {
            "DDR Vertical Shaft In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "DDR Diamond Stone Room": CanUseAbilityBombette(),
            "DDR Deep Tunnel": None,
            "DDR Vertical Shaft B3F": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Stone Puzzle Room",
        "area_id": "11",
        "map_id": "10",
        "map_name": "Stone Puzzle Room",
        "events": {
            "MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle": HasAll(
                "Pyramid Stone",
                "Diamond Stone",
                "Lunar Stone",
                "RF_DrainedThirdSandRoomAndCanSolvePuzzle"
            ),
        },
        "exits": {
            "DDR Descending Stairs 2 B3F": None,
            "DDR Stone Puzzle Room East Upper Door": CanClimbSteps(),
            "DDR Stone Puzzle Room East Lower Door": None,
            "DDR Stone Puzzle Room Stairwell": Has("MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle"),
        }
    },
    {
        "region_name": "DDR Stone Puzzle Room East Upper Door",
        "area_id": "11",
        "map_id": "10",
        "map_name": "Stone Puzzle Room",
        "exits": {
            "DDR Sand Drainage Room 3 B3F": Has("Ruins Key", count=4),
            "DDR Stone Puzzle Room": None,
        }
    },
    {
        "region_name": "DDR Stone Puzzle Room East Lower Door",
        "area_id": "11",
        "map_id": "10",
        "map_name": "Stone Puzzle Room",
        "exits": {
            "DDR Sand Drainage Room 3 B4F West": None,
            "DDR Stone Puzzle Room": CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Stone Puzzle Room Stairwell",
        "area_id": "11",
        "map_id": "10",
        "map_name": "Stone Puzzle Room",
        "exits": {
            "DDR Ruins Boss Antechamber": None,
            "DDR Stone Puzzle Room": Has("MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle") & CanClimbSteps(),
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 3 B3F",
        "area_id": "11",
        "map_id": "11",
        "map_name": "Sand Drainage Room 3",
        "events": {
            "RF_DrainedThirdSandRoomAndCanSolvePuzzle": CanClimbSteps(),
        },
        "exits": {
            "DDR Stone Puzzle Room East Upper Door": None,
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 3 B4F West",
        "area_id": "11",
        "map_id": "11",
        "map_name": "Sand Drainage Room 3",
        "events": {
            "RF_ISK12_CanEnterFromAbove": None,
        },
        "exits": {
            "DDR Stone Puzzle Room East Lower Door": None,
            "DDR Sand Drainage Room 3 B4F Ledge": (
                Has("RF_DrainedThirdSandRoomAndCanSolvePuzzle")
                | (CanClimbSteps()
                   & (HasSuperHammer() | Has("RF_ISK09_OpenedHammerChest"))
                )
            ),
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 3 B4F East",
        "area_id": "11",
        "map_id": "11",
        "map_name": "Sand Drainage Room 3",
        "events": {
            "RF_ISK12_CanEnterFromAbove": None,
        },
        "exits": {
            "DDR Sand Drainage Room 3 B4F Ledge": None,
            "DDR Lunar Stone Room": None,
        }
    },
    {
        "region_name": "DDR Sand Drainage Room 3 B4F Ledge",
        "area_id": "11",
        "map_id": "11",
        "map_name": "Sand Drainage Room 3",
        "locations": {
            "DDR Sand Drainage Room 3 On Ledge": None,
        },
        "exits": {
            "DDR Sand Drainage Room 3 B4F East": Has("RF_DrainedThirdSandRoomAndCanSolvePuzzle"),
            "DDR Sand Drainage Room 3 B4F West": (
                Has("RF_DrainedThirdSandRoomAndCanSolvePuzzle")
                & CanClimbSteps()
            ),
        }
    },
    {
        "region_name": "DDR Lunar Stone Room",
        "area_id": "11",
        "map_id": "12",
        "map_name": "Lunar Stone Room",
        "locations": {
            "DDR Lunar Stone Room On Pedestal": (
                CanClimbSteps()
                & (HasSuperHammer() | Has("RF_ISK09_OpenedHammerChest"))
            ),
        },
        "exits": {
            "DDR Sand Drainage Room 3 B4F East": None,
        }
    },
    {
        "region_name": "DDR Diamond Stone Room",
        "area_id": "11",
        "map_id": "13",
        "map_name": "Diamond Stone Room",
        "locations": {
            "DDR Diamond Stone Room On Pedestal": (
                CanClimbSteps()
                & (HasSuperHammer() | Has("RF_ISK09_OpenedHammerChest"))
            ),
        },
        "exits": {
            "DDR Vertical Shaft B5F": None,
        }
    },
    {
        "region_name": "DDR Tutankoopa Room",
        "area_id": "11",
        "map_id": "14",
        "map_name": "Tutankoopa Room",
        "events": {
            "STARSPIRIT_2": Has("MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle"),
            "STARSPIRIT": Has("MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle"),
            "RF_Ch2_SavedStarSpirit": Has("MB_Ch2_Spirit_ISK11_SolvedArtifactPuzzle"),
        },
        "exits": {
            "DDR Ruins Boss Antechamber": None,
        }
    },
    {
        "region_name": "DDR Deep Tunnel",
        "area_id": "11",
        "map_id": "15",
        "map_name": "Deep Tunnel",
        "exits": {
            "DDR Vertical Shaft B5F": None,
        }
    },
    {
        "region_name": "DDR Ruins Boss Antechamber",
        "area_id": "11",
        "map_id": "16",
        "map_name": "Boss Antechamber",
        "exits": {
            "DDR Stone Puzzle Room Stairwell": None,
            "DDR Tutankoopa Room": None,
        }
    }
]
