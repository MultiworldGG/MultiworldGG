from typing import Dict

from rule_builder.rules import (
    And,
    #Or,
    #AtLeast,
    True_,
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
)

from .LogicHelpers import (
    HasBoots,
    HasSuperBoots,
    HasHammer,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanClimbSteps,
    CanFlipPanels,
)

boos_mansion_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "BM Foyer 1F",
        "area_id": "13",
        "map_id": "0",
        "map_name": "Foyer",
        "locations": {
            "BM Foyer From Franky (Koopa Koot Favor)": HasAll(
                "RF_OpenedGustyGulch",
                "FAVOR_5_02_active",
            ),
            "BM Foyer Franky Letter Reward": HasAll(
                "RF_OpenedGustyGulch",
                "Letter to Franky",
            ) & CanUseAbilityParakarry(),
            "BM Foyer Hidden Panel": True_() & CanFlipPanels()
        },
        "exits": {
            "FOR Outside Boo's Mansion Steps": None,
            "BM Pot Room": None,
            "BM Basement Stairs Upper": Has("Boo Weight") & CanClimbSteps(),
            "BM Foyer 2F": (HasBoots() | Has("Boo Weight")) & CanClimbSteps()
        }
    },
    {
      "region_name": "BM Foyer 2F",
      "area_id": "13",
      "map_id": "0",
      "map_name": "Foyer",
      "exits": {
        "BM Record Player Room": None,
        "BM Record Room": None,
        "BM Foyer 1F": None,
        "BM Foyer 3F": Has("Boo Portrait")
      }
    },
    {
      "region_name": "BM Foyer 3F",
      "area_id": "13",
      "map_id": "0",
      "map_name": "Foyer",
      "exits": {
        "BM Lady Bow's Room": None,
        "BM Foyer 2F": None
      }
    },
    {
      "region_name": "BM Basement Stairs Upper",
      "area_id": "13",
      "map_id": "1",
      "map_name": "Basement Stairs",
      "exits": {
        "BM Foyer 1F": None,
        "BM Basement Stairs Lower": None
      }
    },
    {
      "region_name": "BM Basement Stairs Lower",
      "area_id": "13",
      "map_id": "1",
      "map_name": "Basement Stairs",
      "locations": {
        "BM Basement Stairs Hidden Panel": CanFlipPanels()
      },
      "exits": {
        "BM Mansion Basement Upper": None,
        "BM Basement Stairs Upper": HasBoots(),
        "BM Library Lower": CanUseAbilityBombette()
      }
    },
    {
      "region_name": "BM Mansion Basement Upper",
      "area_id": "13",
      "map_id": "2",
      "map_name": "Basement",
      "locations": {
        "BM Basement In Crate": HasSuperBoots()
      },
      "exits": {
        "BM Basement Stairs Lower": None,
        "BM Super Boots Room": None,
        "BM Mansion Basement Lower": Has("RF_OBK03_BuiltStairs")
      }
    },
    {
      "region_name": "BM Mansion Basement Lower",
      "area_id": "13",
      "map_id": "2",
      "map_name": "Basement",
      "events": {
        "RF_OBK03_BuiltStairs": HasBoots(),
      },
      "locations": {
        "BM Basement Igor Letter Reward": CanUseAbilityParakarry() & Has("Letter to Igor"),
        "BM Basement Shop Item 1": Has("RF_OpenedGustyGulch"),
        "BM Basement Shop Item 2": Has("RF_OpenedGustyGulch"),
        "BM Basement Shop Item 3": Has("RF_OpenedGustyGulch"),
        "BM Basement Shop Item 4": Has("RF_OpenedGustyGulch"),
        "BM Basement Shop Item 5": Has("RF_OpenedGustyGulch"),
        "BM Basement Shop Item 6": Has("RF_OpenedGustyGulch"),
      },
      "exits": {
        "BM Mansion Basement Upper": Has("RF_OBK03_BuiltStairs")
      }
    },
    {
      "region_name": "BM Super Boots Room",
      "area_id": "13",
      "map_id": "3",
      "map_name": "Super Boots Room",
      "events": {
        "RF_OBK04_OpenedBigChest": HasBoots() | HasHammer()
      },
      "locations": {
        "BM Super Boots Room In Crate": HasSuperBoots(),
        "BM Super Boots Room In Big Chest": HasBoots() | HasHammer(),
        "BM Super Boots Room Hidden Panel": CanFlipPanels()
      },
      "exits": {
        "BM Mansion Basement Lower": Has("RF_OBK04_OpenedBigChest")
      }
    },
    {
      "region_name": "BM Pot Room",
      "area_id": "13",
      "map_id": "4",
      "map_name": "Pot Room",
      "locations": {
        "BM Pot Room In Crate 1": HasSuperBoots(),
        "BM Pot Room In Crate 2": HasSuperBoots()
      },
      "exits": {
        "BM Foyer 1F": None,
        "BM Library Upper": And(HasSuperBoots(), CanUseAbilityBombette())
      }
    },
    {
      "region_name": "BM Library Upper",
      "area_id": "13",
      "map_id": "5",
      "map_name": "Library",
      "locations": {
        "BM Library In Crate": HasSuperBoots(),
        "BM Library On Bookshelf": CanUseAbilityParakarry()
      },
      "exits": {
        "BM Library Lower": None
      }
    },
    {
      "region_name": "BM Library Lower",
      "area_id": "13",
      "map_id": "5",
      "map_name": "Library",
      "exits": {
        "BM Basement Stairs Lower": CanUseAbilityBombette()
      }
    },
    {
      "region_name": "BM Record Player Room",
      "area_id": "13",
      "map_id": "6",
      "map_name": "Record Player Room",
      "locations": {
        "BM Record Player Room In Chest": Has("Boo Record")
      },
      "exits": {
        "BM Foyer 2F": None
      }
    },
    {
      "region_name": "BM Record Room",
      "area_id": "13",
      "map_id": "7",
      "map_name": "Record Room",
      "locations": {
        "BM Record Room Hidden Panel": CanFlipPanels(),
        "BM Record Room Beat Boo Game": HasBoots() | HasHammer()
      },
      "exits": {
        "BM Foyer 2F": None
      }
    },
    {
      "region_name": "BM Lady Bow's Room",
      "area_id": "13",
      "map_id": "8",
      "map_name": "Lady Bow's Room",
      "events": {
        "RF_OpenedGustyGulch": None
      },
      "locations": {
        "BM Lady Bow's Room Bow Partner": None
      },
      "exits": {
        "BM Foyer 3F": None
      }
    }
]
