from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..Requirements import level_3_e_tanks
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator4Top
from ..regions.Sector2 import Sector2TubeRight
from ..regions.Sector4 import *
from ..regions.Sector5 import Sector5NightmareHub
from ..regions.Sector6 import Sector6TubeLeft

Sector4Hub.connections = [
    VariableConnection(SectorHubElevator4Top, []),
    Connection(Sector4UpperZone, [
        Requirement("Get to Room Center of Reservoir East", [
            # Entry
            CanBomb(),
            CanPowerBomb()
        ], [
            # Leaving
            CanActivatePumpControl(),
            HasSpaceJump(),
            PONRRequirement("PONR - Entrance Lobby -> Reservoir East Room Center")
        ], energy_tanks_needed=level_1_e_tanks)
    ], one_way=True),
    Connection(Sector4DataZone, [
        HasMorph("Cross Powamp Playhouse",
                 [
                     CanActivatePumpControl(),
                     HasGravity("Damage Run - Powamp Playhouse",
                                energy_tanks_needed=level_1_e_tanks),
                     HasVaria("Damage Run - Powamp Playhouse Water Physics",
                              energy_tanks_needed=level_2_e_tanks)
                 ], [
                     CanUseDiffusionMissile(),
                     HasIceBeam(None, [
                         HasWaveBeam()
                     ])
                 ])
    ]),
    Connection(Sector4RightWaterZone, [
        CanCrossSector4DrainPipeTunnel("Enter Sector 4 Right Water Zone Save through Drain Pipe", [
            CanSpeedBoosterUnderwater(),
            CanScrewAttackUnderwater()
        ])
    ]),
    Connection(Sector4RightWaterZoneSave, [
        CanCrossSector4DrainPipeTunnel("Enter Sector 4 Right Water Zone Save through Drain Pipe", [
            HasGravity(None, [
                HasBombData()
            ]),
            HasHiJump()
        ])
    ]),
]


Sector4TubeRight.connections = [
    VariableConnection(Sector6TubeLeft, [
        HasScrewAttack()
    ]),
    Connection(Sector4RightDataZone, [
        HasMissile(None, [
            CanBallJump(),
            PONRRequirement("PONR - Enter Sector 4 from Upper Tube", [
                HasMorph()
            ])
        ], missile_ammo_needed=2)
    ], one_way=True),
]

Sector4TubeLeft.connections = [
    VariableConnection(Sector2TubeRight, []),
    Connection(Sector4RightWaterZone, [
        CanScrewAttackUnderwater("Exit from Sector 4 Lower Tube", [
            HasSpaceJump(),
            CanDoSimpleWallJump()
        ])
    ])
]

Sector4UpperZone.connections = [
    Connection(Sector4Hub, [
        Requirement("Get to Entrance Lobby", [
            HasSpaceJump("Fly to Bomb Block Chain", [
                CanBomb(),
                CanPowerBomb()
            ]),
            PONRRequirement("PONR - Leave Upper Sector 4 toward Entrance Lobby", [
                CanSpeedBoosterUnderwater("Damage Run - Leave Upper Sector 4 toward Entrance Lobby",
                                          energy_tanks_needed=level_2_e_tanks),
                CanActivatePumpControl("Water Drained - Leave Upper Sector 4 toward Entrance Lobby", [
                    HasSpeedBooster()
                ])
            ])
        ])
    ], one_way=True),
    Connection(Sector4BeforePumpControlZone, [
        Requirement("Cross Sector 4 Reservoir West to Pump Control", [
            CanBomb(),
            CanPowerBomb(power_bomb_ammo_needed=3),
            CanJumpHighUnderwater("Damage Run - Reservoir West with Jump",
                                  energy_tanks_needed=level_2_e_tanks),
            CanSpeedBoosterUnderwater("Damage Run - Reservoir West with Speed", [
                CanDoBeginnerShinespark()
            ], energy_tanks_needed=level_2_e_tanks)
        ])
    ], one_way=True),
    Connection(Sector4ReservoirVault, [
        HasSpaceJump(),
        CanDoSimpleWallJump()
    ])
]

Sector4BeforePumpControlZone.connections = [
    Connection(Sector4PumpControl, [
        HasKeycard1()
    ], one_way=True),
    Connection(Sector4UpperWaterZone, [
        HasKeycard4("Get to Cargo Hold from Pump Control Access", [
            # Get through door
            CanActivatePumpControl("After Water is Drained"),
            HasGravity("Damage Run - Enter Cargo Hold",
                       energy_tanks_needed=level_1_e_tanks),
            HasVaria("Damage Run - Enter Cargo Hold - Water Physics",
                     energy_tanks_needed=level_2_e_tanks),
        ], [
            # Can come back to the door after entry?
            HasGravity(),
            HasHiJump(),
            CanFreezeEnemies(),
            PONRRequirement("PONR - Enter Cargo Hold from Pump Control Access")
        ])
    ], one_way=True),
    Connection(Sector4SerrisZone, [
        Requirement("Get to Serris Arena from Pump Control Access", [
            # Kill Eyedoor
            CanDamageGadora()
        ], [
            # Cross Breeding Tank
            HasGravity(),
            HasHiJump(),
            HasSpaceJump()
            #future CanDoSimpleUnderwaterWallJump()
        ], [
            # Pass through Tunnel by Save
            CanBomb(),
            CanPowerBomb()
        ], [
            # Can return or escape?
            HasGravity(None, [
                HasSpaceJump(),
                CanDoSimpleWallJump(None, [
                    HasHiJump()
                ]),
            ]),
            HasSpeedBooster(),
            PONRRequirement("PONR - Enter Serris Arena")
        ])
    ], one_way=True),
    Connection(Sector4UpperZone, [
        Requirement("Cross Reservoir West to Reservoir East",[
            Requirement("Cross Reservoir West Top To Skultera Cistern", [
                CanBomb(),
                CanPowerBomb()
            ]),
            Requirement("Cross Reservoir West Bottom to Skultera Cistern", [
                HasMorph(None, [
                    CanActivatePumpControl("Water Drained"),
                    HasGravity("Damage Run",
                               energy_tanks_needed=level_1_e_tanks),
                    HasVaria("Damage Run - Water Physics",
                             energy_tanks_needed=level_2_e_tanks),
                ]),
            ]),
            Requirement("Cross Waterway", [
                # Enter the basin
                CanBomb(),
                CanPowerBomb(),
                HasMorph()
            ], [
                CanActivatePumpControl("Water Drained", [
                    HasSpeedBooster()
                ]),
                CanSpeedBoosterUnderwater("Damage Run - Reservoir West to East through Waterway",
                                          energy_tanks_needed=level_1_e_tanks),
            ])
        ])
    ], one_way=True)
]

Sector4SerrisZone.connections = [
    Connection(Sector4BeforePumpControlZone, [
        HasGravity("Exit Serris Left", [
            CanDoSimpleWallJump(),
            HasSpaceJump()
        ])
    ], one_way=True),
    Connection(Sector4ReservoirVault, [
        HasSpeedBooster()
    ], one_way=True)
]

Sector4ReservoirVault.connections = [
    Connection(Sector4UpperZone, [], one_way=True)
]

Sector4PumpControl.connections = [
    Connection(Sector4BeforePumpControlZone, [
        HasKeycard1()
    ], one_way=True)
]

Sector4UpperWaterZone.connections = [
    Connection(Sector4BeforePumpControlZone, [
        HasKeycard4("Cargo Hold <-> Pump Control Access", [
            # Reach the door from Cargo Hold
            HasGravity(),
            HasHiJump(),
            CanFreezeEnemies(),
            #future CanDoSimpleUnderwaterWallJump()
        ], [
            CanActivatePumpControl(),
            HasGravity("Damage Run - Get to Pump Control Door from Cargo Hold",
                       energy_tanks_needed=level_1_e_tanks),
            HasVaria("Damage Run - Get to Pump Control Door from Cargo Hold - Water Physics",
                        energy_tanks_needed=level_2_e_tanks)
        ])
    ]),
    Connection(Sector5NightmareHub, [
        CanSpeedBoosterUnderwater("Sector 4 -> Sector 5 Pipe", energy_tanks_needed=level_3_e_tanks),
    ], one_way=True),
    Connection(Sector4CargoHold, [
        CanScrewAttackUnderwater()
    ]),
    Connection(Sector4UpperSecurityZone, [
        Requirement("Cross the Speed Booster Blocks in Cargo Hold", [
            CanSpeedBoosterUnderwater()
        ], [
            CanScrewAttackUnderwater("Return through Cargo Hold Item Nook", [
                HasMorph()
            ]),
            HasKeycard4("Vanilla Game Sequence Break - Skip Diffusion", [
                # Get to Upper Security Bypass to charge the initial shinespark
                CanDo10MissileDamage("Climb Cheddar Bay first", [
                    CanDestroyBombBlocksUnderwater(),
                    CanPowerBomb(),
                    HasHiJump("Spring Ball and Bomb", [
                        CanBomb()
                    ])
                ], [
                    HasMorph()
                ]),
                CanJumpHighUnderwater("Climb Security Bypass", [
                    # Break bomb blocks above
                    CanPowerBomb(),
                    CanScrewAttackUnderwater()
                ])
            ], [
                # Trick level
                CanDoExpertShinespark(None, [
                    HasGravity()
                ]),
            ], [
                # Climb to maintain shinespark
                HasSpaceJump(None, [
                    HasHiJump()
                ]),
            ]),
            PONRRequirement("PONR - Cross the Speed Booster Blocks in Cargo Hold")
        ], energy_tanks_needed=level_4_e_tanks),
    ], one_way=True)
]

Sector4CargoHold.connections= [
    Connection(Sector4UpperSecurityZone, [
        CanBallJump(None, [
            HasGravity(hard_items_needed={"Bomb Data"}),
            Requirement(hard_items_needed={"Hi-Jump"}),
        ], energy_tanks_needed=level_4_e_tanks)
    ])
]

Sector4UpperSecurityZone.connections= [
    Connection(Sector4CargoHold, [
        HasMorph("Enter Cargo Hold Nook", [
            CanScrewAttackUnderwater(),
            PONRRequirement("PONR - Enter Cargo Hold Nook")
        ]),
    ], one_way=True),
    Connection(Sector4SecurityZone, [
        CanJumpHighUnderwater("Return from dropping down Aquarium Shaft",
                              hard_items_needed={"Space Jump"}),
        PONRRequirement("PONR - Drop down Aquarium Shaft")
    ], one_way=True)
]

Sector4SecurityZone.connections = [
    Connection(Sector4RightWaterZoneSave, [
        Requirement("Get to Aquarium Hub Save Station from bottom of Aquarium Shaft", [
            # One Level 4 Security Door
            HasKeycard4()
        ], [
            # Tunnels from Aquarium Hub Access
            HasMorph()
        ], [
            HasGravity("Climb Evir Enclosure", [
                HasSpaceJump(),
                CanDoAdvancedWallJump(),
                CanFreezeEnemies(None, [
                    CanDoSimpleWallJump(),
                    HasHiJump()
                ])
            ])
            #future CanDoAdvancedUnderwaterWallJump()
        ], [
            # Combat - Prevent ToughEnemy block from triggering Screw Attack without Gravity Suit
            CanDamageToughEnemy("Kill Evir and Aqua Pirates", enemy_hp=((80 * 2) + (90 * 2)),
                                immunities={"Beam", "Bomb", "Screw Attack", "Power Bomb"}),
            CanScrewAttackUnderwater()
        ], energy_tanks_needed=level_4_e_tanks)
    ]),
    Connection(Sector4LowerSecurityZone, [
        Requirement("Drop down Security Access shaft", [
            # Get to top of Security Access room
            HasKeycard4(),
            HasMissile("Climb Cheddar Bay first", [
                CanDestroyBombBlocksUnderwater(),
                CanPowerBomb(),
                HasHiJump("Spring Ball and Bomb", [
                    CanBomb()
                ])
            ], [
                HasMorph()
            ]),
        ], [
            # Can return?
            PONRRequirement(),
            HasGravity(None, [
                HasSpaceJump(),
                CanDoSimpleWallJump(),
            ])
        ]),
    ], one_way=True),
    Connection(Sector4UpperSecurityZone, [
        Requirement("Can Climb Aquarium Shaft", [
            CanJumpHighUnderwater("Space Jump Underwater",
                                  hard_items_needed={"Space Jump"}),
            HasKeycard4("Vanilla Game Sequence Break - Skip Diffusion - Partial", [
                # Get to Upper Security Bypass to charge the initial shinespark
                CanDo10MissileDamage("Climb Cheddar Bay first", [
                    CanDestroyBombBlocksUnderwater(),
                    CanPowerBomb(),
                    HasHiJump("Spring Ball and Bomb", [
                        CanBomb()
                    ])
                ], [
                    HasMorph()
                ]),
                CanJumpHighUnderwater("Climb Security Bypass", [
                    # Break bomb blocks above
                    CanPowerBomb(),
                    CanScrewAttackUnderwater()
                ])
            ], [
                # Trick level
                CanDoAdvancedShinespark(None, [
                    HasGravity()
                ]),
            ]),
        ])
    ]),
    Connection(Sector4UpperWaterZone, [
        HasKeycard4("Vanilla Game Sequence Break - Skip Diffusion", [
            # Get to Upper Security Bypass to charge the initial shinespark
            CanDo10MissileDamage("Climb Cheddar Bay first", [
                CanDestroyBombBlocksUnderwater(),
                CanPowerBomb(),
                HasHiJump("Spring Ball and Bomb", [
                    CanBomb()
                ])
            ], [
                HasMorph()
            ]),
            CanJumpHighUnderwater("Climb Security Bypass", [
                # Break bomb blocks above
                CanPowerBomb(),
                CanScrewAttackUnderwater()
            ])
        ], [
            # Trick level
            CanDoExpertShinespark(None, [
                HasGravity()
            ]),
        ], [
            # Climb to maintain shinespark
            HasSpaceJump(None, [
                HasHiJump()
            ]),
        ]),
        CanScrewAttackUnderwater("Go through Cargo Hold Nook", [
            HasMorph()
        ], [
            HasSpaceJump()
        ])
    ], one_way=True)
]

Sector4LowerSecurityZone.connections = [
    Connection(Sector4SecurityRoom, [
        CanDestroyBombBlocksUnderwater("Vanilla Entry to Level 4 Security", [
            HasKeycard4(),
            PONRRequirement("PONR - Level 4 Security")
        ], [
            CanDamageToughEnemy("Kill Large Skultera", enemy_hp=(28 * 2), immunities={"Beam"})
        ], [
            HasMorph()
        ], power_bomb_ammo_needed=3)
    ], one_way=True),
    Connection(Sector4SecurityZone, [
        Requirement("Get from bottom of Security Access shaft to inside Cheddar Bay pipe", [
            # Climb Security Access Shaft
            HasGravity(None, [
                HasSpaceJump(),
                CanDoSimpleWallJump()
            ])
        ], [
            # Get into Cheddar Bay
            HasKeycard4(),
            HasMorph("Route through Security Bypass", [
                # Break bomb blocks above
                CanPowerBomb(),
                CanScrewAttackUnderwater()
            ], [
                # Climb up
                CanJumpHighUnderwater(),
                #future CanDoUnderwaterWallJump()
            ], [
                # Break through Pipe
                HasMissile(None, [
                    CanDestroyBombBlocksUnderwater()
                ])
            ])
        ])
    ])
]

Sector4SecurityRoom.connections = [
    Connection(Sector4LowerSecurityZone, [
        HasKeycard4("Leave Level 4 Security Room", [
            HasGravity(None, [
                HasSpaceJump(),
                CanDoSimpleWallJump()
            ]),
            #future CanDoUnderwaterWallJump()
        ])
    ])
]

Sector4RightWaterZone.connections = [
    Connection(Sector4RightDataZone, [
        Requirement("Climb Powamp Shaft", [
            # Get Up
            CanFreezeEnemies("Use Powamps as Platforms", [
                HasGravity(),
                CanJumpHigh()
            ], missile_ammo_needed=10),
            CanJumpHighUnderwater(hard_items_needed={"Space Jump"}),
        ], [
            # Break Missile Blocks
            CanUseDiffusionMissile(),
            PONRRequirement("PONR - Climb Powamp Shaft", [
                HasMissile()
            ])
        ])
    ], one_way=True),
    Connection(Sector4TubeLeft, [
        PONRRequirement("PONR - Powamp Shaft -> Tube Left",[
            CanScrewAttackUnderwater()
        ])
    ], one_way=True),
    Connection(Sector4RightWaterZoneSave, [
        CanScrewAttackUnderwater(),
        PONRRequirement("PONR - Shinespark through Aquarium Hub Kago", [
            CanDoBeginnerShinespark(None, [
                CanSpeedBoosterUnderwater()
            ])
        ])
    ], one_way=True)
]

Sector4RightWaterZoneSave.connections = [
    Connection(Sector4SecurityZone, [
        PONRRequirement("PONR - Aquarium Hub Save -> Aquarium Shaft",[
            HasMorph()
        ], [
            HasKeycard4()
        ], [
            CanDamageToughEnemy("Kill Evir and Aqua Pirates", enemy_hp=((80 * 2) + (90 * 2)),
                                immunities={"Beam", "Bomb", "Screw Attack", "Power Bomb"}),
            CanScrewAttackUnderwater()
        ], energy_tanks_needed=level_4_e_tanks)
    ], one_way=True),
    Connection(Sector4RightWaterZone, [
        PONRRequirement("PONR - Aquarium Hub -> Aquarium Speedway", [
            CanSpeedBoosterUnderwater()
        ], [
            CanBallJump()
        ], [
            CanFreezeEnemies()
        ]),
        CanScrewAttackUnderwater()
    ], one_way=True)
]

Sector4DataZone.connections = [
    Connection(Sector4RightDataZone, [
        HasKeycard4("Powamp Playhouse <-> Top of Powamp Shaft", [
            CanBomb(),
            CanPowerBomb()
        ])
    ])
]

Sector4RightDataZone.connections = [
    Connection(Sector4TubeRight, [
        CanUseDiffusionMissile(None, [
            HasMorph()
        ])
    ]),
    Connection(Sector4RightWaterZone, [
        Requirement("Drop down Powamp Shaft", [
            CanUseDiffusionMissile()
        ], [
            HasMorph()
        ], [
            HasGravity(),
            PONRRequirement("PONR - Drop down Powamp Shaft")
        ])
    ], one_way=True)
]

Sector4Hub.locations = [
    FusionLocation("Sector 4 (AQA) -- Drain Pipe", False, [
        HasMorph("Access Drain Pipe Item", [
            CanActivatePumpControl("After Water is Drained"),
            HasGravity("Damage Run - Drain Pipe",
                       energy_tanks_needed=level_1_e_tanks),
            HasVaria("Damage Run - Drain Pipe - Water Physics",
                     energy_tanks_needed=level_2_e_tanks),
        ], [
            CanDamageMediumGeron("Kill Super Geron"),
            CanDamageAnyGeron("Kill Super Geron - Unrestricted"),
            HasWaveBeam("Open the Gate")
        ])
    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir East", False, [
        CanPowerBomb("Access Reservoir East Item", [
            CanActivatePumpControl("After Water is Drained"),
            HasGravity("Damage Run - Reservoir East",
                       energy_tanks_needed=level_1_e_tanks),
            HasVaria("Damage Run - Reservoir East - Water Physics",
                     energy_tanks_needed=level_2_e_tanks),
        ]),
    ])
]

Sector4PumpControl.locations = [
    FusionLocation("Sector 4 (AQA) -- Pump Control Unit", False, [
        CanActivatePumpControl("Go past Pump Control Terminal", [
            CanBallJump()
        ]),
        PONRRequirement("PONR - Pump Control Unit Item Nook", [
            HasSpeedBooster(),
            HasGravity("Use Drain Pipe below Pump Control Terminal", [
                HasSpaceJump()
            ], energy_tanks_needed=level_2_e_tanks)
        ], [
            HasMorph()
        ])
    ])
]

Sector4BeforePumpControlZone.locations = [
    FusionLocation("Sector 4 (AQA) -- C-Cache", False, [
        CanDestroyBombBlocks("Get to C-Cache from Pump Control Access", [
            HasMorph()
        ]),
        HasKeycard1("Get to C-Cache from Pump Control Access", [
            HasMorph()
        ], [
            HasSpeedBooster()
        ]),
    ])
]

Sector4UpperZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Broken Bridge", False, [
        CanDamageToughEnemy("Obtain Broken Bridge Item", [
            HasMorph()
        ], enemy_hp=(28 * 2))
    ]),
    FusionLocation("Sector 4 (AQA) -- Waterway", False, [
        CanActivatePumpControl("Waterway - Water Drained", [
            HasMorph()
        ], [
            HasSpeedBooster()
        ]),
        CanSpeedBoosterUnderwater("Damage Run - Waterway Drowned", [
            HasMorph()
        ], energy_tanks_needed=level_2_e_tanks)
    ])
]

Sector4ReservoirVault.locations = [
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Lower Item", False, [
        CanEnterReservoirVault(None, [
            HasMissile(missile_ammo_needed=2)
        ])
    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Upper Item", False, [
        CanEnterReservoirVault()
    ])
]

Sector4SerrisZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Serris Arena", True, [
        CanFightEarlyGameBoss("Fight Serris", [
            # Dodging
            CanJumpHigh(),
            CanDoAdvancedCombat()
        ], boss_hp=50, immunities={"Beam", "Bomb", "Power Bomb", "Screw Attack"}),
        CanFightBossOnExpert("Fight Serris - Expert Combat", boss_hp=50, immunities={"Beam", "Bomb", "Power Bomb", "Screw Attack"})
    ])
]

Sector4UpperWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cargo Hold", False, [
        CanScrewAttackUnderwater(),
        CanSpeedBoosterUnderwater("Secret Tunnel in Aquarium Shaft", [
            HasMorph()
        ])
    ])
]

Sector4UpperSecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Yard Firing Range", False, [
        CanDamageToughEnemy(enemy_hp=(60*8)),
        CanPowerBomb(power_bomb_ammo_needed=2), # Requires two Power Bombs to kill a Yard
        CanScrewAttackUnderwater(),
        Requirement("Pacifist", energy_tanks_needed=level_3_e_tanks)
    ])
]

Sector4SecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cheddar Bay", False, [
        HasMissile("Break through Pipe Ceiling", [
            CanDestroyBombBlocksUnderwater(),
            CanPowerBomb(),
            HasHiJump("Spring Ball and Bomb", [
                CanBomb()
            ])
        ], [
            HasMorph()
        ]),
        HasKeycard4("Route through Security Bypass", [
            # Break bomb blocks above
            CanPowerBomb(),
            CanScrewAttackUnderwater()
        ], [
            # Climb up
            CanJumpHighUnderwater(),
            #future CanDoUnderwaterWallJump()
        ], [
            HasMorph()
        ])
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Pirate Tank", False, [
        CanPowerBomb("Can Obtain Aquarium Pirate Tank Item", [
            CanDamageToughEnemy("Kill Aqua Pirates", enemy_hp=(90 * 3), immunities={"Beam", "Bomb"}),
        ], [
            # Escape Requirements
            CanFreezeEnemies(None, [
                HasHiJump()
            ], missile_ammo_needed=6),
            CanJumpHighUnderwater(None, [
                HasSpaceJump()
            ], [
                HasScrewAttack(),
                CanDoAdvancedCombat()
            ]),
            PONRRequirement("PONR - Aquarium Pirate Tank Item"),
        ]),
    ])
]

Sector4LowerSecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Sanctuary Cache", False, [
        CanDoScizerSanctuary(None, [
            # Break bomb blocks inside tunnel
            CanBomb(),
            CanPowerBomb()
        ], [
            CanBallJump()
        ], [
            HasGravity("Can Bomb Jump Underwater"),
            HasHiJump()
        ])
    ])
]

Sector4SecurityRoom.locations = [
    FusionLocation("Sector 4 (AQA) -- Level 4 Security Room", True, [])
]

Sector4RightWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Left Item", False, [
        CanSpeedBoosterUnderwater(),
        CanScrewAttackUnderwater(),
        HasGravity("Space Jump Up, Take Secret Tunnel", [
            HasSpaceJump()
        ], [
            HasMorph()
        ])
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Right Item", False, [
        CanSpeedBoosterUnderwater()
    ])
]

Sector4DataZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Data Room", True, [
        HasKeycard4()
    ])
]
