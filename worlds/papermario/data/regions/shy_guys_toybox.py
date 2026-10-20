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
    CanUseAbilityBow,
    CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

shy_guys_toybox_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "SGT BLU Large Playroom",
        "area_id": "16",
        "map_id": "0",
        "map_name": "BLU Large Playroom",
        "locations": {
            "SGT BLU Large Playroom Calculator Thief 1": None,
            "SGT BLU Large Playroom Calculator Thief 2": None,
            "SGT BLU Large Playroom Shy Guy 2": None,
            "SGT BLU Large Playroom Shy Guy 3": None,
            "SGT BLU Large Playroom Shy Guy 4": None,
            "SGT BLU Large Playroom Shy Guy 5": None,
            "SGT BLU Large Playroom Hidden Block 1": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "SGT BLU Large Playroom Hidden Block 2": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT BLU Anti-Guy Hall": None,
        }
    },
    {
        "region_name": "SGT RED Boss Barricade West",
        "area_id": "16",
        "map_id": "1",
        "map_name": "RED Boss Barricade",
        "exits": {
            "SGT RED Station": None,
            "SGT RED Boss Barricade East": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "SGT RED Boss Barricade East",
        "area_id": "16",
        "map_id": "1",
        "map_name": "RED Boss Barricade",
        "locations": {
            "SGT RED Boss Barricade Yellow Block Right": CanHitFloatingBlocks(),
            "SGT RED Boss Barricade Hidden Block Left": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "SGT RED Boss Barricade On Brick Block": (
                HasUltraBoots()
                | (HasBoots()
                   & (HasHammer() | HasSuperBoots())
                   & CanUseAbilityKooper()
                   & CanSeeHiddenBlocks()
                  )
            ),
        },
        "exits": {
            "SGT RED Boss Antechamber": None,
            "SGT RED Boss Barricade West": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "SGT BLU Station",
        "area_id": "16",
        "map_id": "2",
        "map_name": "BLU Station",
        "locations": {
            "SGT BLU Station Hidden Panel": CanFlipPanels(),
            "SGT BLU Station Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT BLU Anti-Guy Hall": None,
            "SGT BLU Block City": None,
            "SGT PNK Station": HasAll("MF_Ch4_CanThrowInTrain", "Toy Train") & HasBoots(),
            "SGT RED Station": (
                HasBoots()
                & HasAll("MF_Ch4_CanThrowInTrain", "Toy Train", "RF_BlueSwitchPulled")
            ),
            "TT Residental District Toybox Room": CanClimbSteps(),
            "SGT BLU Station Switch": (
                HasBoots()
                & HasAll("MF_Ch4_CanThrowInTrain", "Toy Train", "RF_BlueSwitchPulled")
            ),
        }
    },
    {
        "region_name": "SGT BLU Station Switch",
        "area_id": "16",
        "map_id": "2",
        "map_name": "BLU Station",
        "events": {
            "RF_BlueSwitchPulled": None,
        },
        "exits": {
            "SGT BLU Station": None,
        }
    },
    {
        "region_name": "SGT BLU Block City",
        "area_id": "16",
        "map_id": "3",
        "map_name": "BLU Block City",
        "locations": {
            "SGT BLU Block City Infront Of Chest": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City In Chest": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Yellow Block 1": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Yellow Block 2": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Yellow Block On Ledge": (
                CanUseAbilityParakarry()
                & HasBoots()
                & (HasHammer() | HasSuperBoots())
            ),
            "SGT BLU Block City Midair 1": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 2": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 3": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 4": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 5": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 6": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 7": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City Midair 8": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT BLU Block City On Building": (
                CanUseAbilityParakarry()
                & HasBoots()
                & (HasHammer() | HasSuperBoots())
            ),
            "SGT BLU Block City Behind Building Block": HasBoots() & (HasHammer() | HasSuperBoots()),
        },
        "exits": {
            "SGT BLU Station": None,
        }
    },
    {
        "region_name": "SGT PNK Gourmet Guy Crossing South",
        "area_id": "16",
        "map_id": "4",
        "map_name": "PNK Gourmet Guy Crossing",
        "events": {
            "MF_Ch4_GaveCakeToGourmetGuy": Has("AF_CanMakeCake"),
        },
        "locations": {
            "SGT PNK Gourmet Guy Crossing Gourmet Guy Reward": Has("MF_Ch4_GaveCakeToGourmetGuy"),
        },
        "exits": {
            "SGT PNK Tracks Hallway South": None,
            "SGT PNK Gourmet Guy Crossing North": Has("MF_Ch4_GaveCakeToGourmetGuy"),
        }
    },
    {
        "region_name": "SGT PNK Gourmet Guy Crossing North",
        "area_id": "16",
        "map_id": "4",
        "map_name": "PNK Gourmet Guy Crossing",
        "locations": {
            "SGT PNK Gourmet Guy Crossing Yellow Block 1": CanHitFloatingBlocks(),
            "SGT PNK Gourmet Guy Crossing Yellow Block 2": CanHitFloatingBlocks(),
            "SGT PNK Gourmet Guy Crossing Hidden Block Right": (
                CanSeeHiddenBlocks() & CanHitFloatingBlocks()
            ),
            "SGT PNK Gourmet Guy Crossing Hidden Block Left": (
                CanSeeHiddenBlocks() & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "SGT PNK Tracks Hallway North": None,
            "SGT PNK Gourmet Guy Crossing South": None,
        }
    },
    {
        "region_name": "SGT PNK Station",
        "area_id": "16",
        "map_id": "5",
        "map_name": "PNK Station",
        "locations": {
            "SGT PNK Station Hidden Panel": CanFlipPanels(),
            "SGT PNK Station In Chest": None,
        },
        "exits": {
            "SGT PNK Tracks Hallway South": None,
            "SGT BLU Station": HasAll("Toy Train", "MF_Ch4_CanThrowInTrain") & HasBoots(),
            "SGT GRN Station": (
                HasAll("MF_Ch4_CanThrowInTrain", "Toy Train", "MF_Ch4_PulledPinkSwitch")
                & HasBoots()
            ),
            "SGT PNK Playhouse": None,
        }
    },
    {
        "region_name": "SGT PNK Station Switch",
        "area_id": "16",
        "map_id": "5",
        "map_name": "PNK Station",
        "events": {
            "MF_Ch4_PulledPinkSwitch": None,
        },
        "locations": {
            "SGT PNK Station Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT PNK Tracks Hallway North": None,
        }
    },
    {
        "region_name": "SGT PNK Playhouse",
        "area_id": "16",
        "map_id": "6",
        "map_name": "PNK Playhouse",
        "locations": {
            "SGT PNK Playhouse Infront Of Chest (Right)": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT PNK Playhouse In Chest (Far Right)": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT PNK Playhouse In Chest (Top Left)": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT PNK Playhouse In Chest (Right)": HasBoots() & (HasHammer() | HasSuperBoots()),
            "SGT PNK Playhouse Yellow Block": HasBoots() & (HasHammer() | HasSuperBoots()),
        },
        "exits": {
            "SGT PNK Station": None,
        }
    },
    {
        "region_name": "SGT GRN Station",
        "area_id": "16",
        "map_id": "7",
        "map_name": "GRN Station",
        "events": {
            "MF_Ch4_SolvedColorPuzzle": (
                HasAll("RF_CanVisitRussT", "Dictionary", "Mystery Note")
                & HasHammer()
            ),
        },
        "locations": {
            "SGT GRN Station Hidden Panel": CanFlipPanels(),
            "SGT GRN Station Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT GRN Treadmills/Slot Machine": None,
            "SGT PNK Station": HasAll("MF_Ch4_CanThrowInTrain", "Toy Train") & HasBoots(),
            "SGT RED Station": (
                HasAll("MF_Ch4_CanThrowInTrain", "Toy Train", "MF_Ch4_SolvedColorPuzzle")
                & HasBoots()
            ),
        }
    },
    {
        "region_name": "SGT GRN Treadmills/Slot Machine",
        "area_id": "16",
        "map_id": "8",
        "map_name": "GRN Treadmills/Slot Machine",
        "locations": {
            "SGT GRN Treadmills/Slot Machine Infront Of Chest": (
                CanUseAbilityBow()
                & HasBoots()
                & CanUseAbilityParakarry()
            ),
            "SGT GRN Treadmills/Slot Machine In Chest": (
                CanUseAbilityBow()
                & HasBoots()
                & CanUseAbilityParakarry()
            ),
            "SGT GRN Treadmills/Slot Machine Hidden Room Center": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Defeat Shy Guy": CanUseAbilityBow(),
            "SGT GRN Treadmills/Slot Machine On Treadmill 1": None,
            "SGT GRN Treadmills/Slot Machine On Treadmill 2": None,
            "SGT GRN Treadmills/Slot Machine On Treadmill 3": None,
            "SGT GRN Treadmills/Slot Machine On Treadmill 4": None,
            "SGT GRN Treadmills/Slot Machine On Treadmill 5": None,
            "SGT GRN Treadmills/Slot Machine On Treadmill 6": None,
            "SGT GRN Treadmills/Slot Machine Hidden Room 1": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Hidden Room 2": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Hidden Room 3": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Hidden Room 4": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Hidden Room 5": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine Hidden Room 6": CanUseAbilityBow() & HasBoots(),
            "SGT GRN Treadmills/Slot Machine In MultiCoinBlock": (
                CanUseAbilityBow()
                & HasBoots()
                & CanUseAbilityParakarry()
            ),
        },
        "exits": {
            "SGT GRN Station": None,
        }
    },
    {
        "region_name": "SGT RED Station",
        "area_id": "16",
        "map_id": "9",
        "map_name": "RED Station",
        "locations": {
            "SGT RED Station Hidden Panel": CanFlipPanels(),
            "SGT RED Station Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT RED Moving Platforms East Exit": None,
            "SGT RED Boss Barricade West": None,
            "SGT GRN Station": HasAll("MF_Ch4_CanThrowInTrain", "Toy Train") & HasBoots(),
            "SGT BLU Station Switch": HasAll("MF_Ch4_CanThrowInTrain", "Toy Train") & HasBoots(),
        }
    },
    {
        "region_name": "SGT RED Moving Platforms East Exit",
        "area_id": "16",
        "map_id": "10",
        "map_name": "RED Moving Platforms",
        "locations": {
            "SGT RED Moving Platforms Hidden Block Right": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "SGT RED Station": None,
            "SGT RED Moving Platforms": HasBoots(),
        }
    },
    {
        "region_name": "SGT RED Moving Platforms West Exit",
        "area_id": "16",
        "map_id": "10",
        "map_name": "RED Moving Platforms",
        "locations": {
            "SGT RED Moving Platforms Hidden Block Left": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "SGT RED Lantern Ghost": None,
            "SGT RED Moving Platforms": HasBoots(),
        }
    },
    {
        "region_name": "SGT RED Moving Platforms",
        "area_id": "16",
        "map_id": "10",
        "map_name": "RED Moving Platforms",
        "locations": {
            "SGT RED Moving Platforms Yellow Block 1": CanHitFloatingBlocks(),
            "SGT RED Moving Platforms Yellow Block 2": CanHitFloatingBlocks(),
            "SGT RED Moving Platforms Hidden Block Center": CanSeeHiddenBlocks(),
            "SGT RED Moving Platforms In SuperBlock": CanSeeHiddenBlocks(),
            "SGT RED Moving Platforms In MultiCoinBlock": CanSeeHiddenBlocks(),
        },
        "exits": {
            "SGT RED Moving Platforms West Exit": HasBoots(),
            "SGT RED Moving Platforms East Exit": HasBoots(),
        }
    },
    {
        "region_name": "SGT RED Lantern Ghost",
        "area_id": "16",
        "map_id": "11",
        "map_name": "RED Lantern Ghost",
        "locations": {
            "SGT RED Lantern Ghost Watt Partner": (
                HasHammer()
                | CanUseAbilityKooper()
                | CanUseAbilityBombette()
            ),
        },
        "exits": {
            "SGT RED Moving Platforms West Exit": None,
        }
    },
    {
        "region_name": "SGT BLU Anti-Guy Hall",
        "area_id": "16",
        "map_id": "12",
        "map_name": "BLU Anti-Guy Hall",
        "locations": {
            "SGT BLU Anti-Guy Hall In Chest": Has("AF_CanMakeLemonCandy"),
            "SGT BLU Anti-Guy Hall Yellow Block": CanHitFloatingBlocks(),
            "SGT BLU Anti-Guy Hall Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT BLU Large Playroom": None,
            "SGT BLU Station": None,
        }
    },
    {
        "region_name": "SGT RED Boss Antechamber",
        "area_id": "16",
        "map_id": "13",
        "map_name": "RED Boss Antechamber",
        "exits": {
            "SGT RED Boss Barricade East": None,
            "SGT RED General Guy Room": CanUseAbilityWatt(),
        }
    },
    {
        "region_name": "SGT RED General Guy Room",
        "area_id": "16",
        "map_id": "14",
        "map_name": "RED General Guy Room",
        "events": {
            "STARSPIRIT_4": None,
            "STARSPIRIT": None,
        },
        "exits": {
            "SGT RED Boss Antechamber": None,
        }
    },
    {
        "region_name": "SGT PNK Tracks Hallway South",
        "area_id": "16",
        "map_id": "16",
        "map_name": "PNK Tracks Hallway",
        "locations": {
            "SGT PNK Tracks Hallway Yellow Block South": CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT PNK Gourmet Guy Crossing South": None,
            "SGT PNK Station": None,
        }
    },
    {
        "region_name": "SGT PNK Tracks Hallway North",
        "area_id": "16",
        "map_id": "16",
        "map_name": "PNK Tracks Hallway",
        "locations": {
            "SGT PNK Tracks Hallway Yellow Block North 1": CanHitFloatingBlocks(),
            "SGT PNK Tracks Hallway Yellow Block North 2": CanHitFloatingBlocks(),
            "SGT PNK Tracks Hallway In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "SGT PNK Gourmet Guy Crossing North": None,
            "SGT PNK Station Switch": None,
        }
    }
]
