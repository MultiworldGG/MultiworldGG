from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator5Top
from ..regions.Sector3 import Sector3TubeLeft
from ..regions.Sector4 import Sector4UpperWaterZone
from ..regions.Sector5 import *
from ..regions.Sector6 import Sector6TubeRight

Sector5Hub.connections = [
    VariableConnection(SectorHubElevator5Top, []),
    Connection(Sector5MagicBox, [
        HasKeycard3()
    ]),
    Connection(Sector5TopLeftBigRoom, [
        Requirement("Sector 5 Entrance <-> Training Grounds by Entrance Lobby", [
            HasKeycard3("Through Gerubus Gully", [
                CanJumpHigh(),
                CanDoAdvancedWallJump()
            ]),
            HasMorph("Vanilla Access Tunnel", [
                HasMissile(missile_ammo_needed=2)
            ])
        ])
    ]),
    Connection(Sector5FrozenHub, [
        HasVaria("Sector 5 Entrance <-> Arctic Containment", [
            HasKeycard3("Through Gerubus Gully"),
            HasMorph("Vanilla Access Tunnel", [
                HasMissile(missile_ammo_needed=2)
            ])
        ])
    ])
]

Sector5TubeLeft.connections = [
    VariableConnection(Sector6TubeRight, []),
    Connection(Sector5MagicBox, [
        HasScrewAttack()
    ])
]

Sector5TubeRight.connections = [
    VariableConnection(Sector3TubeLeft, []),
    Connection(Sector5BeforeNightmareHub, [], one_way=True)
]

Sector5TopLeftBigRoom.connections = [
    Connection(Sector5FrozenHub, [
        HasVaria()
    ], one_way=True)
]

Sector5FrozenHub.connections = [
    Connection(Sector5DataRoom, [
        HasVaria("Top of Arctic Containment -> Data Room", [
            HasKeycard3()
        ])
    ], one_way=True),
    Connection(Sector5BeforeNightmareHub, [
        HasVaria("Top of Arctic Containment <-> Crow's Nest", [
            HasKeycard3()
        ])
    ]),
    Connection(Sector5SecurityZone, [
        HasVaria("Top of Arctic Containment -> Security", [
            HasSpeedBooster("Go through Cellar", [
                CanBomb(),
                CanPowerBomb(power_bomb_ammo_needed=2)
            ], [
                CanDamageToughEnemy()
            ], [
                # Return from Cellar Save Room?
                HasSpaceJump(),
                HasKeycard3(),
                PONRRequirement("PONR - Enter Level 3 Security via Vanilla Route")
            ]),
            HasWaveBeam("Go backwards through Zeela Checkpoint", [
                HasKeycard3()
            ], [
                CanDamageToughEnemy("Kill Zeela", enemy_hp=(8 * 12)),
                # Use hidden ladder path
                CanBomb(),
                CanPowerBomb()
            ]),
            #future CanDoExpertShinespark("Go backwards through Arctic Underside", [HasKeycard3()])
        ], energy_tanks_needed=level_3_e_tanks)
    ], one_way=True),
    Connection(Sector5TopLeftBigRoom, [
        HasVaria("Arctic Containment <-> Training Grounds by Entrance Lobby", [
            CanJumpHigh(),
            CanDoAdvancedWallJump()
        ])
    ])
]

Sector5SecurityZone.connections = [
    Connection(Sector5DataRoom, [
        HasVaria("Security Room <-> Data Room via Frozen Tower", [
            HasKeycard3()
        ], [
            HasSpaceJump("Climb Frozen Tower"),
            CanDoAdvancedWallJump("Climb above E-Tank Mimic via Frozen Ripper", [
                CanFreezeEnemies()
            ], [
                HasHiJump()
            ], energy_tanks_needed=level_3_e_tanks)
        ])
        #ReverseIceLOLRequirement
    ]),
    Connection(Sector5FrozenHub, [
        HasVaria("Security Room -> Arctic Containment", [
            HasKeycard3(),
            HasSpaceJump("Climb Cellar", [
                CanBomb(),
                CanPowerBomb()
            ])
            # RIP Kago Speedway
        ])
    ], one_way=True)
]

Sector5DataRoom.connections = [
    Connection(Sector5FrozenHub, [
        HasKeycard3("Go backwards from Data Room", [
            HasWaveBeam()
        ])
    ]),
    Connection(Sector5SecurityZone, [
        HasKeycard3()
    ], one_way=True)
]

Sector5BeforeNightmareHub.connections = [
    Connection(Sector5TubeRight, [
        CanJumpHigh(),
        CanDoSimpleWallJump()
    ]),
    Connection(Sector5NightmareHub, [
        PONRRequirement("PONR - Drop down Flooded Tower", [
            CanDamageToughEnemy("Kill Pirates", enemy_hp=(90 * 5), immunities={"Beam", "Bomb", "Screw Attack"}),
            CanScrewAttackUnderwater(),
            CanDoExpertCombat()
        ], energy_tanks_needed=level_3_e_tanks)
    ], one_way=True)
]

Sector5NightmareHub.connections = [
    Connection(Sector5BeforeNightmareHub, [
        CanScrewAttackUnderwater("Climb Flooded Tower", [
            HasSpaceJump(),
            CanDoBeginnerShinespark("Shinespark up Flooded Tower", [
                CanDoAdvancedWallJump()
            ]),
        ], energy_tanks_needed=level_3_e_tanks)
    ]),
    Connection(Sector4UpperWaterZone, [
        CanSpeedBoosterUnderwater()
    ]),
    Connection(Sector5NightmareZoneUpper, [
        Requirement("Zebesian Waters <-> Upper Half of Nightmare Hub", [
            # Combat
            CanDamageToughEnemy("Kill Pirates", enemy_hp=(90 * 5), immunities={"Beam", "Bomb", "Screw Attack"}),
            CanScrewAttackUnderwater(),
            CanDoExpertCombat()
        ], [
            # Climb from Nightmare Hub Lower Half to Upper Half
            CanJumpHigh(),
            CanDoBeginnerShinespark(None, [
                CanSpeedBoosterUnderwater(),
            ]),
        ], energy_tanks_needed=level_3_e_tanks)
    ])
]

Sector5NightmareZoneUpper.connections = [
    Connection(Sector5NightmareHub, [
        PONRRequirement("PONR - Nightmare Hub Upper Half -> Zebesian Waters", [
            # Combat
            CanDamageToughEnemy("Kill Pirates", enemy_hp=(90 * 5), immunities={"Beam", "Bomb", "Screw Attack"}),
            CanScrewAttackUnderwater(),
            CanDoExpertCombat()
        ], energy_tanks_needed=level_3_e_tanks)
    ], one_way=True),
    Connection(Sector5NightmareZoneArena, [
        CanDamageGadora("Enter Nightmare Arena via Nightmare Nook", [
            HasMorph()
        ], [
            CanJumpHigh(),
            CanDoSimpleWallJump()
        ], [
            CanFightNightmare()
        ])
    ], one_way=True)
]

Sector5NightmareZoneArena.connections = [
    Connection(Sector5NightmareHub, [
        CanSpeedBoosterUnderwater("Return from Nightmare Arena", [
            CanFightNightmare()
        ])
    ])
]

Sector5Hub.locations = [
    FusionLocation("Sector 5 (ARC) -- Gerubus Gully", False, [
        HasKeycard3("Can Obtain Gerubus Gully Item", [
            HasMorph()
        ], [
            # Break the bomb block
            CanDoBeginnerShinespark(),
            HasScrewAttack(),
            HasHiJump("Spring Ball and Bomb", [
                CanBomb()
            ]),
            CanPowerBomb()
        ], [
            # Get out of the hole
            CanBomb(),
            CanPowerBomb(),
            PONRRequirement("PONR - Gerubus Gully Item")
        ])
    ]),
]

Sector5MagicBox.locations = [
    FusionLocation("Sector 5 (ARC) -- Magic Box", False, [])
]

Sector5TopLeftBigRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Left Item", False, [
        HasSpeedBooster("Can Obtain Training Aerie Left Item", [
            CanGetToTrainingAerie()
        ])
    ]),
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Right Item", False, [
        CanGetToTrainingAerie()
    ])
]

Sector5FrozenHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Ripper Road", False, [
        CanBallJump("Can Obtain Ripper Road Item", [
            CanFreezeEnemies("Can Freeze The Rippers",[
                Requirement("Kill Geron and Break Bomb Block",[
                    CanDamageLargeGeron(),
                    CanDamageAnyGeron(),
                ],[
                    CanBomb(),
                    CanPowerBomb(),
                ])
            ], missile_ammo_needed=6)
        ])
    ])
]

Sector5BeforeNightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Crow's Nest", False, [
        HasMorph("Can Obtain Crow's Nest Item", [
            # Break bomb blocks and enter
            Requirement("Enter Crow's Nest - Normal", [
                CanPowerBomb(power_bomb_ammo_needed=2),
                HasScrewAttack()
            ], [
                HasSpaceJump(),
                CanDoAdvancedWallJump(None, [
                    HasHiJump()
                ])
            ]),
            CanDoBeginnerShinespark("Enter Crow's Nest - Shinespark", [
                CanDestroyBombBlocks(),
                PONRRequirement("PONR - Enter Crow's Nest - Shinespark")
            ])
        ], [
            # Combat
            CanDamageToughEnemy("Kill Pirates", enemy_hp=(90 * 3), immunities={"Beam", "Bomb"}),
            CanDoExpertCombat()
        ], [
            # Climb to gates
            CanJumpHigh(),
            CanDoSimpleWallJump()
        ], energy_tanks_needed=level_3_e_tanks)
    ])
]

Sector5DataRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Data Room", True, [
        HasVaria()
    ])
]

Sector5SecurityZone.locations = [
    FusionLocation("Sector 5 (ARC) -- E-Tank Mimic Den", False, [
        HasKeycard3("Can Obtain E-Tank Mimic Den", [
            HasVaria()
        ], [
            # Climb Frozen Tower to Mimic Den Door
            HasSpaceJump(),
            CanFreezeEnemies(missile_ammo_needed=2)
        ], [
            # Deal with the Mimic
            CanDo10MissileDamage(),
            CanDoAdvancedCombat()
        ], [
            # Break the bomb block
            CanDestroyBombBlocks()
        ], [
            # Enter and Leave the hole
            CanBallJump(),
            PONRRequirement("PONR - E-Tank Mimic Den Item", [HasMorph()])
        ])
    ]),
    FusionLocation("Sector 5 (ARC) -- Level 3 Security Room", True, [
        HasVaria()
    ]),
    FusionLocation("Sector 5 (ARC) -- Ripper's Treasure", False, [
        HasVaria("Can Obtain Ripper's Treasure Item", [
            CanPowerBomb()
        ], [
            HasSpaceJump(),
            CanFreezeEnemies(None, [
                HasHiJump(),
                CanDoSimpleWallJump()
            ])
        ])
    ]),
    FusionLocation("Sector 5 (ARC) -- Security Shaft East", False, [
        HasVaria("Can Obtain Security Shaft East Item", [
            CanPowerBomb()
        ])
    ]),
    FusionLocation("Sector 5 (ARC) -- Transmutation Trial", False, [
        HasKeycard3("Can Obtain Transmutation Trial Item", [
            HasVaria()
        ], [
            CanBallJump()
        ], [
            HasSpaceJump(),
            CanFreezeEnemies(None, [
                HasHiJump(),
                CanDoSimpleWallJump()
            ], missile_ammo_needed=6)
        ])
    ])
]

Sector5NightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Flooded Airlock", False, [
        CanSpeedBoosterUnderwater()
    ]),
    FusionLocation("Sector 5 (ARC) -- Mini-Fridge", False, [
        HasVaria("Can Obtain Mini-Fridge Item", [
            HasMorph()
        ], [
            HasMissile(missile_ammo_needed=1)
        ], [
            CanFreezeEnemies(missile_ammo_needed=8),
            CanDoBeginnerShinespark(),
            CanJumpHighUnderwater(None, hard_items_needed={"Space Jump"}),
            CanDoExpertCombat("Shoot Missile Block and Grab Ledge in one motion during PONR drop", [
                PONRRequirement("PONR - Mini-Fridge")
            ])
        ], energy_tanks_needed=level_3_e_tanks)
    ])
]

Sector5NightmareZoneUpper.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Hub", False, [
        CanBallJump("Can Obtain Nightmare Hub Item", [
            CanPowerBomb(),
            #future CanDoMidairMorph(None, hard_items_needed={"Bomb Data"})
        ])
    ]),
    FusionLocation("Sector 5 (ARC) -- Ruined Break Room", False, [
        CanPowerBomb()
    ]),
    FusionLocation("Sector 5 (ARC) -- Nightmare Nook", False, [
        CanDamageGadora("Can Obtain Nightmare Nook Item", [
            # Break bomb blocks chain
            CanBomb(),
            CanPowerBomb()
        ], [
            # Get in tunnel
            CanBallJump(),
            #future CanDoMidairMorph()
        ], [
            CanFightNightmare(),
            #future CanDoCrumbleJump("Escape Nightmare Nook Tunnel", [HasHiJump()])
        ])
    ])
]

Sector5NightmareZoneArena.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Arena", True, [
        CanFightNightmare()
    ])
]
