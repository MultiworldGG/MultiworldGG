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
    HasHammer,
    HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    #CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

from ...options import OpenPrologue

goomba_village_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "GR Forest Clearing",
        "area_id": "0",
        "map_id": "0",
        "map_name": "Forest Clearing",
        "locations": {
            "GR Forest Clearing Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "GR Goomba Village": None,
        }
    },
    {
        "region_name": "GR Goomba Village Exit East",
        "area_id": "0",
        "map_id": "1",
        "map_name": "Goomba Village",
        "exits": {
            "GR Goomba Road 1": None,
            "GR Goomba Village": HasHammer() | CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "GR Goomba Village",
        "area_id": "0",
        "map_id": "1",
        "map_name": "Goomba Village",
        "events": {
            "StarPiece_KMR_1": None,
            "StarPiece_KMR_8": None,
        },
        "locations": {
            "GR Goomba Village On The Balcony": Has("RF_FixedVeranda"),
            "GR Goomba Village Goompa Koopa Koot Favor": Has("FAVOR_2_01_active"),
            "GR Goomba Village Goompa Gift": None,
            "GR Goomba Village Goombaria Dolly Reward": Has("Dolly"),
            "GR Goomba Village Goompa Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Goompa")
            ),
            "GR Goomba Village Goompapa Letter Reward 1": (
                CanUseAbilityParakarry()
                & Has("Letter to Goompapa 1")
            ),
            "GR Goomba Village Goompapa Letter Reward 2": (
                CanUseAbilityParakarry()
                & Has("Letter to Goompapa 2")
            ),
            "GR Goomba Village Goomnut Tree": CanShakeTrees(),
            "GR Goomba Village Goombario Partner": None,
            "GR Goomba Village Bush Bottom Right": None,
        },
        "exits": {
            "GR Forest Clearing": None,
            "GR Behind the Village East": None,
            "GR Bottom of the Cliff West": Has("RF_BrokenVeranda"),
            "GR Goomba Village Exit East": HasHammer() | CanUseAbilityBombette(),
            "GR Goomba Village Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
        }
    },
    {
        "region_name": "GR Goomba Village Pipe",
        "area_id": "0",
        "map_id": "1",
        "map_name": "Goomba Village",
        "exits": {
            "TTT Warp Zone 1 (B1) Goomba Village Pipe": CanReenterVerticalPipes(),
            "GR Goomba Village": None,
        }
    },
    {
        "region_name": "GR Behind the Village West",
        "area_id": "0",
        "map_id": "4",
        "map_name": "Behind the Village",
        "exits": {
            "GR Bottom of the Cliff East": None,
            "GR Behind the Village East": CanClimbSteps(),
        }
    },
    {
        "region_name": "GR Behind the Village East",
        "area_id": "0",
        "map_id": "4",
        "map_name": "Behind the Village",
        "locations": {
            "GR Behind the Village On Ledge": HasBoots(),
            "GR Behind the Village In Tree": CanShakeTrees() & HasBoots(),
        },
        "exits": {
            "GR Goomba Village": None,
            "GR Behind the Village West": None,
        }
    },
    {
        "region_name": "GR Bottom of the Cliff West",
        "area_id": "0",
        "map_id": "2",
        "map_name": "Bottom of the Cliff",
        "events": {
            "RF_FixedVeranda": HasHammer() | CanUseAbilityBombette(),
        },
        "locations": {
            "GR Bottom of the Cliff Block On Ground": CanHitGroundedBlocks(),
            "GR Bottom of the Cliff In Tree": CanShakeTrees(),
        },
        "exits": {
            "GR Jr. Troopa's Playground": None,
            "GR Bottom of the Cliff East": HasHammer() | CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "GR Bottom of the Cliff East",
        "area_id": "0",
        "map_id": "2",
        "map_name": "Bottom of the Cliff",
        "events": {
            "RF_FixedVeranda": HasHammer() | CanUseAbilityBombette(),
        },
        "locations": {
            "GR Bottom of the Cliff Hidden Panel": CanFlipPanels(),
            "GR Bottom of the Cliff Above Stone Block": (
                HasSuperHammer()
                & CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
            "GR Bottom of the Cliff Floating Coin 1": CanClimbSteps(),
            "GR Bottom of the Cliff Floating Coin 2": CanClimbSteps(),
            "GR Bottom of the Cliff Floating Coin 3": CanClimbSteps(),
            "GR Bottom of the Cliff Floating Coin 4": CanClimbSteps(),
            "GR Bottom of the Cliff Upper Ledge": CanClimbSteps(),
        },
        "exits": {
            "GR Behind the Village West": None,
            "GR Bottom of the Cliff West": HasHammer() | CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "GR Jr. Troopa's Playground",
        "area_id": "0",
        "map_id": "3",
        "map_name": "Jr. Troopa's Playground",
        "locations": {
            "GR Jr. Troopa's Playground In Tree Left": CanShakeTrees(),
            "GR Jr. Troopa's Playground In Tree Top": CanShakeTrees(),
            "GR Jr. Troopa's Playground In Tree Right": CanShakeTrees(),
            "GR Jr. Troopa's Playground Bush Right": None,
            "GR Jr. Troopa's Playground Bush Bottom Right": None,
            "GR Jr. Troopa's Playground Bush Top 1": None,
            "GR Jr. Troopa's Playground Bush Top 2": None,
            "GR Jr. Troopa's Playground Bush Center": None,
            "GR Jr. Troopa's Playground Bush Top Left": None,
            "GR Jr. Troopa's Playground In Hammer Bush": None,
            "GR Jr. Troopa's Playground In MultiCoinBlock": CanHitGroundedBlocks(),
        },
        "exits": {
            "GR Bottom of the Cliff West": None,
        }
    },
    {
        "region_name": "GR Goomba Road 1",
        "area_id": "0",
        "map_id": "7",
        "map_name": "Goomba Road 1",
        "locations": {
            "GR Goomba Road 1 Yellow Block Left": CanHitFloatingBlocks(),
            "GR Goomba Road 1 Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "GR Goomba Village Exit East": None,
            "GR Goomba Road 2": None,
        }
    },
    {
        "region_name": "GR Goomba Road 2",
        "area_id": "0",
        "map_id": "5",
        "map_name": "Goomba Road 2",
        "locations": {
            "GR Goomba Road 2 On the Sign": None,
            "GR Goomba Road 2 Red Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "GR Goomba Road 1": None,
            "GR Goomba Road 3 West": None,
        }
    },
    {
        "region_name": "GR Goomba Road 3 West",
        "area_id": "0",
        "map_id": "6",
        "map_name": "Goomba Road 3",
        "events": {
            "RF_BeatGoombaBros": None,
        },
        "exits": {
            "GR Goomba Road 2": None,
            "GR Goomba Road 3 East": CanClimbSteps(),
        }
    },
    {
        "region_name": "GR Goomba Road 3 East",
        "area_id": "0",
        "map_id": "6",
        "map_name": "Goomba Road 3",
        "exits": {
            "GR Goomba Road 4": None,
            "GR Goomba Road 3 West": None,
        }
    },
    {
        "region_name": "GR Goomba Road 4",
        "area_id": "0",
        "map_id": "10",
        "map_name": "Goomba Road 4",
        "exits": {
            "GR Goomba Road 3 East": None,
            "GR Goomba King's Castle West": None,
        }
    },
    {
        "region_name": "GR Goomba King's Castle West",
        "area_id": "0",
        "map_id": "9",
        "map_name": "Goomba King's Castle",
        "events": {
            "RF_BeatGoombaKing": Has("RF_BeatGoombaBros") & CanHitGroundedSwitches(),
        },
        "locations": {
            "GR Goomba King's Castle In Tree Left Of Fortress": CanShakeTrees(),
        },
        "exits": {
            "GR Goomba Road 4": None,
            "GR Goomba King's Castle East": Has(
                "RF_BeatGoombaKing",
                options=[OptionFilter(
                    OpenPrologue,
                    False
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "GR Goomba King's Castle East",
        "area_id": "0",
        "map_id": "9",
        "map_name": "Goomba King's Castle",
        "locations": {
            "GR Goomba King's Castle Hidden Panel": CanFlipPanels(),
            "GR Goomba King's Castle Hidden Yellow Block": (
                CanHitGroundedBlocks() & CanHitFloatingBlocks()
            ),
            "GR Goomba King's Castle In Tree Right Of Cliff": CanShakeTrees(),
        },
        "exits": {
            "GR Toad Town Entrance West": None,
            "GR Goomba King's Castle West": Has(
                "RF_BeatGoombaKing",
                options=[OptionFilter(
                    OpenPrologue,
                    False
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "GR Toad Town Entrance West",
        "area_id": "0",
        "map_id": "8",
        "map_name": "Toad Town Entrance",
        "exits": {
            "GR Goomba King's Castle East": None,
            "GR Toad Town Entrance East": None,
        }
    },
    {
        "region_name": "GR Toad Town Entrance East",
        "area_id": "0",
        "map_id": "8",
        "map_name": "Toad Town Entrance",
        "locations": {
            "GR Toad Town Entrance Yellow Block": CanHitFloatingBlocks(),
            "GR Toad Town Entrance Chest On Roof": CanShakeTrees() & CanClimbSteps(),
        },
        "exits": {
            "TT Gate District": None,
            "GR Toad Town Entrance West": CanClimbSteps(),
        }
    },
    {
        "region_name": "GR Mario's House",
        "area_id": "0",
        "map_id": "11",
        "map_name": "Mario's House",
        "locations": {
            "GR Mario's House Luigi Koopa Koot Favor": Has("FAVOR_2_03_active"),
        },
        "exits": {
            "GR Mario's House Warp Pipe": HasBoots(),
        }
    },
    {
        "region_name": "GR Mario's House Warp Pipe",
        "area_id": "0",
        "map_id": "11",
        "map_name": "Mario's House",
        "exits": {
            "GR Mario's House": None,
            "TT Gate District Mario's House Pipe": CanReenterVerticalPipes(),
        }
    }
]
