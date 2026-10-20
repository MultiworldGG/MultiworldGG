from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    True_,
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
    HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    HasSuperBoots,
    HasUltraBoots,
    #CanFlipPanels,
    CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanUseAbilityBow,
    CanUseAbilityWatt,
    CanUseAbilitySushie,
    CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
    CanOpenStarWay,
    #HasStarBeamRequirements,
)

from ...options import BowserCastleMode, BowserDoorQuiz

bowsers_castle_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "BC Dark Cave 1 Lower",
        "area_id": "22",
        "map_id": "0",
        "map_name": "Dark Cave 1",
        "exits": {
            "BC Lava Channel 3 East Exit": CanUseAbilityWatt(),
            "BC Dark Cave 1 Upper": CanUseAbilityWatt() & CanUseAbilityParakarry(),
        }
    },
    {
        "region_name": "BC Dark Cave 1 Upper",
        "area_id": "22",
        "map_id": "0",
        "map_name": "Dark Cave 1",
        "locations": {
            "BC Dark Cave 1 Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "BC Dark Cave 2 Lower": CanUseAbilityWatt(),
            "BC Dark Cave 1 Lower": CanUseAbilityWatt(),
        }
    },
    {
        "region_name": "BC Dark Cave 2 Lower",
        "area_id": "22",
        "map_id": "1",
        "map_name": "Dark Cave 2",
        "locations": {
            "BC Dark Cave 2 Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "BC Dark Cave 1 Upper": CanUseAbilityWatt(),
            "BC Dark Cave 2 Upper": CanUseAbilityWatt() & CanUseAbilityParakarry(),
        }
    },
    {
        "region_name": "BC Dark Cave 2 Upper",
        "area_id": "22",
        "map_id": "1",
        "map_name": "Dark Cave 2",
        "exits": {
            "BC Cave Exit": CanUseAbilityWatt(),
            "BC Dark Cave 2 Lower": CanUseAbilityWatt() & CanClimbSteps(),
        }
    },
    {
        "region_name": "BC Cave Exit",
        "area_id": "22",
        "map_id": "2",
        "map_name": "Cave Exit",
        "exits": {
            "BC Dark Cave 2 Upper": None,
            "BC Guard Door 1 North Exit": None,
        }
    },
    {
        "region_name": "BC Castle Key Timing Puzzle",
        "area_id": "22",
        "map_id": "3",
        "map_name": "Castle Key Timing Puzzle",
        "exits": {
            "BC Split Level Hall Upper Door": None,
            "BC Castle Key Timing Puzzle East Door": (
                HasBoots()
                & (CanUseAbilityKooper() | CanUseAbilityBombette())
            ),
        }
    },
    {
        "region_name": "BC Castle Key Timing Puzzle East Door",
        "area_id": "22",
        "map_id": "3",
        "map_name": "Castle Key Timing Puzzle",
        "exits": {
            "BC Castle Key Room": None,
            "BC Castle Key Timing Puzzle": None,
        }
    },
    {
        "region_name": "BC Ultra Shroom Timing Puzzle West Door",
        "area_id": "22",
        "map_id": "4",
        "map_name": "Ultra Shroom Timing Puzzle",
        "exits": {
            "BC Ultra Shroom Room": None,
            "BC Ultra Shroom Timing Puzzle": None,
        }
    },
    {
        "region_name": "BC Ultra Shroom Timing Puzzle",
        "area_id": "22",
        "map_id": "4",
        "map_name": "Ultra Shroom Timing Puzzle",
        "exits": {
            "BC Upper Grand Hall Upper": None,
            "BC Ultra Shroom Timing Puzzle West Door": CanUseAbilityBombette() & HasBoots(),
        }
    },
    {
        "region_name": "BC Outside Lower Jail East",
        "area_id": "22",
        "map_id": "5",
        "map_name": "Outside Lower Jail",
        "exits": {
            "BC Lava Channel 1 West": None,
            "BC Lower Jail": None,
        }
    },
    {
        "region_name": "BC Outside Lower Jail Lava",
        "area_id": "22",
        "map_id": "5",
        "map_name": "Outside Lower Jail",
        "locations": {
            "BC Outside Lower Jail Yellow Block": (
                CanHitFloatingBlocks()
                & (CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"))
            ),
        },
        "exits": {
            "BC Front Door Exterior Lava": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
            "BC Lava Channel 1 Lava": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Outside Lower Jail West",
        "area_id": "22",
        "map_id": "6",
        "map_name": "Outside Lower Jail",
        "locations": {
            "BC Outside Lower Jail Defeat Koopatrol Reward": CanOpenStarWay(),
        },
        "exits": {
            "BC Front Door Exterior": None,
        }
    },
    {
        "region_name": "BC Lava Channel 1 West",
        "area_id": "22",
        "map_id": "7",
        "map_name": "Lava Channel 1",
        "exits": {
            "BC Outside Lower Jail East": None,
            "BC Lava Channel 1 East": HasBoots(),
            "BC Lava Channel 1 Lava": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 1 East",
        "area_id": "22",
        "map_id": "7",
        "map_name": "Lava Channel 1",
        "exits": {
            "BC Lava Channel 2 West": None,
            "BC Lava Channel 1 West": CanClimbSteps() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 1 Lava",
        "area_id": "22",
        "map_id": "7",
        "map_name": "Lava Channel 1",
        "exits": {
            "BC Outside Lower Jail Lava": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
            "BC Lava Channel 1 West": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 2 West",
        "area_id": "22",
        "map_id": "8",
        "map_name": "Lava Channel 2",
        "exits": {
            "BC Lava Channel 1 East": None,
            "BC Lava Channel 2 East": (
                CanClimbSteps()
                & (CanUseAbilityParakarry() | Has("GF_KPA16_ShutOffLava"))
                & (CanUseAbilityLakilester() | HasBoots() | Has("GF_KPA16_ShutOffLava"))
            ),
            "BC Lava Channel 2 Central Exit": (
                CanClimbSteps()
                & (CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"))
            ),
        }
    },
    {
        "region_name": "BC Lava Channel 2 East",
        "area_id": "22",
        "map_id": "8",
        "map_name": "Lava Channel 2",
        "exits": {
            "BC Lava Channel 3 West": None,
            "BC Lava Channel 2 West": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 2 Central Exit",
        "area_id": "22",
        "map_id": "8",
        "map_name": "Lava Channel 2",
        "exits": {
            "BC Lava Key Room": None,
            "BC Lava Channel 2 West": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 3 West",
        "area_id": "22",
        "map_id": "9",
        "map_name": "Lava Channel 3",
        "locations": {
            "BC Lava Channel 3 On Island 1": (
                (
                    CanUseAbilityLakilester()
                    & CanClimbSteps()
                    & (CanUseAbilityParakarry() | CanUseAbilityKooper())
                )
                | (CanClimbSteps() & Has("GF_KPA16_ShutOffLava"))
            ),
            "BC Lava Channel 3 On Island 2": HasBoots() & Has("GF_KPA16_ShutOffLava"),
        },
        "exits": {
            "BC Lava Channel 2 East": None,
            "BC Lava Channel 3 East Exit": CanClimbSteps() & Has("GF_KPA16_ShutOffLava"),
            "BC Lava Channel 3 Central Exit": (
                CanClimbSteps()
                & (
                    Has("GF_KPA16_ShutOffLava")
                    | (
                        CanUseAbilityLakilester()
                        & CanUseAbilityBow()
                        & CanUseAbilityParakarry()
                    )
                )
            ),
        }
    },
    {
        "region_name": "BC Lava Channel 3 East Exit",
        "area_id": "22",
        "map_id": "9",
        "map_name": "Lava Channel 3",
        "exits": {
            "BC Dark Cave 1 Lower": Has("Bowser Castle Key",count=2),
            "BC Lava Channel 3 West": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Channel 3 Central Exit",
        "area_id": "22",
        "map_id": "9",
        "map_name": "Lava Channel 3",
        "exits": {
            "BC Lava Control Room": None,
            "BC Lava Channel 3 West": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Key Room",
        "area_id": "22",
        "map_id": "10",
        "map_name": "Lava Key Room",
        "locations": {
            "BC Lava Key Room In Chest": CanClimbSteps() & Has("GF_KPA16_ShutOffLava"),
        },
        "exits": {
            "BC Lava Channel 2 Central Exit": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lava Control Room",
        "area_id": "22",
        "map_id": "11",
        "map_name": "Lava Control Room",
        "events": {
            "GF_KPA16_ShutOffLava": CanClimbSteps() & CanUseAbilityLakilester(),
        },
        "exits": {
            "BC Lava Channel 3 Central Exit": CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"),
        }
    },
    {
        "region_name": "BC Lower Jail",
        "area_id": "22",
        "map_id": "12",
        "map_name": "Lower Jail",
        "locations": {
            "BC Lower Jail In Crate 1": HasSuperBoots(),
            "BC Lower Jail In Crate 2": HasSuperBoots(),
        },
        "exits": {
            "BC Outside Lower Jail East": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "BC Lower Grand Hall Lower",
        "area_id": "22",
        "map_id": "13",
        "map_name": "Lower Grand Hall",
        "exits": {
            "BC Guard Door 1": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Guard Door 2": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Stairs to East Upper Jail": None,
            "BC Lower Grand Hall Upper": HasBoots(),
        }
    },
    {
        "region_name": "BC Lower Grand Hall Upper",
        "area_id": "22",
        "map_id": "13",
        "map_name": "Lower Grand Hall",
        "exits": {
            "BC Hall to Water Puzzle": None,
            "BC Castle Item Shop": None,
            "BC Lower Grand Hall Lower": None,
        }
    },
    {
        "region_name": "BC Upper Grand Hall Lower",
        "area_id": "22",
        "map_id": "14",
        "map_name": "Upper Grand Hall",
        "exits": {
            "BC Stairs to West Upper Jail": None,
            "BC Castle Battlement Upper Door": None,
            "BC Upper Grand Hall Upper": HasBoots(),
        }
    },
    {
        "region_name": "BC Upper Grand Hall Upper",
        "area_id": "22",
        "map_id": "14",
        "map_name": "Upper Grand Hall",
        "exits": {
            "BC Split Level Hall": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Blue Fire Bridge": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Ultra Shroom Timing Puzzle": None,
            "BC Upper Grand Hall Lower": None,
        }
    },
    {
        "region_name": "BC Maze Guide Room Lower",
        "area_id": "22",
        "map_id": "15",
        "map_name": "Maze Guide Room",
        "exits": {
            "BC Split Level Hall": None,
            "BC Maze Guide Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "BC Maze Guide Room Upper",
        "area_id": "22",
        "map_id": "15",
        "map_name": "Maze Guide Room",
        "exits": {
            "BC Maze Room Upper": None,
            "BC Maze Guide Room Lower": None,
        }
    },
    {
        "region_name": "BC Maze Room Lower",
        "area_id": "22",
        "map_id": "16",
        "map_name": "Maze Room",
        "exits": {
            "BC Maze Room Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "BC Maze Room Upper",
        "area_id": "22",
        "map_id": "16",
        "map_name": "Maze Room",
        "exits": {
            "BC Maze Guide Room Upper": None,
            "BC Blue Fire Bridge": None,
            "BC Maze Room Lower": None,
        }
    },
    {
        "region_name": "BC Hall to Guard Door 1",
        "area_id": "22",
        "map_id": "17",
        "map_name": "Hall to Guard Door 1",
        "exits": {
            "BC Entry Lava Hall": None,
            "BC Guard Door 1": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Guard Door 2": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
        }
    },
    {
        "region_name": "BC Hall to Water Puzzle",
        "area_id": "22",
        "map_id": "18",
        "map_name": "Hall to Water Puzzle",
        "exits": {
            "BC Lower Grand Hall Upper": None,
            "BC Left Water Puzzle 1F": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Bill Blaster Hall Lower": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
        }
    },
    {
        "region_name": "BC Split Level Hall",
        "area_id": "22",
        "map_id": "19",
        "map_name": "Split Level Hall",
        "exits": {
            "BC Upper Grand Hall Upper": None,
            "BC Maze Guide Room Lower": Has("Bowser Castle Key",count=5),
            "BC Split Level Hall Upper Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "BC Split Level Hall Upper Door",
        "area_id": "22",
        "map_id": "19",
        "map_name": "Split Level Hall",
        "exits": {
            "BC Castle Key Timing Puzzle": None,
            "BC Split Level Hall": None,
        }
    },
    {
        "region_name": "BC Fake Peach Hallway",
        "area_id": "22",
        "map_id": "20",
        "map_name": "Fake Peach Hallway",
        "exits": {
            "BC Blue Fire Bridge": True_() & OptionFilter(
                BowserCastleMode,
                BowserCastleMode.option_Boss_Rush,
                operator="ne",
            ),
            "SSS Riding Star Ship Scene": True_() & OptionFilter(
                BowserCastleMode,
                BowserCastleMode.option_Boss_Rush
            ),
            "BC Guard Door 3": (
                HasBoots()
                | HasHammer()
                | CanUseAbilityKooper()
                | CanUseAbilityBombette()
            ),
        }
    },
    {
        "region_name": "BC Ship Enter/Exit Scenes",
        "area_id": "22",
        "map_id": "21",
        "map_name": "Ship Enter/Exit Scenes",
        "exits": {
            "SSS Riding Star Ship Scene": None,
            "BC Hangar": True_() & OptionFilter(
                BowserCastleMode,
                BowserCastleMode.option_Boss_Rush,
                operator="ne",
            ),
            "BC Fake Peach Hallway": True_() & OptionFilter(
                BowserCastleMode,
                BowserCastleMode.option_Boss_Rush,
            ),
        }
    },
    {
        "region_name": "BC Castle Battlement Lower Door",
        "area_id": "22",
        "map_id": "22",
        "map_name": "Battlement",
        "locations": {
            "BC Battlement Yellow Block Left": CanHitFloatingBlocks(),
            "BC Battlement Yellow Block Center": CanHitFloatingBlocks(),
            "BC Battlement Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "BC Guard Door 2": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Hidden Passage 1": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Castle Battlement Upper Door": CanClimbSteps(),
        }
    },
    {
        "region_name": "BC Castle Battlement Upper Door",
        "area_id": "22",
        "map_id": "22",
        "map_name": "Battlement",
        "locations": {
            "BC Battlement On Ledge": None,
        },
        "exits": {
            "BC Upper Grand Hall Lower": None,
            "BC Castle Battlement Lower Door": None,
        }
    },
    {
        "region_name": "BC Front Door Exterior",
        "area_id": "22",
        "map_id": "23",
        "map_name": "Front Door Exterior",
        "exits": {
            # no key needed for shortened
            "BC Entry Lava Hall": (
                Has("Bowser Castle Key",count=1)
                | OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened)
            ),
            "BC Outside Lower Jail West": None,
            "BC Hangar": None,
        }
    },
    {
        "region_name": "BC Front Door Exterior Lava",
        "area_id": "22",
        "map_id": "23",
        "map_name": "Front Door Exterior",
        "locations": {
            "BC Front Door Exterior Red Block": (
                CanClimbSteps()
                & CanHitFloatingBlocks()
                & (CanUseAbilityLakilester() | Has("GF_KPA16_ShutOffLava"))
            ),
        },
        "exits": {
            "BC Outside Lower Jail Lava": None,
        }
    },
    {
        "region_name": "BC Hangar",
        "area_id": "22",
        "map_id": "24",
        "map_name": "Hangar",
        "exits": {
            "BC Front Door Exterior": None,
            "BC Ship Enter/Exit Scenes": None,
        }
    },
    {
        "region_name": "BC Entry Lava Hall",
        "area_id": "22",
        "map_id": "25",
        "map_name": "Entry Lava Hall",
        "exits": {
            "BC Front Door Exterior": None,
            "BC Hall to Guard Door 1": None,
        }
    },
    {
        "region_name": "BC Guard Door 1",
        "area_id": "22",
        "map_id": "26",
        "map_name": "Guard Door 1",
        "exits": {
            "BC Hall to Guard Door 1": None,
            "BC Lower Jail": ( # Saveguard for beeing able to leave w/o Homeward Shroom
                CanUseAbilityBombette()
                & CanUseAbilityLakilester()
                & CanUseAbilityParakarry()
                & CanUseAbilityBow()
            ),
            "BC Lower Grand Hall Lower": Has("RF_Ch8_FirstGuardDoor"),
            "BC Guard Door 1 North Exit": Has("RF_Ch8_FirstGuardDoor"),
        }
    },
    {
        "region_name": "BC Guard Door 1 North Exit",
        "area_id": "22",
        "map_id": "26",
        "map_name": "Guard Door 1",
        "events": {
            "RF_Ch8_FirstGuardDoor": None,
        },
        "exits": {
            "BC Cave Exit": None,
            "BC Guard Door 1": None,
        }
    },
    {
        "region_name": "BC Guard Door 2",
        "area_id": "22",
        "map_id": "27",
        "map_name": "Guard Door 2",
        "exits": {
            "BC Room with Hidden Door 2": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Castle Battlement Lower Door": (
                OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla)
                & CanOpenStarWay(
                    # Expect being able to open Star Way if Anti Guys Unit's forced
                    options=[OptionFilter(
                        BowserDoorQuiz,
                        BowserDoorQuiz.option_Anti_Guys_Unit,
                    )],
                    filtered_resolution=True,
                )
            ),
            "BC Hall to Guard Door 1": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Lower Grand Hall Lower": (
                OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened)
                & CanOpenStarWay(
                    # Expect being able to open Star Way if Anti Guys Unit's forced
                    options=[OptionFilter(
                        BowserDoorQuiz,
                        BowserDoorQuiz.option_Anti_Guys_Unit,
                    )],
                    filtered_resolution=True,
                )
            ),
        }
    },
    {
        "region_name": "BC Guard Door 3",
        "area_id": "22",
        "map_id": "28",
        "map_name": "Guard Door 3",
        "exits": {
            "BC Fake Peach Hallway": None,
            "BC Exit to Peach's Castle": CanOpenStarWay(),
        }
    },
    {
        "region_name": "BC Stairs to East Upper Jail",
        "area_id": "22",
        "map_id": "29",
        "map_name": "Stairs to East Upper Jail",
        "exits": {
            "BC Lower Grand Hall Lower": None,
            "BC East Upper Jail": None,
        }
    },
    {
        "region_name": "BC East Upper Jail",
        "area_id": "22",
        "map_id": "30",
        "map_name": "East Upper Jail",
        "locations": {
            "BC East Upper Jail Defeat Koopatrol Reward": CanOpenStarWay(),
        },
        "exits": {
            "BC Stairs to East Upper Jail": None,
        }
    },
    {
        "region_name": "BC Stairs to West Upper Jail",
        "area_id": "22",
        "map_id": "31",
        "map_name": "Stairs to West Upper Jail",
        "exits": {
            "BC West Upper Jail": None,
            "BC Upper Grand Hall Lower": None,
        }
    },
    {
        "region_name": "BC West Upper Jail",
        "area_id": "22",
        "map_id": "32",
        "map_name": "West Upper Jail",
        "locations": {
            "BC West Upper Jail Defeat Koopatrol Reward": CanOpenStarWay(),
        },
        "exits": {
            "BC Stairs to West Upper Jail": None,
        }
    },
    {
        "region_name": "BC Castle Item Shop",
        "area_id": "22",
        "map_id": "33",
        "map_name": "Item Shop",
        "locations": {
            "BC Item Shop Shop Item 1": None,
            "BC Item Shop Shop Item 2": None,
            "BC Item Shop Shop Item 3": None,
            "BC Item Shop Shop Item 4": None,
            "BC Item Shop Shop Item 5": None,
            "BC Item Shop Shop Item 6": None,
        },
        "exits": {
            "BC Lower Grand Hall Upper": None,
        }
    },
    {
        "region_name": "BC Castle Key Room",
        "area_id": "22",
        "map_id": "34",
        "map_name": "Castle Key Room",
        "locations": {
            "BC Castle Key Room On The Ground": None,
        },
        "exits": {
            "BC Castle Key Timing Puzzle": None,
        }
    },
    {
        "region_name": "BC Ultra Shroom Room",
        "area_id": "22",
        "map_id": "35",
        "map_name": "Ultra Shroom Room",
        "locations": {
            "BC Ultra Shroom Room On The Ground": CanClimbSteps(),
        },
        "exits": {
            "BC Ultra Shroom Timing Puzzle": None,
        }
    },
    {
        "region_name": "BC Blue Fire Bridge",
        "area_id": "22",
        "map_id": "36",
        "map_name": "Blue Fire Bridge",
        "exits": {
            "BC Maze Room Upper": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Upper Grand Hall Upper": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Fake Peach Hallway": None,
        }
    },
    {
        "region_name": "BC Room with Hidden Door 1",
        "area_id": "22",
        "map_id": "37",
        "map_name": "Room with Hidden Door 1",
        "locations": {
            "BC Room with Hidden Door 1 Yellow Block": CanHitFloatingBlocks(),
            "BC Room with Hidden Door 1 Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
        },
        "exits": {
            "BC Bill Blaster Hall Upper": None,
            "BC Hidden Passage 1": None,
        }
    },
    {
        "region_name": "BC Hidden Passage 1",
        "area_id": "22",
        "map_id": "38",
        "map_name": "Hidden Passage 1",
        "exits": {
            "BC Room with Hidden Door 1": None,
            "BC Room with Hidden Door 2": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Castle Battlement Lower Door": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
        }
    },
    {
        "region_name": "BC Room with Hidden Door 2",
        "area_id": "22",
        "map_id": "39",
        "map_name": "Room with Hidden Door 2",
        "exits": {
            "BC Hidden Passage 1": None,
            "BC Guard Door 2": Has("Bowser Castle Key",count=4),
            "BC Hidden Passage 2": None,
        }
    },
    {
        "region_name": "BC Hidden Passage 2",
        "area_id": "22",
        "map_id": "40",
        "map_name": "Hidden Passage 2",
        "exits": {
            "BC Room with Hidden Door 2": None,
            "BC Room with Hidden Door 3": None,
        }
    },
    {
        "region_name": "BC Room with Hidden Door 3",
        "area_id": "22",
        "map_id": "41",
        "map_name": "Room with Hidden Door 3",
        "exits": {
            "BC Hidden Passage 2": None,
            "BC Dead End Passage": None,
            "BC Hidden Passage 3": None,
        }
    },
    {
        "region_name": "BC Dead End Passage",
        "area_id": "22",
        "map_id": "42",
        "map_name": "Dead End Passage",
        "exits": {
            "BC Room with Hidden Door 3": None,
            "BC Dead End Room": None,
        }
    },
    {
        "region_name": "BC Dead End Room",
        "area_id": "22",
        "map_id": "43",
        "map_name": "Dead End Room",
        "exits": {
            "BC Dead End Passage": None,
        }
    },
    {
        "region_name": "BC Hidden Passage 3",
        "area_id": "22",
        "map_id": "44",
        "map_name": "Hidden Passage 3",
        "exits": {
            "BC Room with Hidden Door 3": None,
            "BC Hidden Key Room": None,
        }
    },
    {
        "region_name": "BC Hidden Key Room",
        "area_id": "22",
        "map_id": "45",
        "map_name": "Hidden Key Room",
        "locations": {
            "BC Hidden Key Room On The Ground": CanClimbSteps(),
        },
        "exits": {
            "BC Hidden Passage 3": None,
        }
    },
    {
        "region_name": "BC Exit to Peach's Castle",
        "area_id": "22",
        "map_id": "46",
        "map_name": "Exit to Peach's Castle",
        "exits": {
            "BC Guard Door 3": None,
            "PCG Hijacked Castle Entrance": None,
        }
    },
    {
        "region_name": "BC Bill Blaster Hall Lower",
        "area_id": "22",
        "map_id": "47",
        "map_name": "Bill Blaster Hall",
        "exits": {
            "BC Right Water Puzzle 1F": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Vanilla),
            "BC Hall to Water Puzzle": True_() & OptionFilter(BowserCastleMode, BowserCastleMode.option_Shortened),
            "BC Bill Blaster Hall Upper": HasBoots(),
        }
    },
    {
        "region_name": "BC Bill Blaster Hall Upper",
        "area_id": "22",
        "map_id": "47",
        "map_name": "Bill Blaster Hall",
        "exits": {
            "BC Room with Hidden Door 1": None,
            "BC Bill Blaster Hall Lower": None,
        }
    },
    {
        "region_name": "BC Left Water Puzzle 1F",
        "area_id": "22",
        "map_id": "48",
        "map_name": "Left Water Puzzle",
        "exits": {
            "BC Hall to Water Puzzle": None,
            "BC Right Water Puzzle 1F": None,
        }
    },
    {
        "region_name": "BC Right Water Puzzle 1F",
        "area_id": "22",
        "map_id": "49",
        "map_name": "Right Water Puzzle",
        "exits": {
            "BC Left Water Puzzle 1F": None,
            "BC Bill Blaster Hall Lower": Has("Bowser Castle Key",count=3),
            "BC Right Water Puzzle 2F": (
                CanUseAbilitySushie()
                & CanClimbSteps()
                & CanHitFloatingBlocks()
            ),
        }
    },
    {
        "region_name": "BC Right Water Puzzle 2F",
        "area_id": "22",
        "map_id": "49",
        "map_name": "Right Water Puzzle",
        "exits": {
            "BC Left Water Puzzle 2F": CanUseAbilitySushie(),
            "BC Right Water Puzzle 1F": CanUseAbilitySushie() & CanHitFloatingBlocks(),
        }
    },
    {
        "region_name": "BC Left Water Puzzle 2F",
        "area_id": "22",
        "map_id": "48",
        "map_name": "Left Water Puzzle",
        "exits": {
            "BC Left Water Puzzle 3F": (
                CanUseAbilitySushie()
                & CanUseAbilityBombette()
                & CanClimbSteps()
            ),
            "BC Right Water Puzzle 2F": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "BC Left Water Puzzle 3F",
        "area_id": "22",
        "map_id": "48",
        "map_name": "Left Water Puzzle",
        "locations": {
            "BC Left Water Puzzle Top Left Ledge": CanUseAbilitySushie() & Has("RF_WaterLevel2"),
        },
        "exits": {
            "BC Right Water Puzzle 3F": None,
        }
    },
    {
        "region_name": "BC Right Water Puzzle 3F",
        "area_id": "22",
        "map_id": "48",
        "map_name": "Right Water Puzzle",
        "events": {
            "RF_WaterLevel2": HasUltraBoots(),
        },
        "locations": {
            "BC Right Water Puzzle Hidden Block": CanSeeHiddenBlocks() & HasUltraBoots(),
        },
        "exits": {
            "BC Right Water Puzzle 3F": CanUseAbilityBombette(),
            "BC Right Water Puzzle 2F": CanHitFloatingBlocks(),
        }
    },
    {
        "region_name": "PCG Hijacked Castle Entrance",
        "area_id": "23",
        "map_id": "2",
        "map_name": "Hijacked Castle Entrance",
        "locations": {
            "PCG Hijacked Castle Entrance Hidden Block": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "BC Exit to Peach's Castle": None,
            "PC Entry Hall (1F)": None,
        }
    }
]
