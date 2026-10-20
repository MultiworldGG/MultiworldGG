from typing import Dict

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    #True_,
    #False_,
    #Has,
    #HasAll,
    #HasAny,
    #HasAllCounts,
    #HasAnyCount,
    HasFromList,
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
    #HasUltraHammer,
    HasBoots,
    #HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    #CanSeeHiddenBlocks,
    #CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    #CanUseAbilityBow,
    #CanUseAbilityWatt,
    #CanUseAbilitySushie,
    CanUseAbilityLakilester,
    CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    #CanReenterVerticalPipes,
)

mt_rugged_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "MR Mt Rugged 1 West",
        "area_id": "8",
        "map_id": "0",
        "map_name": "Mt Rugged 1",
        "locations": {
            "MR Mt Rugged 1 On Slide 1": None,
        },
        "exits": {
            "MR Train Station Upper Exit": None,
            "MR Mt Rugged 1 East": CanClimbSteps(),
            "MR Mt Rugged 1 On Slide": CanUseAbilityKooper() | CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "MR Mt Rugged 1 On Slide",
        "area_id": "8",
        "map_id": "0",
        "map_name": "Mt Rugged 1",
        "locations": {
            "MR Mt Rugged 1 On Slide 2": None,
            "MR Mt Rugged 1 On Slide 3": None,
        },
        "exits": {
            "MR Mt Rugged 1 West": None,
            "MR Mt Rugged 1 East": CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "MR Mt Rugged 1 East",
        "area_id": "8",
        "map_id": "0",
        "map_name": "Mt Rugged 1",
        "exits": {
            "MR Mt Rugged 1 On Slide": CanClimbSteps(),
            "MR Mt Rugged 2 West": None,
            "MR Mt Rugged 1 West": None,
            "MR Mt Rugged 1 East Lower": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 1 East Lower",
        "area_id": "8",
        "map_id": "0",
        "map_name": "Mt Rugged 1",
        "locations": {
            "MR Mt Rugged 1 Hurting Whacka": HasHammer() | CanUseAbilityBombette(),
            "MR Mt Rugged 1 Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "MR Mt Rugged 1 East": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 2 West",
        "area_id": "8",
        "map_id": "1",
        "map_name": "Mt Rugged 2",
        "exits": {
            "MR Mt Rugged 1 East": None,
            "MR Mt Rugged 2 Center": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 2 Center",
        "area_id": "8",
        "map_id": "1",
        "map_name": "Mt Rugged 2",
        "locations": {
            "MR Mt Rugged 2 Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "MR Mt Rugged 2 East Lower": HasBoots(),
            "MR Mt Rugged 2 West": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 2 East Lower",
        "area_id": "8",
        "map_id": "1",
        "map_name": "Mt Rugged 2",
        "locations": {
            "MR Mt Rugged 2 Kooper Ledge": CanUseAbilityKooper() | CanUseAbilityParakarry(),
            "MR Mt Rugged 2 Parakarry Ledge": CanUseAbilityParakarry(),
        },
        "exits": {
            "MR Mt Rugged 3 Lower": None,
            "MR Mt Rugged 2 Center": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 2 East Upper",
        "area_id": "8",
        "map_id": "1",
        "map_name": "Mt Rugged 2",
        "exits": {
            "MR Mt Rugged 3 Upper": None,
            "MR Mt Rugged 2 West Upper": None,
        }
    },
    {
        "region_name": "MR Mt Rugged 2 West Upper",
        "area_id": "8",
        "map_id": "1",
        "map_name": "Mt Rugged 2",
        "exits": {
            "MR Mt Rugged 4": None,
            "MR Mt Rugged 2 Center": None,
        }
    },
    {
        "region_name": "MR Mt Rugged 3 Lower",
        "area_id": "8",
        "map_id": "2",
        "map_name": "Mt Rugged 3",
        "exits": {
            "MR Mt Rugged 2 East Lower": None,
            "MR Mt Rugged 3 Upper": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Mt Rugged 3 Upper",
        "area_id": "8",
        "map_id": "2",
        "map_name": "Mt Rugged 3",
        "locations": {
            "MR Mt Rugged 3 On Scaffolding": None,
            "MR Mt Rugged 3 Bub-ulb Gift": CanUseAbilityParakarry(),
        },
        "exits": {
            "MR Mt Rugged 3 Lower": None,
            "MR Suspension Bridge West": None,
            "MR Mt Rugged 2 East Upper": None,
        }
    },
    {
        "region_name": "MR Mt Rugged 4",
        "area_id": "8",
        "map_id": "3",
        "map_name": "Mt Rugged 4",
        "locations": {
            "MR Mt Rugged 4 Hidden Cave Chest": CanClimbSteps(),
            "MR Mt Rugged 4 Slide Ledge": CanClimbSteps(),
            "MR Mt Rugged 4 Left Ledge Center": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Left Ledge Right": (
                CanClimbSteps()
                & (CanUseAbilityKooper() | CanUseAbilityParakarry())
            ),
            "MR Mt Rugged 4 Left Ledge 3": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Left Ledge 4": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Left Ledge 5": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Left Ledge 6": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Left Ledge 7": CanUseAbilityParakarry(),
            "MR Mt Rugged 4 Bottom Left 1": CanClimbSteps(),
            "MR Mt Rugged 4 Bottom Left 2": CanClimbSteps(),
            "MR Mt Rugged 4 Yellow Block Top Left": CanHitGroundedBlocks() & CanClimbSteps(),
            "MR Mt Rugged 4 Yellow Block Floating": CanHitFloatingBlocks(),
            "MR Mt Rugged 4 Yellow Block Top Right": CanHitGroundedBlocks() & CanClimbSteps(),
        },
        "exits": {
            "MR Mt Rugged 2 West Upper": None,
        }
    },
    {
        "region_name": "MR Suspension Bridge West",
        "area_id": "8",
        "map_id": "4",
        "map_name": "Suspension Bridge",
        "locations": {
            "MR Suspension Bridge Bottom Of Cliff": None,
        },
        "exits": {
            "MR Mt Rugged 3 Upper": None,
            "MR Suspension Bridge East": CanUseAbilityParakarry(),
        }
    },
    {
        "region_name": "MR Suspension Bridge East",
        "area_id": "8",
        "map_id": "4",
        "map_name": "Suspension Bridge",
        "exits": {
            "DDD Desert Rugged Entrance West": None,
            "MR Suspension Bridge West": CanClimbSteps(),
        }
    },
    {
        "region_name": "MR Train Station Upper Exit",
        "area_id": "8",
        "map_id": "5",
        "map_name": "Train Station",
        "locations": {
            "MR Train Station Parakarry Partner": HasFromList(
                "Letter to Merlon",
                "Letter to Goompa",
                "Letter to Mort T",
                "Letter to Russ T",
                "Letter to Mayor Penguin",
                "Letter to Merlow",
                "Letter to Fice T",
                "Letter to Nomadimouse",
                "Letter to Minh T",
                "Letter to Goompapa 1",
                "Letter to Igor",
                "Letter to Franky",
                "Letter to Muss T",
                "Letter to Koover 1",
                "Letter to Fishmael",
                "Letter to Koover 2",
                "Letter to Mr E",
                "Letter to Miss T",
                "Letter to Little Mouser",
                "Letter to Dane T 1",
                "Letter to Red Yoshi Kid",
                "Letter to Dane T 2",
                "Letter to Frost T",
                "Letter to Goompapa 2",
                "Letter to Kolorado",
                count=3
            ),
            "MR Train Station In SuperBlock": HasSuperHammer() & CanHitFloatingBlocks(),
        },
        "exits": {
            "MR Mt Rugged 1 West": None,
            "MR Train Station Lower": HasBoots(),
        }
    },
    {
        "region_name": "MR Train Station Lower",
        "area_id": "8",
        "map_id": "5",
        "map_name": "Train Station",
        "locations": {
            "MR Train Station Bush 1": None,
            "MR Train Station Bush 2": None,
            "MR Train Station Bush 3": None,
            "MR Train Station Bush Top": None,
        },
        "exits": {
            "MR Train Station Upper Exit": HasBoots(),
            "MR Train Station Platform": HasBoots(),
        }
    },
    {
        "region_name": "MR Train Station Platform",
        "area_id": "8",
        "map_id": "5",
        "map_name": "Train Station",
        "exits": {
            "MR Train Station Lower": HasBoots(),
            "MR Train Ride Scene": None
        }
    },
    {
        "region_name": "MR Train Ride Scene",
        "area_id": "8",
        "map_id": "6",
        "map_name": "Train Ride Scene",
        "exits": {
            "TT Station District Train": None,
            "MR Train Station Platform": None,
        }
    }
]
