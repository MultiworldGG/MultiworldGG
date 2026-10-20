from typing import Dict
import dataclasses

from typing_extensions import override

from rule_builder.rules import (
    #And,
    #Or,
    #AtLeast,
    True_,
    #False_,
    Has,
    HasAll,
    HasAny,
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
from rule_builder.field_resolvers import FromOption

from .LogicHelpers import (
    HasHammer,
    #HasSuperHammer,
    #HasUltraHammer,
    HasBoots,
    HasSuperBoots,
    #HasUltraBoots,
    CanFlipPanels,
    #CanSeeHiddenBlocks,
    CanShakeTrees,
    #CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanUseAbilityBow,
    #CanUseAbilityWatt,
    CanUseAbilitySushie,
    #CanUseAbilityLakilester,
    #CanHitGroundedBlocks,
    #CanHitFloatingBlocks,
    #CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

from ...options import (
    MagicalSeedsRequired,
    CookWithoutFryingPan,
    OpenForest,
    OpenBlueHouse,
    OpenMtRugged,
    OpenToybox,
    OpenWhale,
)

toad_town_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "TT Gate District",
        "area_id": "1",
        "map_id": "1",
        "map_name": "Gate District",
        "events": {
            "RF_RadioTradeEvt1Done": HasAll("RF_RadioTradeEvt1", "Koopa Leaf"),
            "RF_CanVisitRussT": None
        },
        "locations": {
            "TT Gate District Hidden Panel": CanFlipPanels(),
            "TT Gate District Sushie Island": CanUseAbilitySushie(),
            "TT Gate District Russ T. Dictionary Reward": Has("Dictionary"),
            "TT Gate District Russ T. Letter Reward": CanUseAbilityParakarry() & Has("Letter to Russ T"),
            "TT Gate District Miss T. Letter Reward": CanUseAbilityParakarry() & Has("Letter to Miss T"),
            "TT Gate District Radio Trade Event 1 Reward": HasAll("RF_RadioTradeEvt1", "Koopa Leaf"),
            "TT Gate District Shop Item 1": None,
            "TT Gate District Shop Item 2": None,
            "TT Gate District Shop Item 3": None,
            "TT Gate District Shop Item 4": None,
            "TT Gate District Shop Item 5": None,
            "TT Gate District Shop Item 6": None,
            "TT Gate District Dojo: Chan": HasBoots() | HasAny("Goombario", "Watt", "Sushie"),
            "TT Gate District Dojo: Lee": (
                Has("STARSPIRIT", count=1)
                & (HasBoots() | HasAny("Goombario", "Watt", "Sushie"))
            ),
            "TT Gate District Dojo: Master 1": (
                Has("STARSPIRIT", count=3)
                & (HasBoots() | HasAny("Goombario", "Watt", "Sushie"))
            ),
            "TT Gate District Dojo: Master 2": (
                Has("STARSPIRIT", count=4)
                & (HasBoots() | HasAny("Goombario", "Watt", "Sushie"))
            ),
            "TT Gate District Dojo: Master 3": (
                Has("STARSPIRIT", count=5)
                & (HasBoots() | HasAny("Goombario", "Watt", "Sushie"))
            ),
        },
        "exits": {
            "GR Toad Town Entrance East": None,
            "TT Plaza District": None,
            "TT Gate District Island": CanUseAbilitySushie(),
            "TT Gate District Mario's House Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "TT Gate District Island Pipe",
        "area_id": "1",
        "map_id": "1",
        "map_name": "Gate District",
        "exits": {
            "TTT Under the Toad Town Pond": CanReenterVerticalPipes(),
            "TT Gate District Island": None,
        }
    },
    {
        "region_name": "TT Gate District Island",
        "area_id": "1",
        "map_id": "1",
        "map_name": "Gate District",
        "exits": {
            "TT Gate District Island Pipe": CanClimbSteps(),
            "TT Gate District": CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "TT Gate District Mario's House Pipe",
        "area_id": "1",
        "map_id": "1",
        "map_name": "Gate District",
        "exits": {
            "GR Mario's House Warp Pipe": CanReenterVerticalPipes(),
            "TT Gate District": None,
        }
    },
    {
        "region_name": "TT Plaza District",
        "area_id": "1",
        "map_id": "2",
        "map_name": "Plaza District",
        "events": {
            "RF_CanReadToadTownNews": None,
            "StarPiece_MAC_1": None,
            "StarPiece_MAC_5": Has("STARSPIRIT", count=2),
            "StarPiece_MAC_9": Has("STARSPIRIT", count=4),
            "StarPiece_MAC_13": Has("STARSPIRIT", count=6),
        },
        "locations": {
            "TT Plaza District Merlon House Stomping": HasSuperBoots(),
            "TT Plaza District Rowf's Calculator Reward": Has("Calculator"),
            "TT Plaza District Postmaster MailBag Reward": Has("Mailbag"),
            "TT Plaza District Merlon Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Merlon")
            ),
            "TT Plaza District Minh T. Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Minh T")
            ),
            "TT Plaza District In Tree": CanShakeTrees(),
            "TT Plaza District Rowf's Shop Set 1 - 1": None,
            "TT Plaza District Rowf's Shop Set 1 - 2": None,
            "TT Plaza District Rowf's Shop Set 1 - 3": None,
            "TT Plaza District Rowf's Shop Set 1 - 4": None,
            "TT Plaza District Rowf's Shop Set 2 - 1": Has("STARSPIRIT", count=1),
            "TT Plaza District Rowf's Shop Set 2 - 2": Has("STARSPIRIT", count=1),
            "TT Plaza District Rowf's Shop Set 2 - 3": Has("STARSPIRIT", count=1),
            "TT Plaza District Rowf's Shop Set 3 - 1": Has("STARSPIRIT", count=2),
            "TT Plaza District Rowf's Shop Set 3 - 2": Has("STARSPIRIT", count=2),
            "TT Plaza District Rowf's Shop Set 3 - 3": Has("STARSPIRIT", count=2),
            "TT Plaza District Rowf's Shop Set 4 - 1": Has("STARSPIRIT", count=3),
            "TT Plaza District Rowf's Shop Set 4 - 2": Has("STARSPIRIT", count=3),
            "TT Plaza District Rowf's Shop Set 4 - 3": Has("STARSPIRIT", count=3),
            "TT Plaza District Rowf's Shop Set 5 - 1": Has("STARSPIRIT", count=4),
            "TT Plaza District Rowf's Shop Set 5 - 2": Has("STARSPIRIT", count=4),
            "TT Plaza District Rowf's Shop Set 5 - 3": Has("STARSPIRIT", count=4),
        },
        "exits": {
            "TT Gate District": None,
            "KR Pleasant Path Entry West": None,
            "PCG Ruined Castle Grounds": None,
            "TT Southern District": None,
            "FLO Fields Center": Has("Magical Seed", count=FromOption(MagicalSeedsRequired)),
        }
    },
    {
        "region_name": "TT Southern District",
        "area_id": "1",
        "map_id": "3",
        "map_name": "Southern District",
        "events": {
            "GF_MAC02_UnlockedHouse": Has("Odd Key"),
            "RF_CanCook": Has(
                "Frying Pan",
                options=[OptionFilter(
                    CookWithoutFryingPan,
                    False
                )],
                filtered_resolution=True,
            ),
            "RF_CanVisitTayceT": None,
            "AF_CanMakeKoopaTea": HasAll("RF_CanCook", "Koopa Leaf"),
            "AF_CanMakeNuttyCake": HasAll("RF_CanCook", "Goomnut"),
            "AF_CanMakeCake": HasAll("RF_CanCook", "Cake Mix"),
            "AF_CanMakeLemonCandy": HasAll("RF_CanCook", "Cookbook", "Cake Mix", "Lemon"),
            "AF_CanMakeKoopasta": HasAll(
                "RF_CanCook",
                "Cookbook",
                "Koopa Leaf",
                "Dried Pasta",
            ),
            "AF_CanMakeKookyCookie": HasAll("RF_CanCook", "Cookbook", "Koopa Leaf", "Cake Mix"),
            "AF_CanMakeLifeShroom": (
                HasAll(
                    "RF_CanCook",
                    "Cookbook",
                    "Super Shroom",
                )
                & HasAny("Koopa Leaf", "Goomnut")
            ),
            "AF_CanMakeSleepySheep": (
                HasAll(
                    "RF_CanCook",
                    "Cookbook",
                    "Strange Leaf",
                )
                & HasAny("Blue Berry", "Yellow Berry", "Red Berry")
            ),
            "AF_CanMakeTastyTonic": (
                Has("RF_CanCook")
                & (HasAny("Lemon", "Lime", "Coconut")
                   | HasAll("Cookbook", "Bubble Berry")
                )
            ),
        },
        "locations": {
            "TT Southern District Bub-ulb Gift": CanClimbSteps(),
            "TT Southern District Tayce T. Frying Pan Reward": Has("Frying Pan"),
            "TT Southern District Fice T. Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Fice T")
            ),
            "TT Southern District Fice T. Forest Pass": True_(
                options=[OptionFilter(
                    OpenForest,
                    False
                )],
                filtered_resolution=False,
            ),
            "TT Southern District Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "TT Residental District": None,
            "FOR Exit to Toad Town": None,
            "TT Plaza District": None,
            "TT Station District": None,
            "TT Southern District Sewers Pipe": CanClimbSteps(),
            "TT Southern District Odd House": Has("GF_MAC02_UnlockedHouse"),
        }
    },
    {
        "region_name": "TT Southern District Sewers Pipe",
        "area_id": "1",
        "map_id": "3",
        "map_name": "Southern District",
        "exits": {
            "TTT Sewer Entrance (B1)": CanReenterVerticalPipes(),
            "TT Southern District": None,
        }
    },
    {
        "region_name": "TT Southern District Odd House",
        "area_id": "1",
        "map_id": "3",
        "map_name": "Southern District",
        "events": {
            "GF_MAC02_UnlockedHouse": Has(
                "Odd Key",
                options=[OptionFilter(
                    OpenBlueHouse,
                    False
                )],
                filtered_resolution=True,
            ),
        },
        "locations": {
            "TT Southern District Inside Blue House": None,
        },
        "exits": {
            "TT Southern District": Has("GF_MAC02_UnlockedHouse"),
            "TT Southern District Odd House Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "TT Southern District Odd House Pipe",
        "area_id": "1",
        "map_id": "3",
        "map_name": "Southern District",
        "exits": {
            "TTT Rip Cheato's Home (B3)": CanReenterVerticalPipes(),
            "TT Southern District Odd House": None,
        }
    },
    {
        "region_name": "TT Station District",
        "area_id": "1",
        "map_id": "4",
        "map_name": "Station District",
        "events": {
            "GF_MAC03_BombedRock": CanUseAbilityBombette(
                options=[OptionFilter(
                    OpenMtRugged,
                    False
                )],
                filtered_resolution=True,
            ),
        },
        "locations": {
            "TT Station District Dane T. Letter Reward 1": (
                CanUseAbilityParakarry()
                & Has("Letter to Dane T 1")
                & HasBoots()
            ),
            "TT Station District Dane T. Letter Reward 2": (
                CanUseAbilityParakarry()
                & Has("Letter to Dane T 2")
                & HasBoots()
            ),
            "TT Station District Hidden Panel": CanFlipPanels(),
        },
        "exits": {
            "TT Southern District": None,
            "TT Station District Train": Has("GF_MAC03_BombedRock"),
            "TT Station District Pipe": CanShakeTrees() & CanClimbSteps(),
        }
    },
    {
        "region_name": "TT Station District Train",
        "area_id": "1",
        "map_id": "4",
        "map_name": "Station District",
        "events": {
            "GF_MAC03_BombedRock": None,
        },
        "exits": {
            "MR Train Ride Scene": None,
            "TT Station District": None,
        }
    },
    {
        "region_name": "TT Station District Pipe",
        "area_id": "1",
        "map_id": "4",
        "map_name": "Station District",
        "exits": {
            "MGM Playroom Lobby": CanReenterVerticalPipes(),
            "TT Station District": None,
        }
    },
    {
        "region_name": "TT Residental District",
        "area_id": "1",
        "map_id": "5",
        "map_name": "Residental District",
        "events": {
            "StarPiece_MAC_1": None,
            "StarPiece_MAC_5": Has("STARSPIRIT", count=2),
            "StarPiece_MAC_9": Has("STARSPIRIT", count=4),
            "StarPiece_MAC_13": Has("STARSPIRIT", count=6),
        },
        "locations": {
            "TT Residental District Storeroom Item 1": Has("Storeroom Key"),
            "TT Residental District Storeroom Item 2": Has("Storeroom Key"),
            "TT Residental District Storeroom Item 3": Has("Storeroom Key"),
            "TT Residental District Storeroom Item 4": Has("Storeroom Key"),
            "TT Residental District Shop Item 1": None,
            "TT Residental District Shop Item 2": None,
            "TT Residental District Shop Item 3": None,
            "TT Residental District Shop Item 4": None,
            "TT Residental District Shop Item 5": None,
            "TT Residental District Shop Item 6": None,
        },
        "exits": {
            "TT Southern District": None,
            "TT Port District": None,
            "TT Residental District Toybox Room": CanUseAbilityBow(
                options=[OptionFilter(
                    OpenToybox,
                    False
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "TT Residental District Toybox Room",
        "area_id": "1",
        "map_id": "5",
        "map_name": "Residental District",
        "events": {
            "MF_Ch4_CanThrowInTrain": None,
        },
        "exits": {
            "SGT BLU Station": CanClimbSteps(),
            "TT Residental District": None,
        }
    },
    {
        "region_name": "TT Port District",
        "area_id": "1",
        "map_id": "6",
        "map_name": "Port District",
        "events": {
            "RF_RadioTradeEvt3Done": HasAll("RF_RadioTradeEvt3", "Coconut"),
            "StarPiece_MAC_1": None,
            "StarPiece_MAC_5": Has("STARSPIRIT", count=2),
            "StarPiece_MAC_9": Has("STARSPIRIT", count=4),
            "StarPiece_MAC_13": Has("STARSPIRIT", count=6),
        },
        "locations": {
            "TT Port District Poet Gift": None,
            "TT Port District Poet Melody Reward": Has("Melody"),
            "TT Port District Fishmael Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Fishmael")
            ),
            "TT Port District Radio Trade Event 3 Reward": HasAll("RF_RadioTradeEvt3", "Coconut"),
            "TT Port District Hidden Panel": CanFlipPanels(),
            "TT Port District In MultiCoinBlock": HasBoots(),
        },
        "exits": {
            "TT Residental District": None,
            "TT Riding the Whale": Has(
                "RF_CanRideWhale",
                options=[OptionFilter(
                    OpenWhale,
                    False
                )],
                filtered_resolution=True,
            ),
            "ITW Whale Mouth": HasHammer() | HasSuperBoots() | CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "TT Riding the Whale",
        "area_id": "1",
        "map_id": "7",
        "map_name": "Riding the Whale",
        "exits": {
            "TT Port District": None,
            "JJ Whale Cove": None,
        }
    },
    {
        "region_name": "PCG Ruined Castle Grounds",
        "area_id": "23",
        "map_id": "1",
        "map_name": "Ruined Castle Grounds",
        "locations": {
            "PCG Ruined Castle Grounds Muss T. Letter Reward": (
                CanUseAbilityParakarry()
                & Has("Letter to Muss T")
            ),
        },
        "exits": {
            "TT Plaza District": None,
            "SSS Shooting Star Path": None,
        }
    }
]
