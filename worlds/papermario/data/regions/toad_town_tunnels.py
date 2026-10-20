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
    #HasAll,
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

from .LogicHelpers import (
    HasHammer,
    HasSuperHammer,
    HasUltraHammer,
    HasBoots,
    HasSuperBoots,
    HasUltraBoots,
    CanFlipPanels,
    CanSeeHiddenBlocks,
    CanShakeTrees,
    CanUseAbilityKooper,
    CanUseAbilityBombette,
    CanUseAbilityParakarry,
    CanUseAbilityBow,
    CanUseAbilityWatt,
    CanUseAbilitySushie,
    CanUseAbilityLakilester,
    CanHitGroundedBlocks,
    CanHitFloatingBlocks,
    CanHitGroundedSwitches,
    CanClimbSteps,
    CanReenterVerticalPipes,
)

from ...options import BlooperDamageRequirements, Chapter7BridgeVisible, GearShuffleMode

class CanBeatAllBloopers(Rule["PaperMarioWorld"], game="Paper Mario"):
    @override
    def _instantiate(self, world) -> Rule.Resolved:
        has_weak_aerial_partner: Rule = HasAny("Goombario", "Parakarry")
        has_strong_aerial_partner: Rule = HasAny("Bow", "Watt", "Sushie", "Lakilester")

        can_beat_blooper: Rule = (
            True_()
            if world.options.blooper_damage_requirements == BlooperDamageRequirements.option_None
            else (
                HasSuperBoots()
                | (HasBoots() & has_weak_aerial_partner)
                | has_strong_aerial_partner
            )
        )

        can_beat_electro_blooper: Rule = (
            True_()
            if world.options.blooper_damage_requirements < BlooperDamageRequirements.option_Medium
            else (
                HasUltraBoots()
                | (HasSuperBoots() & (has_weak_aerial_partner | has_strong_aerial_partner))
            )
        )

        can_beat_super_blooper: Rule = (
            True_()
            if world.options.blooper_damage_requirements < BlooperDamageRequirements.option_High
            else (HasUltraBoots() & has_strong_aerial_partner)
        )

        return (
            can_beat_blooper
            & can_beat_electro_blooper
            & can_beat_super_blooper
        ).resolve(world)

toad_town_tunnels_regions: list[Dict[str, str | Dict[str, Rule | None]]] = [
    {
        "region_name": "TTT Warp Zone 1 (B1)",
        "area_id": "2",
        "map_id": "0",
        "map_name": "Warp Zone 1 (B1)",
        "events": {
            "GF_TIK01_WarpPipes": CanBeatAllBloopers() & CanHitGroundedSwitches(),
        },
        "exits": {
            "TTT Sewer Entrance (B1)": None,
            "TTT Short Elevator Room (B1)": CanBeatAllBloopers() & HasSuperHammer(),
            "TTT Warp Zone 1 (B1) Goomba Village Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
            "TTT Warp Zone 1 (B1) Koopa Village Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
            "TTT Warp Zone 1 (B1) Outpost Pipe": Has("GF_TIK01_WarpPipes") & HasBoots(),
        }
    },
    {
        "region_name": "TTT Warp Zone 1 (B1) Goomba Village Pipe",
        "area_id": "2",
        "map_id": "0",
        "map_name": "Warp Zone 1 (B1)",
        "exits": {
            "GR Goomba Village Pipe": CanReenterVerticalPipes(),
            "TTT Warp Zone 1 (B1)": None,
            "TTT Warp Zone 1 (B1) Koopa Village Pipe": (
                Has("GF_TIK01_WarpPipes")
                & CanUseAbilityParakarry()
            ),
        }
    },
    {
        "region_name": "TTT Warp Zone 1 (B1) Koopa Village Pipe",
        "area_id": "2",
        "map_id": "0",
        "map_name": "Warp Zone 1 (B1)",
        "exits": {
            "KR Koopa Village 2 Pipe": CanReenterVerticalPipes(),
            "TTT Warp Zone 1 (B1)": None,
            "TTT Warp Zone 1 (B1) Goomba Village Pipe": (
                    Has("GF_TIK01_WarpPipes")
                    & CanUseAbilityParakarry()
                ),
            "TTT Warp Zone 1 (B1) Outpost Pipe": (
                    Has("GF_TIK01_WarpPipes")
                    & CanUseAbilityParakarry()
                ),
            }
    },
    {
        "region_name": "TTT Warp Zone 1 (B1) Outpost Pipe",
        "area_id": "2",
        "map_id": "0",
        "map_name": "Warp Zone 1 (B1)",
        "exits": {
            "DDO Outpost 1 Pipe": CanReenterVerticalPipes(),
            "TTT Warp Zone 1 (B1)": None,
            "TTT Warp Zone 1 (B1) Koopa Village Pipe": (
                Has("GF_TIK01_WarpPipes")
                & CanUseAbilityParakarry()
            ),
        }
    },
    {
        "region_name": "TTT Blooper Boss 1 (B1)",
        "area_id": "2",
        "map_id": "1",
        "map_name": "Blooper Boss 1 (B1)",
        "locations": {
            "TTT Blooper Boss 1 (B1) Blooper Fight Reward": CanBeatAllBloopers(),
        },
        "exits": {
            "TTT Hall to Blooper 1 (B1)": None,
        }
    },
    {
        "region_name": "TTT Short Elevator Room (B1)",
        "area_id": "2",
        "map_id": "2",
        "map_name": "Short Elevator Room (B1)",
        "locations": {
            "TTT Short Elevator Room (B1) Yellow Block Center": CanHitFloatingBlocks(),
            "TTT Short Elevator Room (B1) Yellow Block Left": CanHitFloatingBlocks(),
            "TTT Short Elevator Room (B1) Yellow Block Right": CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Warp Zone 1 (B1)": None,
            "TTT Scales Room (B2) West": None,
        }
    },
    {
        "region_name": "TTT Scales Room (B2) West",
        "area_id": "2",
        "map_id": "3",
        "map_name": "Scales Room (B2)",
        "exits": {
            "TTT Spring Room (B2)": None,
            "TTT Short Elevator Room (B1)": None,
            "TTT Scales Room (B2) East": HasBoots(),
            "TTT Scales Room (B2) Lower": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Scales Room (B2) East",
        "area_id": "2",
        "map_id": "3",
        "map_name": "Scales Room (B2)",
        "exits": {
            "TTT Elevator Attic Room (B2) West": None,
            "TTT Scales Room (B2) West": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Scales Room (B2) Lower",
        "area_id": "2",
        "map_id": "3",
        "map_name": "Scales Room (B2)",
        "exits": {
            "TTT Scales Room (B2) Lower Pipe": CanClimbSteps(),
            "TTT Scales Room (B2) West": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Scales Room (B2) Lower Pipe",
        "area_id": "2",
        "map_id": "3",
        "map_name": "Scales Room (B2)",
        "exits": {
            "TTT Metal Block Room (B3)": CanReenterVerticalPipes(),
            "TTT Scales Room (B2) Lower": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Spring Room (B2)",
        "area_id": "2",
        "map_id": "4",
        "map_name": "Spring Room (B2)",
        "locations": {
            "TTT Spring Room (B2) Chest On Ledge": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Scales Room (B2) West": None,
        }
    },
    {
        "region_name": "TTT Sewer Entrance (B1)",
        "area_id": "2",
        "map_id": "5",
        "map_name": "Sewer Entrance (B1)",
        "exits": {
            "TTT Warp Zone 1 (B1)": HasSuperHammer(),
            "TTT Hall to Blooper 1 (B1)": HasHammer() | CanUseAbilityBombette(),
            "TT Southern District Sewers Pipe": None,
            "TTT Second Level Entry (B2) West": HasSuperBoots(),
        }
    },
    {
        "region_name": "TTT Sewer Entrance (B1) Tall Pipe",
        "area_id": "2",
        "map_id": "5",
        "map_name": "Sewer Entrance (B1)",
        "exits": {
            "TTT Sewer Entrance (B1)": None,
            "TTT Second Level Entry (B2) West": CanReenterVerticalPipes(),
        }
    },
    {
        "region_name": "TTT Elevator Attic Room (B2) West",
        "area_id": "2",
        "map_id": "6",
        "map_name": "Elevator Attic Room (B2)",
        "locations": {
            "TTT Elevator Attic Room (B2) On Parakarry Ledge": CanUseAbilityParakarry(),
        },
        "exits": {
            "TTT Scales Room (B2) East": None,
            "TTT Elevator Attic Room (B2) East": None,
        }
    },
    {
        "region_name": "TTT Elevator Attic Room (B2) East",
        "area_id": "2",
        "map_id": "6",
        "map_name": "Elevator Attic Room (B2)",
        "locations": {
            "TTT Elevator Attic Room (B2) In SuperBlock": (
                CanClimbSteps()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "TTT Elevator Attic Room (B2) East Pipe": HasBoots(),
        }
    },
    {
        "region_name": "TTT Elevator Attic Room (B2) East Pipe",
        "area_id": "2",
        "map_id": "6",
        "map_name": "Elevator Attic Room (B2)",
        "exits": {
            "TTT Elevator Attic Room (B2) West Pipe": CanReenterVerticalPipes(),
            "TTT Elevator Attic Room (B2) East": None,
        }
    },
    {
        "region_name": "TTT Elevator Attic Room (B2) West Pipe",
        "area_id": "2",
        "map_id": "6",
        "map_name": "Elevator Attic Room (B2)",
        "exits": {
            "TTT Elevator Attic Room (B2) East Pipe": CanReenterVerticalPipes(),
            "TTT Elevator Attic Room (B2) West": None,
        }
    },
    {
        "region_name": "TTT Second Level Entry (B2) West",
        "area_id": "2",
        "map_id": "7",
        "map_name": "Second Level Entry (B2)",
        "exits": {
            "TTT Warp Zone 2 (B2)": None,
            "TTT Sewer Entrance (B1) Tall Pipe": None,
            "TTT Second Level Entry (B2) East": CanBeatAllBloopers() & CanUseAbilitySushie(),
        }
    },
    {
        "region_name": "TTT Second Level Entry (B2) East",
        "area_id": "2",
        "map_id": "7",
        "map_name": "Second Level Entry (B2)",
        "events": {
            "GF_TIK08_WarpPipe": CanBeatAllBloopers() & CanHitGroundedSwitches(),
        },
        "exits": {
            "TTT Room with Spikes (B2)": None,
            "TTT Second Level Entry (B2) West": CanBeatAllBloopers() & CanUseAbilitySushie(),
            "TTT Second Level Entry (B2) Blue Pipe": Has("GF_TIK08_WarpPipe") & HasBoots(),
        }
    },
    {
        "region_name": "TTT Second Level Entry (B2) Blue Pipe",
        "area_id": "2",
        "map_id": "7",
        "map_name": "Second Level Entry (B2)",
        "exits": {
            "JJ Village Buildings Pipe": CanReenterVerticalPipes(),
            "TTT Second Level Entry (B2) East": None,
        }
    },
    {
        "region_name": "TTT Warp Zone 2 (B2)",
        "area_id": "2",
        "map_id": "8",
        "map_name": "Warp Zone 2 (B2)",
        "events": {
            "GF_TIK09_WarpPipe": CanHitGroundedSwitches(),
        },
        "exits": {
            "TTT Blue Pushblock Room (B2)": None,
            "TTT Second Level Entry (B2) West": None,
            "TTT Warp Zone 2 (B2) Pipe": Has("GF_TIK09_WarpPipe") & HasBoots(),
        }
    },
    {
        "region_name": "TTT Warp Zone 2 (B2) Pipe",
        "area_id": "2",
        "map_id": "8",
        "map_name": "Warp Zone 2 (B2)",
        "exits": {
            "FOR Outside Boo's Mansion Pipe": None,
            "TTT Warp Zone 2 (B2)": None,
        }
    },
    {
        "region_name": "TTT Blue Pushblock Room (B2)",
        "area_id": "2",
        "map_id": "9",
        "map_name": "Blue Pushblock Room (B2)",
        "locations": {
            "TTT Blue Pushblock Room (B2) Hidden Block Left": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
            "TTT Blue Pushblock Room (B2) Hidden Block Center": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
            "TTT Blue Pushblock Room (B2) Hidden Block Right": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
                & CanClimbSteps()
            ),
            "TTT Blue Pushblock Room (B2) In SuperBlock": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Warp Zone 2 (B2)": None,
        }
    },
    {
        "region_name": "TTT Metal Block Room (B3)",
        "area_id": "2",
        "map_id": "10",
        "map_name": "Metal Block Room (B3)",
        "locations": {
            "TTT Metal Block Room (B3) In SuperBlock": (
                HasUltraHammer()
                & CanClimbSteps()
                & CanHitFloatingBlocks()
            ),
        },
        "exits": {
            "TTT Scales Room (B2) Lower Pipe": None,
        }
    },
    {
        "region_name": "TTT Rip Cheato Antechamber (B3)",
        "area_id": "2",
        "map_id": "11",
        "map_name": "Rip Cheato Antechamber (B3)",
        "exits": {
            "TTT Bridge to Shiver City (B2) Pipe": None,
            "TTT Rip Cheato's Home (B3)": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "TTT Rip Cheato's Home (B3)",
        "area_id": "2",
        "map_id": "12",
        "map_name": "Rip Cheato's Home (B3)",
        "locations": {
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 1": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 2": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 3": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 4": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 5": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 6": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 7": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 8": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 9": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 10": None,
            "TTT Rip Cheato's Home (B3) Rip Cheato Offer 11": None,
        },
        "exits": {
            "TT Southern District Odd House Pipe": None,
            "TTT Rip Cheato Antechamber (B3)": CanUseAbilityBombette(),
        }
    },
    {
        "region_name": "TTT Frozen Room (B3) West Pipe",
        "area_id": "2",
        "map_id": "13",
        "map_name": "Frozen Room (B3)",
        "exits": {
            "TTT Pipe to Frozen Room (B2) Pipe": CanReenterVerticalPipes(),
            "TTT Frozen Room (B3)": None,
        }
    },
    {
        "region_name": "TTT Frozen Room (B3)",
        "area_id": "2",
        "map_id": "13",
        "map_name": "Frozen Room (B3)",
        "locations": {
            "TTT Frozen Room (B3) In SuperBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Frozen Room (B3) West Pipe": CanClimbSteps(),
            "TTT Frozen Room (B3) East Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Frozen Room (B3) East Pipe",
        "area_id": "2",
        "map_id": "13",
        "map_name": "Frozen Room (B3)",
        "exits": {
            "SR Shiver City Center Pipe": None,
            "TTT Frozen Room (B3)": None,
        }
    },
    {
        "region_name": "TTT Hall to Blooper 1 (B1)",
        "area_id": "2",
        "map_id": "14",
        "map_name": "Hall to Blooper 1 (B1)",
        "locations": {
            "TTT Hall to Blooper 1 (B1) Hidden Block": CanSeeHiddenBlocks() & CanHitFloatingBlocks(),
            "TTT Hall to Blooper 1 (B1) In MultiCoinBlock": CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Sewer Entrance (B1)": None,
            "TTT Blooper Boss 1 (B1)": None,
        }
    },
    {
        "region_name": "TTT Under the Toad Town Pond",
        "area_id": "2",
        "map_id": "15",
        "map_name": "Under the Toad Town Pond",
        "locations": {
            "TTT Under the Toad Town Pond In SuperBlock": CanClimbSteps() & CanHitFloatingBlocks(),
        },
        "exits": {
            "TT Gate District Island Pipe": None,
        }
    },
    {
        "region_name": "TTT Room with Spikes (B2)",
        "area_id": "2",
        "map_id": "16",
        "map_name": "Room with Spikes (B2)",
        "locations": {
            "TTT Room with Spikes (B2) Yellow Block": HasUltraBoots(),
        },
        "exits": {
            "TTT Second Level Entry (B2) East": None,
            "TTT Bridge to Shiver City (B2) West": None,
            "TTT Room with Spikes (B2) Pipe": HasBoots() & CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "TTT Room with Spikes (B2) Pipe",
        "area_id": "2",
        "map_id": "16",
        "map_name": "Room with Spikes (B2)",
        "exits": {
            "TTT Winding Path (Spiny Room)": CanReenterVerticalPipes(),
            "TTT Room with Spikes (B2)": CanUseAbilityLakilester(),
        }
    },
    {
        "region_name": "TTT Bridge to Shiver City (B2) West",
        "area_id": "2",
        "map_id": "17",
        "map_name": "Bridge to Shiver City (B2)",
        "events": {
            "RF_BuiltCh7Bridge": (
                (HasUltraBoots() & CanSeeHiddenBlocks())
                | HasSuperBoots(
                    options=[OptionFilter(
                        Chapter7BridgeVisible,
                        True
                    )],
                    filtered_resolution=False,
                )
            ),
        },
        "locations": {
            "TTT Bridge to Shiver City (B2) Yellow Block 1": HasSuperBoots(),
            "TTT Bridge to Shiver City (B2) Yellow Block 2": Has("RF_BuiltCh7Bridge") & HasSuperBoots(),
            "TTT Bridge to Shiver City (B2) Yellow Block 3": Has("RF_BuiltCh7Bridge") & HasSuperBoots(),
            "TTT Bridge to Shiver City (B2) Yellow Block 4": Has("RF_BuiltCh7Bridge") & HasSuperBoots(),
            "TTT Bridge to Shiver City (B2) Yellow Block 5": Has("RF_BuiltCh7Bridge") & HasSuperBoots(),
        },
        "exits": {
            "TTT Room with Spikes (B2)": None,
            "TTT Bridge to Shiver City (B2) East Door": CanClimbSteps() & Has("RF_BuiltCh7Bridge"),
            "TTT Bridge to Shiver City (B2) Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Bridge to Shiver City (B2) East Door",
        "area_id": "2",
        "map_id": "17",
        "map_name": "Bridge to Shiver City (B2)",
        "exits": {
            "TTT Pipe to Frozen Room (B2)": None,
            "TTT Bridge to Shiver City (B2) West": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Bridge to Shiver City (B2) Pipe",
        "area_id": "2",
        "map_id": "17",
        "map_name": "Bridge to Shiver City (B2)",
        "exits": {
            "TTT Rip Cheato Antechamber (B3)": CanReenterVerticalPipes(),
            "TTT Bridge to Shiver City (B2) West": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Pipe to Frozen Room (B2)",
        "area_id": "2",
        "map_id": "18",
        "map_name": "Pipe to Frozen Room (B2)",
        "exits": {
            "TTT Bridge to Shiver City (B2) East Door": None,
            "TTT Pipe to Frozen Room (B2) Pipe": CanClimbSteps(),
        }
    },
    {
        "region_name": "TTT Pipe to Frozen Room (B2) Pipe",
        "area_id": "2",
        "map_id": "18",
        "map_name": "Pipe to Frozen Room (B2)",
        "exits": {
            "TTT Frozen Room (B3) West Pipe": CanReenterVerticalPipes(),
            "TTT Pipe to Frozen Room (B2)": None,
        }
    },
    {
        "region_name": "TTT Winding Path (Spiny Room)",
        "area_id": "2",
        "map_id": "19",
        "map_name": "Winding Path (Spiny Room)",
        "locations": {
            "TTT Winding Path (Spiny Room) Hidden Block Center": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
            "TTT Winding Path (Spiny Room) Hidden Block Right": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
            "TTT Winding Path (Spiny Room) Hidden Block Left": (
                CanSeeHiddenBlocks()
                & CanHitFloatingBlocks()
            ),
            "TTT Winding Path (Spiny Room) Yellow Block": CanHitFloatingBlocks(),
        },
        "exits": {
            "TTT Room with Spikes (B2) Pipe": None,
            "TTT Hall to Ultra Boots (B3)": HasSuperHammer(
                options=[OptionFilter(
                    GearShuffleMode,
                    GearShuffleMode.option_Gear_Location_Shuffle,
                    operator="ne",
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "TTT Hall to Ultra Boots (B3)",
        "area_id": "2",
        "map_id": "20",
        "map_name": "Hall to Ultra Boots (B3)",
        "locations": {
            "TTT Hall to Ultra Boots (B3) Hidden Block": CanSeeHiddenBlocks() & HasUltraBoots(),
            "TTT Hall to Ultra Boots (B3) Yellow Block Left": HasUltraBoots(),
            "TTT Hall to Ultra Boots (B3) Yellow Block Right": HasUltraBoots(),
        },
        "exits": {
            "TTT Winding Path (Spiny Room)": None,
            "TTT Ultra Boots Room (B3)": HasUltraHammer(
                options=[OptionFilter(
                    GearShuffleMode,
                    GearShuffleMode.option_Gear_Location_Shuffle,
                    operator="ne",
                )],
                filtered_resolution=True,
            ),
        }
    },
    {
        "region_name": "TTT Ultra Boots Room (B3)",
        "area_id": "2",
        "map_id": "21",
        "map_name": "Ultra Boots Room (B3)",
        "locations": {
            "TTT Ultra Boots Room (B3) In Big Chest": CanHitFloatingBlocks() & CanClimbSteps(),
        },
        "exits": {
            "TTT Hall to Ultra Boots (B3)": None,
        }
    }
]
