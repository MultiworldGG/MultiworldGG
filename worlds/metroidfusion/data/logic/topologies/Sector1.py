from ..Connection import Connection
from ..Requirement import Requirement, PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator1Top
from ..regions.Sector1 import *
from ..regions.Sector2 import Sector2TubeLeft
from ..regions.Sector3 import Sector3TubeRight
from ..regions.Sector6 import Sector6RestrictedZoneElevatorToTourian

# Region Connections
Sector1AfterChargeCoreZone.connections = [
    Connection(Sector1FirstStabilizerZone, [], one_way=True),
    Connection(Sector1ChargeCoreZone, [
        Requirement("", [
            CanDamageAnyGeron(),
            CanDamageStabilizer("",[HasMorph()])
        ],[
            HasMissile(),
            PONRRequirement("PONR - Enter Charge Core Zone", [])
        ])
    ], one_way=True),
]

Sector1Antechamber.connections = [
    Connection(Sector1Hub, [
        HasKeycard2("Enter Antechamber - Bottom Half and Open Door", [
            HasScrewAttack()
        ])
    ], one_way=True),
    Connection(Sector1TubeRight, [
        HasMorph("Secret Tunnel")
    ], one_way=True)
]

Sector1ChargeCoreZone.connections = [
    Connection(Sector1AfterChargeCoreZone, [
        CanDamageCoreX("Need to Kill Beam Core X", [CanDamageGadora()])
    ], one_way=True)
]

Sector1FirstStabilizerZone.connections = [
    Connection(Sector1SecondStabilizerZone, []),
    Connection(Sector1AfterChargeCoreZone, [
        HasWaveBeam("Backwards Travel")
    ], one_way=True),
]

Sector1FourthStabilizerZone.connections = [
    Connection(Sector1ChargeCoreZone, [
        HasMorph("Enter Charge Core Zone", [
            CanDamageCoreX("License to Kill"),
            PONRRequirement("PONR - Enter Charge Core Zone", items_needed={"Charge Beam"})
        ])
    ], one_way=True),
]

Sector1Hub.connections = [
    VariableConnection(SectorHubElevator1Top, []),
    Connection(Sector1Antechamber, [
        HasKeycard2("Enter Antechamber - Top Half", [
            HasSpaceJump("Fly"),
            CanDoAdvancedWallJump("Jump Good", [
                HasHiJump()
            ])
        ], [
            HasScrewAttack()
        ])
    ]),
    Connection(Sector1TubeLeft, [
        HasKeycard1("Can Approach West Tube from Top Door", [
            HasMorph()
        ], [
            HasScrewAttack()
        ])
    ]),
    Connection(Sector1FirstStabilizerZone, [
        CanDamageSmallGeron("Atmospheric Stabilizer NW - Vanilla Kill"),
        CanDamageAnyGeron("Atmospheric Stabilizer NW - Alternate Kill"),
        CanDoAdvancedShinespark("Atmospheric Stabilizer NW - Shinespark Kill")
    ]),
    Connection(Sector1SecondStabilizerZone, [
        CanLavaDive("Cut Through Lava Pool", items_needed={"Level 1 Keycard", "Level 2 Keycard"})
    ]),
]

Sector1SecondStabilizerZone.connections = [
    Connection(Sector1ThirdStabilizerZone, [
        CanDamageStabilizer(),
        CanDamageAnyGeron()
    ])
]

Sector1ThirdStabilizerZone.connections = [
    Connection(Sector1FourthStabilizerZone, [
        CanDamageStabilizer(),
        CanDamageAnyGeron()
    ]),
    Connection(Sector1TourianExit, [
        HasMorph("Enter Tourian Exit from Stabilizers", [
            PONRRequirement("PONR - Enter Tourian Exit from Stabilizers", [
                CanFreezeEnemies("Use Rippers as platforms")
            ]),
            HasSpaceJump("Fly")
        ], [
            HasScrewAttack()
        ], energy_tanks_needed=level_4_e_tanks),
    ], one_way=True)
]

Sector1TourianExit.connections = [
    Connection(Sector1ThirdStabilizerZone, [
        Requirement("Break Out of Tourian Exit toward Stabilizers", [
            # Must defeat SW or SE Stabilizers
            CanDamageStabilizer(),
            CanDamageAnyGeron()
        ],  items_needed={"Space Jump", "Wave Beam", "Morph Ball"},
        energy_tanks_needed=level_4_e_tanks),
    ], one_way=True),
    Connection(Sector1TourianHub, [
        Requirement("Break Into Tourian from Exit", [
            HasSpaceJump("Fly"),
            CanDoSimpleWallJump()
        ], [
            HasWaveBeam("Can Open Shutter Gate Backwards"),
            PONRRequirement("PONR - Break Into Tourian from Exit")
        ], items_needed={"Missile Data", "Screw Attack", "Morph Ball"},
        energy_tanks_needed=level_3_e_tanks),
    ], one_way=True)
]

Sector1TourianHub.connections = [
    Connection(Sector1TourianExit, [
        HasMissile("Open and Enter Tunnel to Tourian Exit", [
            HasSpaceJump(),
            CanDoAdvancedWallJump()
        ], items_needed={"Morph Ball", "Screw Attack", "Wave Beam"},
        energy_tanks_needed=level_4_e_tanks),
    ]),
    Connection(Sector1TourianHubElevatorTop, [
        Requirement("Traverse Tourian Hub to/from Tourian Elevator", [
            HasSpaceJump(),
            CanDoSimpleWallJump()
        ], [
            # Pinnacle of Movement and Avoidance
            CanDoExpertCombat(),
            CanDoAdvancedCombat(None, [
                # Gerubus HP is between 41 and 45
                CanDamageToughEnemy("Kill Pirate and Kill/Stun Gerubus", enemy_hp=(90 + (2 * 45)))
            ], [
                HasIceBeam("Freeze Ripper")
            ]),
            HasMissile("Trickless Combat", [
                CanFreezeEnemies(missile_ammo_needed=10),
                HasScrewAttack("Kill Everything")
            ])
        ], energy_tanks_needed=level_4_e_tanks)
    ])
]

Sector1TourianHubElevatorTop.connections = [
    VariableConnection(Sector6RestrictedZoneElevatorToTourian, []),
    Connection(Sector1TourianHub, [
        PONRRequirement("PONR - Leaving Tourian Elevator",
                        energy_tanks_needed=level_4_e_tanks),
    ], one_way=True)
]

Sector1TubeLeft.connections = [
    VariableConnection(Sector3TubeRight, [])
]

Sector1TubeRight.connections = [
    Connection(Sector1Antechamber, [
        CanBallJump("Jump Into Tunnel")
    ]),
    VariableConnection(Sector2TubeLeft, [])
]

# Item Locations
Sector1AfterChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Crab Rave", False, [
        HasMorph("Enter Crab Rave", [
            HasMissile()
        ])
    ])
]

Sector1Antechamber.locations = [
    FusionLocation("Sector 1 (SRX) -- Antechamber", False, [])
]

Sector1ChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Core X", True, [
        CanDamageCoreX()
    ]),
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Upper Item", False, [
        HasSpeedBooster("Obtain Charge Core Upper Item", [
            CanDamageCoreX("Kill the Core X First"),
            PONRRequirement("PONR - Obtain Charge Core Upper Item")
        ])
    ]),
    FusionLocation("Sector 1 (SRX) -- Watering Hole", False, [
        CanBallJump("Grab Watering Hole Item", [
            CanSpeedBoosterUnderwater(),
            # When new trick level is ready to unleash in the YAML
            # Video proof: https://www.youtube.com/watch?v=7CrmoeqlIUk
            CanDoExpertShinespark("Watering Hole - The 7 Frame Window", [HasChargeBeam("Pseudo-Screw the Crab")])
        ], [
            CanDoAdvancedShinespark("Avoid the Crab"),
            CanDoBeginnerShinespark("Alternate Kill the Crab", [
                HasWaveBeam(),
                CanDo10MissileDamage(),
                CanPowerBomb()
            ]),
            Requirement("Trickless - Kill the Crab", [
                HasScrewAttack(),
                HasChargeBeam(),
                HasPlasmaBeam()
            ])
        ])
    ])
]

Sector1FirstStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Atmospheric Stabilizer Northeast", False, [
        Requirement("Collect Atmospheric Stabilizer NE Item", [
            PONRRequirement("PONR - Collect Atmospheric Stabilizer NE Item"),
            CanDamageStabilizer("Atmospheric Stabilizer NE - Vanilla"),
            CanDamageAnyGeron("Atmospheric Stabilizer NE - Alternate"),
            # Video proof: https://www.youtube.com/watch?v=I9YH_s989sQ
            CanDoExpertShinespark("Atmospheric Stabilizer NE - Shinespark"),
        ])
    ]),
    FusionLocation("Sector 1 (SRX) -- Hornoad Hole", False, [
        HasMorph("Secret Tunnel")
    ]),
    FusionLocation("Sector 1 (SRX) -- Wall Jump Tutorial", False, [
        HasMorph("Enter Wall Jump Tutorial", [
            HasWallJump(),
            HasSpaceJump()
        ]),
        CanBallJump("Enter Wall Jump Tutorial - Skill Issue", [
            HasWallJump(),
            HasSpaceJump()
        ])
    ])
]

Sector1FourthStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Stabilizer Storage", False, [
        CanDamageStabilizer("Can Kill Atmospheric Stabilizer SE - Vanilla"),
        CanDamageAnyGeron("Can Kill Atmospheric Stabilizer SE - Alternate", [
            HasHiJump(),
            CanDoSimpleWallJump(),
            Requirement(hard_items_needed={"Power Bomb Data"})
        ])
    ])
]

Sector1SecondStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Lower Item", False, [
        CanLavaDive("Lava Bath - Enter Tunnel", [
            HasMorph()
        ])
    ]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Left Item", False, [
        HasSpaceJump("Lava Lake Far Shelf - Fly"),
        CanDoBeginnerShinespark("Lava Lake Far Shelf - Shinespark")
    ]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Right Item", False, []),
]

Sector1TourianHub.locations = [
    FusionLocation("Sector 1 (SRX) -- Animorphs Cache", False, [
        CanDamageToughEnemy("Kill the Yard", [
            # Kill the Gerubus
            CanDefeatGerubus()
        ], [
            # Kill the Golden Pirate
            CanDamageToughEnemy("Kill the Golden Pirate", enemy_hp=135, immunities={"Beam", "Power Bomb"})
        ], [
            PONRRequirement("PONR - Enter and Collect Animorphs"),
            HasSpaceJump("Fly out of Animorphs Cache"),
            CanDoSimpleWallJump("Wall Jump out of Animorphs Cache", [
                HasHiJump()
            ])
        ], enemy_hp=60, behind_wall=True)
    ]),
    FusionLocation("Sector 1 (SRX) -- Neo-Ridley Arena", True, [
        Requirement("Enter Neo-Ridley Arena", [
            # Destroy Bomb Wall
            CanBomb(),
            CanPowerBomb()
        ], [
            # Can Kill Genesis under floor
            HasWaveBeam(),
            CanPowerBomb(power_bomb_ammo_needed=2)
        ], [
            # Can Kill Golden Pirates
            CanDamageToughEnemy("Kill Golden Pirates", enemy_hp=(135 * 2), immunities={"Beam", "Power Bomb"})
        ], [
            # Do Ridley Fight
            CanFightLateGameBoss("Ridley Trickless", energy_tanks_needed=level_4_e_tanks, boss_hp=4500,
                                 immunities={"Beam", "Bomb", "Power Bomb", "Screw Attack"}),
            CanFightLateGameBossOnAdvanced("Ridley On Advanced", [
                HasPlasmaBeam()
            ], boss_hp=4500, immunities={"Beam", "Bomb", "Power Bomb", "Screw Attack"}),
            CanFightBossOnExpert("Ridley On Expert", boss_hp=4500,
                                 immunities={"Beam", "Bomb", "Power Bomb", "Screw Attack"})
        ], [
            HasSpaceJump("Can Leave Neo-Ridley Arena"),
            PONRRequirement("PONR - Neo-Ridley Arena")
        ])
    ]),
    FusionLocation("Sector 1 (SRX) -- Ripper Maze", False, [
        HasMorph("Collect Ripper Maze Item", [
            CanBallJump("Can Leave after Ripper Maze Item"),
            PONRRequirement("PONR - Ripper Maze Item")
        ], [
            # Mobility Requirements
            HasSpaceJump(),
            CanDoSimpleWallJump()
        ], [
            # Dealing with Rippers
            CanFreezeEnemies(missile_ammo_needed=5),
            HasScrewAttack()
        ], [
            CanUseDiffusionMissile(),
            # Can be done without Diffusion. Awaiting trick identity
            # HasMissile(missile_ammo_needed=3)
        ])
    ])
]
