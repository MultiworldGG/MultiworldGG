from ..Connection import Connection
from ..Requirement import Requirement, PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator2Top
from ..regions.Sector1 import Sector1TubeRight
from ..regions.Sector2 import *
from ..regions.Sector4 import Sector4TubeLeft

# Region Connections
Sector2Hub.connections = [
    VariableConnection(SectorHubElevator2Top, []),
    Connection(Sector2TubeLeft, [
        HasScrewAttack()
    ]),
    Connection(Sector2TubeRight, [
        HasScrewAttack()
    ]),
    Connection(Sector2LeftSide, [
        HasMorph("Traverse from Data Room to Zig-Zag-Zone", [
            CanDestroyBombBlocks()
        ], [
            CanBallJump(),
            PONRRequirement("PONR - To Zig-Zag-Zone")
        ])
    ], one_way=True),
    Connection(Sector2ZazabiZoneUpper, [
        CanBomb(),
        CanPowerBomb(power_bomb_ammo_needed=2)
    ]),
    Connection(Sector2NettoriZone, [
        HasMorph("Can Enter Hub Power Bomb Tunnel", [
            CanPowerBomb()
        ], [
            CanJumpHigh(),
            CanDoSimpleWallJump()
        ])
    ])
]

Sector2LeftSide.connections = [
    Connection(Sector2Hub, [
        CanBallJump("Maintenance Wing -> Data Courtyard", [
            CanBomb(None, [HasScrewAttack()]),
            CanPowerBomb(power_bomb_ammo_needed=4)
        ], [
            HasSpaceJump(),
            CanDoAdvancedWallJump(None, [
                HasHiJump()
            ])
        ])
    ], one_way=True),
    Connection(Sector2ZazabiZone, [
        Requirement("", [
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=4)
        ],[
            CanJumpHigh(),
            PONRRequirement(),
        ])
    ], one_way=True)
]

Sector2TubeLeft.connections = [
    VariableConnection(Sector1TubeRight, [])
]

Sector2TubeRight.connections = [
    VariableConnection(Sector4TubeLeft, [])
]

Sector2ZazabiZone.connections = [
    Connection(Sector2LeftSide, [
        Requirement("Climb Cultivation Station to Zig-Zag-Zone", [
            CanBomb("Spring Ball Bomb", [HasHiJump()]),
            CanPowerBomb(),
            HasScrewAttack()
        ], [
            HasSpaceJump(),
            CanDoSimpleWallJump(None, [
                HasHiJump()
            ]),
            CanDoAdvancedWallJump()
        ], [
            # Required if coming from Cathedral
            CanFreezeEnemies(),
            CanJumpHigh()
        ], [
            PONRRequirement("PONR - To Zig-Zag-Zone"),
            CanBallJump()
        ])
    ], one_way=True),
    Connection(Sector2NettoriZone, [
        HasSpaceJump()
    ]),
    Connection(Sector2ZazabiZoneUpper, [
        Requirement("Climb Cathedral", [
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=2)
        ], [
            CanJumpHigh()
        ])
    ]),
]

Sector2ZazabiZoneUpper.connections = [
    Connection(Sector2ZazabiZone, [
        Requirement("Drop Down Cathedral",[
            CanBomb(),
            CanPowerBomb()
        ],[
            CanJumpHigh(),
            PONRRequirement("PONR - Drop Down Cathedral")
        ])
    ], one_way=True)
]

# Item Locations
Sector2Hub.locations = [
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Lower Item", False, [
        CanCollectCrumbleCity()
    ]),
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Upper Item", False, [
        CanCollectCrumbleCity()
    ]),
    FusionLocation("Sector 2 (TRO) -- Data Courtyard", False, [
        CanBomb(),
        CanPowerBomb()
    ]),
    FusionLocation("Sector 2 (TRO) -- Data Room", True, [
        HasKeycard1()
    ]),
    FusionLocation("Sector 2 (TRO) -- Kago Room", False, [
        CanJumpHigh(),
        HasScrewAttack(),
        CanFreezeEnemies(missile_ammo_needed=3),
        CanDoBeginnerShinespark()
    ]),
    FusionLocation("Sector 2 (TRO) -- Level 1 Security Room", True, [
        Requirement("Use the Security Terminal", [
            HasSpaceJump("Fly"),
            HasKeycard1("Open the Door"),
            PONRRequirement("PONR - Level 1 Security Room")
        ])
    ]),
    FusionLocation("Sector 2 (TRO) -- Lobby Cache", False, [
        HasKeycard1("Can Collect Lobby Cache", [
            # These bomb blocks don't return once broken, even on room reload.
            CanBomb(),
            CanPowerBomb()
        ])
    ]),
]

Sector2LeftSide.locations = [
    FusionLocation("Sector 2 (TRO) -- Zig-Zag-Zone", False, [
        HasMorph("Can Obtain Zig-Zag-Zone Item", [
            CanActivatePillar(power_bomb_ammo_needed=2),
            CanJumpHigh()
        ])
    ])
]

Sector2NettoriZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Nettori Arena", True, [
        CanFightMidGameBoss(boss_hp=2000, immunities={"Beam", "Bomb", "Screw Attack"}),
        CanFightMidGameBossOnAdvanced(boss_hp=2000, immunities={"Beam", "Bomb", "Screw Attack"})
    ]),
    FusionLocation("Sector 2 (TRO) -- Overgrown Cache", False, [
        HasMorph()
    ]),
    FusionLocation("Sector 2 (TRO) -- Puyo Palace", False, [
        Requirement("Obtain Puyo Palace Item from Above", [
            PONRRequirement("PONR - Puyo Palace Item from Above"),
            HasSpaceJump("Obtain Puyo Palace Item and Return")
        ])
    ])
]

Sector2ZazabiZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Cultivation Station", False, [
        Requirement("Can Obtain Cultivation Station Item", [
            # Need to break a chain of bomb blocks. Satisfies CanActivatePillar
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=3)
        ], [
            # Required when coming from Cathedral
            CanFreezeEnemies(),
            CanJumpHigh()
        ])
    ]),
    FusionLocation("Sector 2 (TRO) -- Oasis", False, [
        CanJumpHigh(),
        CanFreezeEnemies(missile_ammo_needed=5)
    ]),
    FusionLocation("Sector 2 (TRO) -- Oasis Storage", False, [
        HasMorph("Can Obtain Oasis Storage Item", [
            CanPowerBomb("Power Bomb the Block and Use the Pillar"),
            CanBomb("Use the Pillar to Bomb the Block", [
                HasHiJump(),
                # Good movement from pillar can be used to barely be able to bomb the block.
                #future CanDoMidairMorph()
            ]),
            HasGravity("Move Underwater", [
                CanBomb("Bomb Jump from Pillar"),
                HasWaveBeam("Screw Attack from the Pillar", [
                    HasScrewAttack()
                ]),
                CanJumpHigh("Screw Attack from the Ground", [
                    HasScrewAttack()
                ])
            ])
        ], [
            # Getting into the room from Oasis
            CanActivatePillar(),
            CanFreezeEnemies("Freeze the Fish")
        ])
    ]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Lower Item", False, [
        CanDestroyBombBlocks("Grab Ripper Tower Items and Leave", [
            CanObtainRipperTower()
        ], [
            HasMorph(),
            PONRRequirement("PONR - Ripper Tower Lower Item")
        ]),
    ]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Upper Item", False, [
        CanDestroyBombBlocks("Grab Ripper Tower Items and Leave", [
            CanObtainRipperTower()
        ], [
            HasMorph(),
            PONRRequirement("PONR - Ripper Tower Upper Item")
        ]),
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena", True, [
        CanFightZazabi()
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena Access", False, []),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Lower Item", False, [
        CanFightZazabi("Kill Zazabi and Enter Zazabi Speedway", [
            HasSpaceJump()
        ], [
            HasScrewAttack()
        ], [
            HasSpeedBooster()
        ]),
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Upper Item", False, [
        CanFightZazabi("Kill Zazabi and Enter Zazabi Speedway", [
            HasSpaceJump()
        ], [
            HasScrewAttack()
        ], [
            HasSpeedBooster()
        ]),
    ])
]

Sector2ZazabiZoneUpper.locations = [
    FusionLocation("Sector 2 (TRO) -- Dessgeega Dorm", False, [
        PONRRequirement("PONR - Dessgeega Dorm", [
            HasScrewAttack()
        ], [
            HasMorph()
        ]),
        CanBomb(),
        CanPowerBomb(power_bomb_ammo_needed=2)
    ])
]
