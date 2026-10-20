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
    HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    #CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

from ...options import GearShuffleMode

mt_lavalava_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "MLL Volcano Entrance",
        "area_id": "18",
        "map_id": "0",
        "map_name": "Volcano Entrance",
        "exits": {
            "JJ Path to the Volcano Entrance": None,
            "MLL First Lava Lake West": None
        }
    },
    {
        "region_name": "MLL First Lava Lake West",
        "area_id": "18",
        "map_id": "1",
        "map_name": "First Lava Lake",
        "exits": {
            "MLL Volcano Entrance": None,
            "MLL First Lava Lake East": CanUseAbilityLakilester() | CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL First Lava Lake East",
        "area_id": "18",
        "map_id": "1",
        "map_name": "First Lava Lake",
        "exits": {
            "MLL Central Cavern 1F": None,
            "MLL First Lava Lake West": CanUseAbilityLakilester() | CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Central Cavern 1F",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "exits": {
            "MLL First Lava Lake East": None,
            "MLL Central Cavern B1F": None,
            "MLL Central Cavern B1F East Exit": None,
        }
    },
    {
        "region_name": "MLL Central Cavern B1F",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "locations": {
            "MLL Central Cavern Yellow Block 1": CanHitFloatingBlocks(),
            "MLL Central Cavern Yellow Block 2": CanHitFloatingBlocks(),
            "MLL Central Cavern Yellow Block 3": CanHitFloatingBlocks(),
            "MLL Central Cavern Yellow Block 4": CanHitFloatingBlocks(),
        },
        "exits": {
            "MLL Central Cavern B2F": CanClimbSteps(),
            "MLL Central Cavern B1F Brick Block": HasUltraBoots(),
            "MLL Central Cavern 1F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Central Cavern B1F Brick Block",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "locations": {
            "MLL Central Cavern On Brick Block": None,
        },
        "exits": {
            "MLL Central Cavern B1F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Central Cavern B1F East Exit",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "exits": {
            "MLL Fire Bar Bridge": CanClimbSteps(),
            "MLL Central Cavern B1F Brick Block": CanUseAbilityKooper(),
            "MLL Central Cavern B1F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Central Cavern B2F",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "locations": {
            "MLL Central Cavern On Stone Pillar": None,
        },
        "exits": {
            "MLL Zipline Cavern B2F": HasUltraHammer() | Has("RF_KZN07_OpenedHammerChest"),
            "MLL Central Cavern B1F": CanClimbSteps(),
            "MLL Central Cavern B4F West Exit": CanClimbSteps(),
            "MLL Central Cavern B4F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Central Cavern B4F West Exit",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "exits": {
            "MLL Descent Toward Ultra Hammer": None,
            "MLL Zipline Cavern B4F": None,
        }
    },
    {
        "region_name": "MLL Central Cavern B4F",
        "area_id": "18",
        "map_id": "2",
        "map_name": "Central Cavern",
        "exits": {
            "MLL Zipline Cavern B4F": None,
            "MLL Central Cavern B2F": CanClimbSteps(),
            "MLL Central Cavern B4F West Exit": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Fire Bar Bridge",
        "area_id": "18",
        "map_id": "3",
        "map_name": "Fire Bar Bridge",
        "locations": {
            "MLL Fire Bar Bridge In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "MLL Central Cavern B1F East Exit": None,
        }
    },
    {
        "region_name": "MLL Descent Toward Ultra Hammer",
        "area_id": "18",
        "map_id": "4",
        "map_name": "Descent Toward Ultra Hammer",
        "exits": {
            "MLL Flowing Lava Puzzle East": None,
            "MLL Central Cavern B4F West Exit": None,
        }
    },
    {
        "region_name": "MLL Flowing Lava Puzzle East",
        "area_id": "18",
        "map_id": "5",
        "map_name": "Flowing Lava Puzzle",
        "events": {
            "RF_KZN06_SolvedBlockPuzzle": CanUseAbilityParakarry() | CanUseAbilityLakilester(),
        },
        "locations": {
            "MLL Flowing Lava Puzzle Hidden Block": (
                CanClimbSteps()
                & CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "MLL Descent Toward Ultra Hammer": None,
            "MLL Flowing Lava Puzzle West": CanUseAbilityParakarry() | CanUseAbilityLakilester(),
            "MLL Flowing Lava Puzzle East Lower Exit": (
                CanClimbSteps()
                & (HasUltraHammer() | Has("RF_KZN07_OpenedHammerChest"))
            ),
        }
    },
    {
        "region_name": "MLL Flowing Lava Puzzle West",
        "area_id": "18",
        "map_id": "5",
        "map_name": "Flowing Lava Puzzle",
        "exits": {
            "MLL Ultra Hammer Room": None,
            "MLL Flowing Lava Puzzle East": (
                (Has("RF_KZN06_SolvedBlockPuzzle") & CanUseAbilityParakarry())
                | CanUseAbilityLakilester()
            ),
        }
    },
    {
        "region_name": "MLL Flowing Lava Puzzle East Lower Exit",
        "area_id": "18",
        "map_id": "5",
        "map_name": "Flowing Lava Puzzle",
        "exits": {
            "MLL Dizzy Stomp Room": None,
            "MLL Flowing Lava Puzzle East": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Ultra Hammer Room",
        "area_id": "18",
        "map_id": "6",
        "map_name": "Ultra Hammer Room",
        "events": {
            "RF_KZN07_OpenedHammerChest": (
                CanClimbSteps(
                    options=[OptionFilter(
                        GearShuffleMode,
                        GearShuffleMode.option_Vanilla
                    )],
                    filtered_resolution=False,
                )
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester())
            ),
            "RF_KZN06_SolvedBlockPuzzle": (
                CanClimbSteps()
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester())
            ),
        },
        "locations": {
            "MLL Ultra Hammer Room In Big Chest": (
                CanClimbSteps()
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester() | HasUltraHammer())
            ),
        },
        "exits": {
            "MLL Flowing Lava Puzzle West": None,
        }
    },
    {
        "region_name": "MLL Dizzy Stomp Room",
        "area_id": "18",
        "map_id": "7",
        "map_name": "Dizzy Stomp Room",
        "locations": {
            "MLL Dizzy Stomp Room In Chest": (
                CanClimbSteps()
                & (CanUseAbilityParakarry() | CanUseAbilityLakilester())
            ),
        },
        "exits": {
            "MLL Flowing Lava Puzzle East Lower Exit": None
        }
    },
    {
        "region_name": "MLL Zipline Cavern B2F",
        "area_id": "18",
        "map_id": "8",
        "map_name": "Zipline Cavern",
        "locations": {
            "MLL Zipline Cavern In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "MLL Central Cavern B2F": None,
            "MLL Zipline Cavern B3F": None,
            "MLL Zipline Cavern B4F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Zipline Cavern B3F",
        "area_id": "18",
        "map_id": "8",
        "map_name": "Zipline Cavern",
        "exits": {
            "MLL Descent Toward Boss": None,
            "MLL Zipline Cavern B4F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Zipline Cavern B4F",
        "area_id": "18",
        "map_id": "8",
        "map_name": "Zipline Cavern",
        "locations": {
            "MLL Zipline Cavern Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "MLL Central Cavern B4F": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Descent Toward Boss",
        "area_id": "18",
        "map_id": "9",
        "map_name": "Descent Toward Boss",
        "exits": {
            "MLL Zipline Cavern B3F": None,
            "MLL Second Lava Lake West": None,
        }
    },
    {
        "region_name": "MLL Second Lava Lake West",
        "area_id": "18",
        "map_id": "10",
        "map_name": "Second Lava Lake",
        "exits": {
            "MLL Descent Toward Boss": None,
            "MLL Second Lava Lake East": CanClimbSteps() | CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "MLL Second Lava Lake East",
        "area_id": "18",
        "map_id": "10",
        "map_name": "Second Lava Lake",
        "exits": {
            "MLL Spike Roller Trap": None,
            "MLL Second Lava Lake West": CanClimbSteps() | CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "MLL Spike Roller Trap",
        "area_id": "18",
        "map_id": "11",
        "map_name": "Spike Roller Trap",
        "exits": {
            "MLL Second Lava Lake East": None,
            "MLL Boss Antechamber Upper": (
                CanClimbSteps()
                & (HasUltraHammer() | Has("RF_KZN07_OpenedHammerChest"))
            ),
        }
    },
    {
        "region_name": "MLL Boss Antechamber Upper",
        "area_id": "18",
        "map_id": "12",
        "map_name": "Boss Antechamber",
        "locations": {
            "MLL Boss Antechamber Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "MLL Spike Roller Trap": None,
            "MLL Boss Room Upper": None,
            "MLL Boss Antechamber Lower": None,
        }
    },
    {
        "region_name": "MLL Boss Antechamber Lower",
        "area_id": "18",
        "map_id": "12",
        "map_name": "Boss Antechamber",
        "exits": {
            "MLL Boss Room Lower": None,
            "MLL Boss Antechamber Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "MLL Boss Room Upper",
        "area_id": "18",
        "map_id": "13",
        "map_name": "Boss Room",
        "locations": {
            "MLL Boss Room Yellow Block Left": CanHitFloatingBlocks(),
            "MLL Boss Room Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "MLL Boss Antechamber Upper": None,
        }
    },
    {
        "region_name": "MLL Boss Room Lower",
        "area_id": "18",
        "map_id": "13",
        "map_name": "Boss Room",
        "exits": {
            "MLL Boss Antechamber Lower": None,
            "MLL Rising Lava 1 Lower": None,
        }
    },
    {
        "region_name": "MLL Rising Lava 1 Lower",
        "area_id": "18",
        "map_id": "14",
        "map_name": "Rising Lava 1",
        "exits": {
            "MLL Boss Room Lower": None,
            "MLL Rising Lava 1 Upper": HasBoots(),
        }
    },
    {
        "region_name": "MLL Rising Lava 1 Upper",
        "area_id": "18",
        "map_id": "14",
        "map_name": "Rising Lava 1",
        "exits": {
            "MLL Rising Lava 2": None,
            "MLL Rising Lava 1 Lower": None,
        }
    },
    {
        "region_name": "MLL Rising Lava 2",
        "area_id": "18",
        "map_id": "15",
        "map_name": "Rising Lava 2",
        "events": {
            "MF_Ch5_FoundEscapeRoute": CanClimbSteps(),
        },
        "exits": {
            "MLL Rising Lava 1 Upper": None,
        }
    }
]
