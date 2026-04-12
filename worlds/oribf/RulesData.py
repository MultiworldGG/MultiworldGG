# Location and Connection rules copied (with some changes) from 
# https://github.com/sparkle-preference/ori_rando_server/blob/master/seedbuilder/areas.ori

location_rules: dict[str, dict[str, dict[str, list[list[str | tuple[str, int]]]]]] = {
    "TeleporterNetwork": {
    },
    "SunkenGladesRunaway": { 
        "FirstPickup": {
            "casual": [["Free"]]
        },
        "FirstEnergyCell": {
            "casual": [["Free"]]
        },
        "FronkeyFight": {
            "casual": [["Free"]]
        },
        "Sein":{
            "casual": [["Free"]]
        },
        "GladesKeystone1": {
            "casual": [["Free"]]
        },
        "GladesKeystone2": {
            "casual": [["Free"]]
        },
        "GladesGrenadePool": {
            "casual": [["Grenade", "CleanWater"]], 
            "expert": [["Grenade", ("HealthCell", 6)], ["Grenade", "Stomp", ("HealthCell", 5)]], 
            "master": [["Grenade", ("HealthCell", 5)]]
        },
        "GladesGrenadeTree": {
            "casual": [["Grenade", "ChargeJump"], ["Grenade", "Bash"]], 
            "standard": [["Grenade", "WallJump", "DoubleJump"], ["Grenade", "Glide", "Wind", "WallJump"], ["Grenade", "Glide", "Wind", "Climb"]], 
            "expert": [["Grenade", "ChargeDash"]], 
            "glitched": [["Grenade"]]
        },
        "GladesMainPool": {
            "casual": [["CleanWater"]], 
            "expert": [["Bash", ("HealthCell", 3)], ["Stomp", ("HealthCell", 3)], [("HealthCell", 4)]], 
            "master": [[("HealthCell", 3)]]
        },
        "GladesMainPoolDeep": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 7)]]
        },
        "FronkeyWalkRoof": {
            "casual": [["ChargeJump"], ["Glide", "Wind"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "GladesFirstKeyDoor": {
    },
    "GladesFirstKeyDoorOpened": {
    },
    "GladesMain": { 
        "FourthHealthCell": {
            "casual": [["Free"]]
        },
        "GladesMapKeystone": {
            "casual": [["Free"]]
        },
        "GladesMap": {
            "casual": [[("MapStone", 9)], [("GladesMapStone", 1)]]
        },
        "GladesMapEvent": {
            "casual": [["Free"]]
        }
    },
    "GladesMainAttic": { 
        "AboveFourthHealth": {
            "casual": [["Free"]]
        }
    },
    "LeftGlades": { 
        "LeftGladesHiddenExp": {
            "casual": [["Free"]]
        },
        "WallJumpSkillTree": {
            "casual": [["Free"]]
        },
        "WallJumpAreaExp": {
            "casual": [["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["Lure", "Bash"]]
        },
        "WallJumpAreaEnergyCell": {
            "casual": [["WallJump"], ["ChargeJump"], ["Climb"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"], ["Lure", "Bash"]]
        }
    },
    "UpperLeftGlades": { 
        "LeftGladesExp": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "expert": [["Bash"], ["DoubleJump"]]
        },
        "LeftGladesKeystone": {
            "casual": [["Free"]]
        },
        "LeftGladesMapstone": {
            "casual": [["Free"]]
        }
    },
    "DeathGauntletDoor": {
    },
    "DeathGauntletDoorOpened": {
    },
    "DeathGauntletMoat": { 
        "DeathGauntletSwimEnergyDoor": {
            "casual": [[("EnergyCell", 4)]]
        }
    },
    "DeathGauntlet": { 
        "DeathGauntletExp": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump"]], 
            "standard": [["Lure", "Bash"]]
        },
        "DeathGauntletStompSwim": {
            "casual": [["Stomp", "CleanWater"]], 
            "standard": [["Lure", "CleanWater"]], 
            "expert": [[("HealthCell", 3)]]
        },
        "DeathGauntletEnergyCell": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump"]]
        }
    },
    "DeathGauntletRoof": { 
        "DeathGauntletRoofHealthCell": {
            "casual": [["Free"]]
        }
    },
    "DeathGauntletRoofPlantAccess": { 
        "DeathGauntletRoofPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "SpiritCavernsDoor": {
    },
    "SpiritCavernsDoorOpened": {
    },
    "LowerSpiritCaverns": { 
        "SpiritCavernsKeystone1": {
            "casual": [["Free"]]
        },
        "SpiritCavernsKeystone2": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash"], ["DoubleJump"]], 
            "expert": [["ChargeDash"]], 
            "master": [["Free"]]
        },
        "SpiritCavernsAbilityCell": {
            "casual": [["ChargeJump"], ["Bash"]], 
            "standard": [["WallJump", "DoubleJump"]], 
            "expert": [["Climb", "DoubleJump"], ["ChargeDash"]], 
            "master": [["TripleJump"]]
        }
    },
    "MidSpiritCaverns": {
    },
    "UpperSpiritCaverns": { 
        "SpiritCavernsTopLeftKeystone": {
            "casual": [["WallJump"], ["DoubleJump", "Climb"], ["Glide", "Climb"], ["ChargeJump", ("HealthCell", 3)], ["Bash", ("HealthCell", 3)]], 
            "standard": [["ChargeJump"], ["Bash"]], 
            "master": [["Climb"], ["DoubleJump"]]
        },
        "SpiritCavernsTopRightKeystone": {
            "casual": [["Free"]]
        }
    },
    "SpiritTreeDoor": {
    },
    "SpiritTreeDoorOpened": {
    },
    "GladesLaserArea": { 
        "GladesLaser": {
            "casual": [["DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["WallJump", "Glide", ("HealthCell", 3)], ["ChargeDash"]]
        },
        "GladesLaserGrenade": {
            "casual": [["Grenade", "Climb", "ChargeJump", "Bash"], ["Grenade", "WallJump", "DoubleJump", "Bash"]], 
            "standard": [["Grenade", "Climb", "Bash"], ["Grenade", "Climb", "DoubleJump", "ChargeJump", "Glide"], ["Grenade", "WallJump", "Bash"], ["Grenade", "Climb", "DoubleJump", "AirDash", "ChargeJump"], ["Grenade", "WallJump", "DoubleJump", "AirDash", "ChargeJump", "Glide"]], 
            "expert": [["Grenade", "Climb", "ChargeJump", "CleanWater"], ["Grenade", "WallJump", "DoubleJump", "ChargeJump", "CleanWater"], ["Grenade", "WallJump", "DoubleJump", "ChargeJump", "Glide"], ["Grenade", "ChargeJump", ("HealthCell", 5)], ["Grenade", "ChargeJump", ("HealthCell", 4), ("AbilityCell", 3), ("EnergyCell", 1)], ["Grenade", "ChargeJump", ("HealthCell", 3), ("AbilityCell", 3), ("EnergyCell", 2)], ["Grenade", "ChargeJump", ("HealthCell", 3), ("AbilityCell", 6), ("EnergyCell", 1)], ["Grenade", "ChargeJump", "Glide", ("HealthCell", 3)], ["Grenade", "ChargeJump", "Bash", ("HealthCell", 3)], ["Grenade", "ChargeJump", "CleanWater", ("HealthCell", 3)], ["Grenade", "Climb", "ChargeJump", ("HealthCell", 3)], ["Grenade", "Climb", "ChargeDash", ("HealthCell", 5), ("EnergyCell", 1)], ["Grenade", "Climb", "ChargeDash", ("HealthCell", 3), ("EnergyCell", 2)], ["Grenade", "Climb", "ChargeDash", "Glide", ("HealthCell", 3), ("EnergyCell", 1)], ["Grenade", "Climb", "ChargeDash", "CleanWater", ("HealthCell", 3), ("EnergyCell", 1)], ["Grenade", "Climb", "DoubleJump", "ChargeDash", ("HealthCell", 3), ("EnergyCell", 1)], ["Grenade", "WallJump", "DoubleJump", "ChargeJump", ("HealthCell", 3)], ["Grenade", "WallJump", "ChargeDash", ("HealthCell", 5), ("EnergyCell", 1)], ["Grenade", "WallJump", "ChargeDash", ("HealthCell", 3), ("EnergyCell", 2)], ["Grenade", "WallJump", "ChargeDash", "Glide", ("HealthCell", 3), ("EnergyCell", 1)], ["Grenade", "WallJump", "ChargeDash", "CleanWater", ("HealthCell", 3), ("EnergyCell", 1)], ["Grenade", "Climb", "ChargeDash", "ChargeJump", ("EnergyCell", 2)], ["Grenade", "Climb", "ChargeDash", "ChargeJump", "Glide", ("EnergyCell", 1)], ["Grenade", "WallJump", "DoubleJump", "ChargeDash", ("EnergyCell", 1)]], 
            "master": [["Grenade", "DoubleJump", "Bash"], ["GrenadeJump"]]
        }
    },
    "ChargeFlameSkillTreeChamber": { 
        "ChargeFlameSkillTree": {
            "casual": [["Free"]]
        }
    },
    "ChargeFlameAreaStump": {
    },
    "ChargeFlameAreaPlantAccess": { 
        "ChargeFlameAreaPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "LowerChargeFlameArea": { 
        "ChargeFlameAreaExp": {
            "casual": [["Free"]]
        }
    },
    "SpiritTreeRefined": { 
        "AboveChargeFlameTreeExp": {
            "casual": [["DoubleJump", "Climb"], ["DoubleJump", "WallJump"], ["ChargeJump", "Climb"], ["ChargeJump", "WallJump"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["Bash", "Grenade"]], 
            "standard": [["Bash", "Glide", "WallJump"], ["Bash", "Glide", "Climb"], ["AirDash", "WallJump"], ["AirDash", "Climb"]], 
            "expert": [["Dash", "WallJump"], ["Dash", "Climb"]], 
            "master": [["Bash", "Glide", "DoubleJump"]]
        },
        "SpiritTreeExp": {
            "casual": [["ChargeJump"], ["BashGrenade"]], 
            "standard": [["Lure", "Bash", "ChargeFlame"], ["Lure", "Bash", "Stomp", "WallJump"], ["Lure", "Bash", "Stomp", "Climb"], ["Lure", "Bash", "Stomp", "DoubleJump"]], 
            "expert": [["Lure", "RocketJump", ("EnergyCell", 1)]], 
            "master": [["TripleJump"]]
        }
    },
    "SpiderSacTetherArea": { 
        "SpiderSacHealthCell": {
            "casual": [["ChargeFlame", "WallJump"], ["ChargeFlame", "DoubleJump"], ["ChargeFlame", "Climb", "ChargeJump"], ["Grenade", "WallJump"], ["Grenade", "DoubleJump"], ["Grenade", "Climb", "ChargeJump"], ["ChargeFlame", ("HealthCell", 3)], ["Grenade", ("HealthCell", 3)]], 
            "expert": [["ChargeDash"]], 
            "master": [["ChargeFlame", "DoubleJump"], ["Grenade", "DoubleJump"], ["ChargeDash", "DoubleJump"]]
        },
        "SpiderSacEnergyDoor": {
            "casual": [[("EnergyCell", 4)]], 
            "timed-level": [[("EnergyCell", 2)]], 
            "glitched": [[("EnergyCell", 3)]], 
            "master": [[("EnergyCell", 2)]]
        },
        "SpiderSacGrenadeDoor": {
            "casual": [["Grenade", "Bash"], ["Grenade", "DoubleJump", "WallJump"], ["Grenade", "ChargeJump"]], 
            "expert": [["Grenade", "DoubleJump", "Climb"], ["Grenade", "ChargeDash"]]
        }
    },
    "SpiderSacArea": {
    },
    "SpiderSacEnergyNook": { 
        "SpiderSacEnergyCell": {
            "casual": [["Free"]]
        }
    },
    "SpiderWaterArea": { 
        "GroveSpiderWaterSwim": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 6)], ["Bash", ("HealthCell", 5)]], 
            "master": [[("HealthCell", 5)], [("HealthCell", 4), "UltraDefense"], ["Bash", "UltraDefense", ("HealthCell", 3)]]
        },
        "GroveAboveSpiderWaterExp": {
            "casual": [["ChargeJump", "DoubleJump", "WallJump"], ["ChargeJump", "DoubleJump", "Climb"], ["Bash", "DoubleJump", "WallJump"], ["Bash", "DoubleJump", "Climb"]], 
            "standard": [["ChargeJump", "Bash", "WallJump"], ["ChargeJump", "Bash", "Climb"]], 
            "expert": [["DoubleBash"], ["ChargeDash"]], 
            "master": [["GrenadeJump"]]
        },
        "GroveAboveSpiderWaterHealthCell": {
            "casual": [["ChargeJump", "WallJump", "DoubleJump"], ["ChargeJump", "Climb"], ["Bash", "WallJump"], ["Bash", "Grenade"], ["Bash", "DoubleJump"], ["Bash", "Glide"]], 
            "standard": [["Bash", "ChargeJump"]], 
            "expert": [["DoubleBash"], ["ChargeDash"]], 
            "master": [["GrenadeJump"]]
        },
        "GroveAboveSpiderWaterEnergyCell": {
            "casual": [["Grenade", "ChargeJump", "Climb", "DoubleJump"]], 
            "standard": [["Grenade", "ChargeJump", "WallJump", "DoubleJump", "Glide"], ["Grenade", "ChargeJump", "WallJump", "DoubleJump", "Dash"], ["Grenade", "Bash"]], 
            "expert": [["Grenade", "ChargeDash"]]
        }
    },
    "BlackrootDarknessRoom": { 
        "DashAreaOrbRoomExp": {
            "casual": [["WallJump"], ["Climb"], ["Bash"], ["ChargeJump"], ["DoubleJump"]]
        },
        "DashAreaAbilityCell": {
            "casual": [["WallJump"], ["Climb"], ["Bash"], ["ChargeJump"], ["DoubleJump"]]
        },
        "DashAreaRoofExp": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "master": [["DoubleJump"], ["Bash"]]
        }
    },
    "DashArea": { 
        "DashSkillTree": {
            "casual": [["Free"]]
        }
    },
    "DashAreaMapstoneAccess": { 
        "DashAreaMapstone": {
            "casual": [["Dash"]], 
            "expert": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump"]]
        }
    },
    "DashPlantAccess": { 
        "DashAreaPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "RazielNoArea": { 
        "RazielNo": {
            "casual": [["Free"]]
        }
    },
    "BlackrootGrottoConnection": { 
        "BlackrootTeleporterHealthCell": {
            "casual": [["Free"]]
        },
        "BlackrootBoulderExp": {
            "casual": [["Stomp"]], 
            "glitched": [["Free"]]
        },
        "BlackrootMap": {
            "casual": [[("MapStone", 9), "WallJump"], [("MapStone", 9), "Climb", "DoubleJump"], [("MapStone", 9), "Bash", "Grenade"], [("MapStone", 9), "ChargeJump"], [("BlackrootMapStone", 1), "WallJump"], [("BlackrootMapStone", 1), "Climb", "DoubleJump"], [("BlackrootMapStone", 1), "Bash", "Grenade"], [("BlackrootMapStone", 1), "ChargeJump"]], 
            "standard": [[("MapStone", 9), "Climb", "AirDash"], [("BlackrootMapStone", 1), "Climb", "AirDash"]], 
            "expert": [[("MapStone", 9), "Climb"], [("BlackrootMapStone", 1), "Climb"]]
        },
        "BlackrootMapEvent": {
            "casual": [["WallJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "standard": [["Climb", "AirDash"]], 
            "expert": [["Climb"]]
        }
    },
    "GrenadeAreaAccess": {
    },
    "GrenadeArea": { 
        "GrenadeSkillTree": {
            "casual": [["Dash", "WallJump"], ["Dash", "Climb"], ["Dash", "ChargeJump"], ["Dash", "Bash", "Grenade"]], 
            "standard": [["Bash", "Grenade"]], 
            "expert": [["Dash", "Bash"], ["DoubleJump", "WallJump"], ["DoubleJump", "Climb"], ["ChargeDash"], ["DoubleBash", "WallJump"], ["DoubleBash", "Climb"], ["DoubleBash", "DoubleJump"], ["DoubleBash", "ChargeJump"]], 
            "master": [["ChargeJump"]], 
            "insane": [["WallJump"]]
        },
        "GrenadeAreaExp": {
            "casual": [["Dash", "WallJump", "Glide"], ["Dash", "Climb", "Glide"], ["Dash", "Bash", "Glide"], ["ChargeJump", "DoubleJump"], ["Bash", "Grenade"], ["ChargeJump", ("HealthCell", 3)]], 
            "standard": [["Dash", "DoubleJump"]], 
            "expert": [["ChargeDash"], ["DoubleBash", "WallJump"], ["DoubleBash", "Climb"], ["DoubleBash", "DoubleJump"], ["DoubleBash", "ChargeJump"]]
        },
        "GrenadeAreaAbilityCell": {
            "casual": [["Dash", "Bash", "Grenade"], ["Dash", "ChargeJump", "Grenade"]], 
            "standard": [["Bash", "Grenade"]], 
            "expert": [["ChargeDash", "Grenade"]], 
            "master": [["ChargeJump", "Grenade"]]
        }
    },
    "LowerBlackroot": { 
        "LowerBlackrootAbilityCell": {
            "casual": [["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["DoubleJump", ("HealthCell", 5)], ["ChargeDash"]], 
            "master": [["DoubleJump"]]
        },
        "LowerBlackrootLaserAbilityCell": {
            "casual": [["Dash", "Bash", "Grenade"]], 
            "standard": [["Dash", "DoubleJump"], ["Dash", "ChargeJump", ("HealthCell", 4)]], 
            "expert": [["DoubleJump", "Glide"], ["Bash", "Grenade"], ["WallJump", "Glide", ("HealthCell", 4)], ["Stomp", "Glide", ("HealthCell", 4)], ["DoubleJump", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4)], ["AirDash", ("HealthCell", 4)]], 
            "master": [["Stomp", ("HealthCell", 4)]]
        },
        "LowerBlackrootLaserExp": {
            "casual": [["Dash", "WallJump"], ["Dash", "Climb", "DoubleJump"], ["Dash", "Bash", "Grenade"], ["Dash", "ChargeJump"]], 
            "expert": [["WallJump"], ["DoubleJump"], ["Bash", "Grenade"], ["ChargeJump"], ["ChargeDash"]]
        },
        "LowerBlackrootGrenadeThrow": {
            "casual": [["WallJump", "Grenade"], ["Climb", "Grenade"], ["DoubleJump", "Grenade"], ["ChargeJump", "Grenade"], ["Bash", "Grenade"], ["Glide", "Grenade"]], 
            "standard": [["ChargeJump", "DoubleJump"]], 
            "timed-level": [["Free"]]
        }
    },
    "LostGrove": { 
        "LostGroveLongSwim": {
            "casual": [["CleanWater"]], 
            "master": [[("HealthCell", 6), "UltraDefense"], [("HealthCell", 12)]]
        }
    },
    "LostGroveExit": { 
        "LostGroveAbilityCell": {
            "casual": [["Free"]]
        },
        "LostGroveHiddenExp": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump"]]
        },
        "LostGroveTeleporter": {
            "casual": [["BashGrenade"], ["Grenade", "WallJump", "DoubleJump", "Glide"], ["Grenade", "Climb", "DoubleJump", "Glide"], ["Dash", "WallJump"], ["Dash", "Climb"], ["Dash", "ChargeJump"]], 
            "standard": [["Grenade", "Glide", "WallJump", ("HealthCell", 3)], ["Grenade", "Glide", "Climb", ("HealthCell", 3)], ["Grenade", "DoubleJump", "WallJump", ("HealthCell", 3)], ["Grenade", "DoubleJump", "Climb", ("HealthCell", 3)], ["Grenade", "Glide", "ChargeJump", ("HealthCell", 3)], ["Grenade", "DoubleJump", "ChargeJump", ("HealthCell", 3)]], 
            "expert": [["Grenade", "ChargeJump", ("HealthCell", 5)]], 
            "master": [["GrenadeJump"], ["Grenade", "DoubleJump", ("HealthCell", 3)], ["Grenade", "TripleJump"], ["Dash", "DoubleJump"]]
        }
    },
    "HollowGrove": { 
        "HollowGroveMapstone": {
            "casual": [["Free"]]
        },
        "GroveWaterStompAbilityCell": {
            "casual": [["CleanWater", "Stomp"]], 
            "expert": [["Lure", "Bash", "CleanWater"], ["Bash", ("HealthCell", 6)], ["Stomp", ("HealthCell", 5)]], 
            "master": [["Lure", ("HealthCell", 5)], ["Lure", "UltraDefense", ("HealthCell", 3)]], 
            "glitched": [["Bash"]]
        },
        "HoruFieldsHealthCell": {
            "casual": [["Stomp"]], 
            "standard": [["Lure", "Free"]]
        },
        "HollowGroveTreePlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        },
        "HollowGroveTreeAbilityCell": {
            "casual": [["WallJump", "DoubleJump"], ["Wind", "Glide"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash", "WallJump"], ["Lure", "Bash", "Climb"], ["Stomp", "Glide", "WallJump", "AirDash"], ["Stomp", "Glide", "Climb", "AirDash"]], 
            "expert": [["ChargeDash"], ["DoubleBash"]], 
            "master": [["Stomp", "DoubleJump"]]
        },
        "HollowGroveMap": {
            "casual": [[("MapStone", 9)], [("GroveMapStone", 1)]]
        },
        "HollowGroveMapEvent": {
            "casual": [["Free"]]
        },
        "HollowGroveMapPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        },
        "SwampTeleporterAbilityCell": {
            "casual": [["Wind", "Glide"], ["ChargeJump", "DoubleJump", "Glide", "WallJump"], ["ChargeJump", "DoubleJump", "Glide", "Climb"], ["Bash", "Grenade", "Glide", "DoubleJump"], ["Bash", "Grenade", "Glide", "WallJump"], ["Bash", "Grenade", "Glide", "Climb"]], 
            "standard": [["Bash", "Grenade", "Glide"], ["Bash", "Grenade", "DoubleJump"], ["ChargeJump", "DoubleJump", "Glide", "AirDash"]], 
            "expert": [["Bash", "Grenade"], ["ChargeDash"]], 
            "master": [["ChargeJump", "DoubleJump", "Glide"], ["Lure", "Bash"], ["ChargeJump", "TripleJump"], ["GrenadeJump"]]
        }
    },
    "SwampTeleporter": {
    },
    "OuterSwampUpperArea": { 
        "OuterSwampGrenadeExp": {
            "casual": [["Grenade", "WallJump"], ["Grenade", "Climb"], ["Grenade", "ChargeJump"], ["Grenade", "Bash"]]
        }
    },
    "OuterSwampAbilityCellNook": { 
        "OuterSwampAbilityCell": {
            "casual": [["Free"]]
        }
    },
    "OuterSwampLowerArea": {
    },
    "OuterSwampSwarmLedge": {
        "OuterSwampStompExp": {
            "casual": [["CleanWater"]],
            "standard": [["Free"]]
        },
        "OuterSwampHealthCell": {
            "casual": [["WallJump", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]],
            "standard": [["Climb", "DoubleJump", "Glide"]],
            "expert": [["Climb", "DoubleJump"], ["ChargeDash", ("EnergyCell", 1)]],
            "master": [["Bash"], ["DoubleJump", "Glide"], ["TripleJump"]]
        }
    },
    "OuterSwampMortarAbilityCellLedge": { 
        "OuterSwampMortarAbilityCell": {
            "casual": [["Free"]]
        }
    },
    "OuterSwampMortarPlantAccess": { 
        "OuterSwampMortarPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "GinsoOuterDoor": {
    },
    "GinsoInnerDoor": {
    },
    "LowerGinsoTree": { 
        "LowerGinsoHiddenExp": {
            "casual": [["ChargeJump"], ["Bash", "Grenade"], ["WallJump", "DoubleJump"], ["Climb", "DoubleJump"]], 
            "master": [["DoubleJump"], ["ChargeDash", "Climb"], ["ChargeDash", "WallJump"]]
        },
        "LowerGinsoPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "GinsoMiniBossDoor": { 
        "LowerGinsoKeystone1": {
            "casual": [["DoubleJump"], ["Glide"]], 
            "standard": [["Bash", "Grenade"], [("HealthCell", 3)], ["AirDash"]]
        },
        "LowerGinsoKeystone2": {
            "casual": [["DoubleJump"], ["Glide"]], 
            "standard": [["Bash", "Grenade"], ["ChargeJump", ("HealthCell", 3)], ["AirDash"]]
        },
        "LowerGinsoKeystone3": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        },
        "LowerGinsoKeystone4": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        }
    },
    "BashTreeDoorClosed": {
    },
    "BashTreeDoorOpened": {
    },
    "BashTree": { 
        "BashSkillTree": {
            "casual": [["Free"]]
        },
        "BashAreaExp": {
            "casual": [["Bash"], ["ChargeJump"]], 
            "expert": [["WallJump", "DoubleJump", "ChargeDash"]], 
            "master": [["TripleJump"]]
        }
    },
    "UpperGinsoRedirectArea": { 
        "UpperGinsoRedirectLowerExp": {
            "casual": [["Stomp"], ["Bash"]], 
            "standard": [["ChargeJump", "Climb"]], 
            "expert": [["ChargeFlame"], ["ChargeJump", "AirDash"]], 
            "master": [["Grenade"]]
        },
        "UpperGinsoRedirectUpperExp": {
            "casual": [["Stomp"], ["Bash"]], 
            "expert": [["ChargeFlame"], ["Climb", "ChargeJump"], ["ChargeJump", "AirDash"]]
        }
    },
    "UpperGinsoTree": { 
        "UpperGinsoLowerKeystone": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"]], 
            "standard": [["Bash", ("HealthCell", 3)], ["DoubleJump", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 3)], ["ChargeJump", "AirDash"]], 
            "expert": [[("HealthCell", 5)], ["ChargeDash"]]
        },
        "UpperGinsoRightKeystone": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"]], 
            "standard": [["Bash"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["ChargeJump", ("HealthCell", 3)], ["ChargeJump", "AirDash"]], 
            "expert": [["WallJump", "DoubleJump", ("HealthCell", 5)]], 
            "master": [["TripleJump", "UltraDefense", ("HealthCell", 3)]]
        },
        "UpperGinsoUpperRightKeystone": {
            "casual": [["Bash", "DoubleJump"]], 
            "standard": [["Bash"], ["ChargeJump", "DoubleJump"], ["ChargeJump", ("HealthCell", 3)]], 
            "master": [["TripleJump", "UltraDefense", ("HealthCell", 5)]]
        },
        "UpperGinsoUpperLeftKeystone": {
            "casual": [["Bash", "DoubleJump"]], 
            "standard": [["Bash"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["ChargeJump", ("HealthCell", 3)], ["ChargeJump", "AirDash"]], 
            "master": [[ "TripleJump", "UltraDefense", ("HealthCell", 5)]]
        },
        "UpperGinsoEnergyCell": {
            "casual": [["Stomp"], ["Bash"]], 
            "standard": [["ChargeJump", "Climb"]], 
            "expert": [["ChargeJump", "Dash"], ["ChargeFlame"]]
        }
    },
    "UpperGinsoDoorClosed": {
    },
    "UpperGinsoDoorOpened": {
    },
    "GinsoTeleporter": {
    },
    "TopGinsoTree": { 
        "TopGinsoLeftLowerExp": {
            "casual": [["DoubleJump", "WallJump"], ["DoubleJump", "Climb"], ["Bash", "DoubleJump"], ["Bash", "Glide"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"]], 
            "standard": [["Bash"], ["ChargeJump", ("HealthCell", 3)], ["DoubleJump", ("HealthCell", 3)]], 
            "expert": [["ChargeDash"], [("HealthCell", 5)]], 
            "master": [["DoubleJump"]]
        },
        "TopGinsoLeftUpperExp": {
            "casual": [["Bash"], ["ChargeJump"]], 
            "standard": [["Dash", "WallJump", "DoubleJump", ("HealthCell", 3)], ["Dash", "Climb", "DoubleJump", ("HealthCell", 3)], ["WallJump", "DoubleJump", "Glide", ("HealthCell", 3)], ["Climb", "DoubleJump", "Glide", ("HealthCell", 3)]], 
            "expert": [["ChargeDash"]], 
            "master": [["TripleJump"], ["DoubleJump", "Glide", ("HealthCell", 3)], ["DoubleJump", "Dash", ("HealthCell", 3)]]
        },
        "TopGinsoRightPlant": {
            "casual": [["Bash", "ChargeFlame"], ["Bash", "Grenade"], ["ChargeJump", "ChargeFlame"], ["ChargeJump", "Grenade"]], 
            "standard": [["DoubleJump", "WallJump", "Grenade", ("HealthCell", 3)], ["DoubleJump", "Climb", "Grenade", ("HealthCell", 3)]], 
            "expert": [["DoubleJump", "WallJump", "ChargeFlame", ("HealthCell", 3)], ["DoubleJump", "Climb", "ChargeFlame", ("HealthCell", 3)], ["ChargeDash"]], 
            "master": [["TripleJump", "ChargeFlame"], ["TripleJump", "Grenade"], ["DoubleJump", "ChargeFlame", ("HealthCell", 3)], ["DoubleJump", "Grenade", ("HealthCell", 3)]]
        }
    },
    "GinsoEscape": {
    },
    "GinsoEscapeComplete": { 
        "GinsoEscapeSpiderExp": {
            "casual": [["Free"]]
        },
        "GinsoEscapeJumpPadExp": {
            "casual": [["Free"]]
        },
        "GinsoEscapeProjectileExp": {
            "casual": [["Free"]]
        },
        "GinsoEscapeHangingExp": {
            "casual": [["Free"]]
        },
        "GinsoEscapeExit": {
            "casual": [["Free"]]
        }
    },
    "UpperGrotto": { 
        "GrottoLasersRoofExp": {
            "casual": [["WallJump", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Climb", "DoubleJump"]], 
            "expert": [["WallJump", "ChargeDash"], ["Climb", "ChargeDash"]], 
            "master": [["Bash"], ["DoubleJump", "Glide"]]
        }
    },
    "MoonGrottoStompPlantAccess": { 
        "MoonGrottoStompPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "MoonGrottoAboveTeleporter": {
        "AboveGrottoTeleporterExp": {
            "casual": [["DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"], ["Bash", "WallJump"], ["Bash", "Climb"]],
            "expert": [["ChargeDash"], ["DoubleBash"]]
        },
        "LeftGrottoTeleporterExp": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump", "ChargeJump"]],
            "standard": [["DoubleJump", "AirDash"], ["Climb", "Glide", ("HealthCell", 4)], ["Climb", "DoubleJump", ("HealthCell", 4)], ["DoubleJump", "Glide", ("HealthCell", 4)], ["Climb", "AirDash", ("HealthCell", 4)], ["WallJump", "AirDash", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4)]],
            "expert": [["Grenade", "Bash"], ["Climb", "ChargeJump"], ["DoubleJump", "Dash"], ["ChargeJump", ("HealthCell", 4)], ["WallJump", "Glide", ("HealthCell", 4)], ["DoubleJump", ("HealthCell", 4)], ["WallJump", ("HealthCell", 7)], ["Climb", ("HealthCell", 7)], ["ChargeDash", ("HealthCell", 4)]],
            "master": [["Lure", "Bash"], ["TripleJump"], ["ChargeDash"]]
        }
    },
    "MoonGrotto": {
        "GrottoEnergyDoorSwim": {
            "casual": [[("EnergyCell", 2), "CleanWater"]],
            "expert": [[("EnergyCell", 2), ("HealthCell", 3)]]
        },
        "GrottoEnergyDoorHealthCell": {
            "casual": [[("EnergyCell", 2), "ChargeJump"], [("EnergyCell", 2), "Bash", "Grenade"], [("EnergyCell", 2), "WallJump", "DoubleJump"]],
            "standard": [[("EnergyCell", 2), "WallJump", ("HealthCell", 3)], [("EnergyCell", 2), "Climb", "AirDash"]],
            "expert": [[("EnergyCell", 2), "Climb", "Glide"], [("EnergyCell", 2), "Climb", "DoubleJump", ("HealthCell", 3)], [("EnergyCell", 2), "ChargeDash"]]
        },
        "BelowGrottoTeleporterHealthCell": {
            "casual": [["DoubleJump", "Bash", "WallJump"], ["DoubleJump", "Bash", "Climb"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide", "WallJump"], ["ChargeJump", "Glide", "Climb"]],
            "standard": [["ChargeJump", "Glide"], ["Bash", "WallJump", "Glide"], ["Bash", "Grenade"], ["ChargeJump", ("HealthCell", 3)], ["Bash", "DoubleJump", ("HealthCell", 3)], ["Bash", "AirDash", "WallJump"], ["Bash", "AirDash", "Climb"], ["ChargeJump", "AirDash"]],
            "expert": [["DoubleJump", "Bash"], ["WallJump", "Bash", ("HealthCell", 6)], ["ChargeDash", ("HealthCell", 3)], ["Lure", "Bash", "Glide", ("HealthCell", 6)], ["ChargeDash", "WallJump"], ["ChargeDash", "Climb"], ["AirDash", "Bash"]],
            "master": [["Bash", "ChargeJump"], ["Bash", "Glide"], ["WallJump", "TripleJump"]]
        },
        "BelowGrottoTeleporterPlant": {
            "casual": [["DoubleJump", "ChargeFlame"], ["DoubleJump", "Grenade"], ["ChargeJump", "Glide", "ChargeFlame"], ["ChargeJump", "Glide", "Grenade"]],
            "standard": [["WallJump", "Glide", "ChargeFlame"], ["WallJump", "Glide", "Grenade"], ["Bash", "Grenade"], ["Glide", "ChargeFlame", ("HealthCell", 4)], ["Glide", "Grenade", ("HealthCell", 4)], ["ChargeJump", "ChargeFlame", ("HealthCell", 3)], ["ChargeJump", "Grenade", ("HealthCell", 3)], ["AirDash", "ChargeFlame"], ["AirDash", "Grenade"]],
            "expert": [["WallJump", "ChargeFlame", ("HealthCell", 6)], ["WallJump", "Grenade", ("HealthCell", 6)], ["ChargeDash"]],
            "master": [["Glide", "ChargeFlame"], ["Glide", "Grenade"]]
        }
    },
    "Iceless": {
        "IcelessExp": {
            "casual": [["Free"]]
        }
    },
    "MoonGrottoSwampAccessArea": {
        "GrottoSwampDrainAccessExp": {
            "casual": [["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["ChargeJump", "DoubleJump"], ["Bash", "DoubleJump", "Glide"]],
            "expert": [["ChargeDash"], ["DoubleBash"]]
        },
        "GrottoSwampDrainAccessPlant": {
            "casual": [["Stomp", "ChargeFlame", "WallJump", "DoubleJump"], ["Stomp", "ChargeFlame", "ChargeJump", "Glide"], ["Stomp", "ChargeFlame", "ChargeJump", "DoubleJump"], ["Stomp", "ChargeFlame", "ChargeJump", "Climb"], ["Stomp", "Grenade"]],
            "standard": [["Lure", "Grenade"], ["Lure", "ChargeFlame", "Bash"], ["ChargeFlame", "WallJump", ("HealthCell", 4)], ["ChargeFlame", "ChargeJump", ("HealthCell", 4)], ["ChargeFlame", "DoubleJump", ("HealthCell", 4)], ["ChargeFlame", "Glide", ("HealthCell", 4)], ["ChargeFlame", "Glide", "AirDash"], ["ChargeFlame", "WallJump", "AirDash"]],
            "expert": [["ChargeDash"]]
        }
    },
    "SideFallCell": { 
        "GrottoHideoutFallAbilityCell": {
            "casual": [["Free"]]
        }
    },
    "GumoHideout": { 
        "GumoHideoutMap": {
            "casual": [[("MapStone", 9)], [("GrottoMapStone", 1)]]
        },
        "GumoHideoutMapEvent": {
            "casual": [["Free"]]
        },
        "GumoHideoutMapstone": {
            "casual": [["WallJump"], ["DoubleJump"], ["Climb", "ChargeJump"], ["Climb", "Bash", "Grenade"], ["Glide"]], 
            "standard": [["Bash", "Grenade"], ["Climb"], ["ChargeJump", ("HealthCell", 4)], ["AirDash"]]
        },
        "GumoHideoutMiniboss": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["Lure", "Bash"]], 
            "master": [["DoubleJump"]]
        },
        "GumoHideoutEnergyCell": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"], ["WallJump", "Dash"], ["Climb", "Dash"]]
        },
        "GumoHideoutCrusherExp": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["DoubleJump"]]
        },
        "GumoHideoutCrusherKeystone": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump", ("HealthCell", 3)], ["Bash", "Grenade", ("HealthCell", 3)]], 
            "expert": [["DoubleJump"]]
        }
    },
    "DoubleJumpKeyDoor": {
    },
    "DoubleJumpKeyDoorOpened": { 
        "DoubleJumpSkillTree": {
            "casual": [["WallJump"], ["Glide"], ["DoubleJump"], ["Climb", "Bash", "Grenade"], ["Climb", "ChargeJump"], ["Climb", ("HealthCell", 3)], ["Bash", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 3)]], 
            "standard": [["Dash", ("HealthCell", 3)], ["AirDash"]], 
            "expert": [["Climb"], ["Bash", "Grenade"]]
        },
        "DoubleJumpAreaExp": {
            "casual": [["Bash", "Climb", "Grenade"], ["Bash", "DoubleJump"], ["Bash", "Glide"], ["Bash", "WallJump", "CleanWater"], ["ChargeJump", "Climb"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["ChargeJump", "WallJump", "CleanWater"], ["Climb", "DoubleJump"], ["DoubleJump", "WallJump"], ["Bash", "Grenade", ("HealthCell", 3)], ["Bash", "CleanWater", ("HealthCell", 3)], ["Bash", "WallJump", ("HealthCell", 2)], ["ChargeJump", "WallJump", ("HealthCell", 2)], ["ChargeJump", "CleanWater", ("HealthCell", 3)]], 
            "standard": [["ChargeJump", "WallJump"], ["Bash", ("HealthCell", 4)], ["Bash", ("AbilityCell", 3), ("EnergyCell", 1), ("HealthCell", 3)], ["Bash", "Dash", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 4)], ["ChargeJump", ("AbilityCell", 3), ("EnergyCell", 1), ("HealthCell", 3)], ["ChargeJump", "Dash", ("HealthCell", 3)], ["Bash", "AirDash"], ["ChargeJump", "AirDash"]], 
            "expert": [["Bash", "Climb", "CleanWater"], ["Bash", "Grenade"], ["Bash", "Climb", ("HealthCell", 2)], ["ChargeDash", ("EnergyCell", 1)]], 
            "master": [["DoubleJump"]]
        }
    },
    "LeftGumoHideout": { 
        "LeftGumoHideoutUpperPlant": {
            "casual": [["Grenade"], ["WallJump", "ChargeFlame"], ["Climb", "ChargeFlame"], ["ChargeJump", "ChargeFlame"], ["DoubleJump", "ChargeFlame"]], 
            "expert": [["ChargeFlame"], ["WallJump", "ChargeDash"], ["Climb", "ChargeDash"], ["ChargeJump", "ChargeDash"]]
        },
        "FarLeftGumoHideoutExp": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "ChargeJump"], ["Climb", "DoubleJump", "Glide"]], 
            "standard": [["Climb", "Bash", "Grenade"], ["WallJump", "AirDash"], ["Climb", "AirDash"]], 
            "master": [["Bash"]]
        }
    },
    "LowerLeftGumoHideout": { 
        "LeftGumoHideoutLowerPlant": {
            "casual": [["Grenade"], ["ChargeFlame"]], 
            "expert": [["ChargeDash"]]
        },
        "GumoHideoutLeftHangingExp": {
            "casual": [["Free"]]
        },
        "GumoHideoutRightHangingExp": {
            "casual": [["WallJump", "Glide"], ["Climb", "Glide"], ["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Glide", "Wind"]], 
            "standard": [["WallJump", "Dash"], ["Climb", "Dash"]], 
            "expert": [["DoubleJump"], ["DoubleBash"]]
        },
        "LeftGumoHideoutExp": {
            "casual": [["WallJump", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["Climb", "DoubleJump"], ["DoubleBash"]], 
            "master": [["TripleJump"]]
        },
        "LeftGumoHideoutHealthCell": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["DoubleBash"], ["ChargeDash"]], 
            "master": [["TripleJump"]]
        },
        "LeftGumoHideoutSwim": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 3)]]
        }
    },
    "WaterVeinArea": { 
        "GumoHideoutRockfallExp": {
            "casual": [["Free"]]
        },
        "WaterVein": {
            "casual": [["Free"]]
        }
    },
    "GumoHideoutRedirectArea": { 
        "GumoHideoutRedirectAbilityCell": {
            "casual": [["Glide"], ["DoubleJump"], ["Climb", "ChargeJump"], ["WallJump", ("HealthCell", 3)], ["Climb", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 3)]], 
            "standard": [["Bash", "Grenade"], ["AirDash"]]
        },
        "GumoHideoutRedirectPlant": {
            "casual": [["WallJump", "ChargeFlame"], ["Climb", "ChargeFlame"], ["ChargeJump", "ChargeFlame"], ["WallJump", "Grenade"], ["Climb", "Grenade"], ["Bash", "Grenade"], ["ChargeJump", "Grenade"]], 
            "expert": [["WallJump", "ChargeDash"], ["Climb", "ChargeDash"], ["ChargeJump", "ChargeDash"]], 
            "master": [["DoubleJump", "ChargeDash"]]
        }
    },
    "GumoHideoutRedirectEnergyVault": { 
        "GumoHideoutRedirectEnergyCell": {
            "casual": [["WallJump"], ["Climb", "Glide"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]]
        },
        "GumoHideoutRedirectExp": {
            "casual": [["WallJump"], ["Climb", "Glide"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]]
        }
    },
    "SwampEntryArea": { 
        "SwampEntranceSwim": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 3)]]
        },
        "SwampEntrancePlant": {
            "casual": [["ChargeFlame", "WallJump"], ["ChargeFlame", "Climb"], ["ChargeFlame", "ChargeJump"], ["Grenade", "WallJump"], ["Grenade", "Climb"], ["Grenade", "Bash"], ["Grenade", "ChargeJump"]], 
            "expert": [["Grenade"], ["WallJump", "ChargeDash"], ["Climb", "ChargeDash"], ["ChargeJump", "ChargeDash"]]
        }
    },
    "Swamp": { 
        "SwampMap": {
            "casual": [[("MapStone", 9)], [("SwampMapStone", 1)]]
        },
        "SwampMapEvent": {
            "casual": [["Free"]]
        },
        "InnerSwampDrainExp": {
            "casual": [["CleanWater", "Climb", "ChargeJump"], ["CleanWater", "WallJump", "DoubleJump"], ["CleanWater", "Climb", "DoubleJump"], ["CleanWater", "WallJump", "Bash", "Grenade"], ["CleanWater", "Climb", "Bash", "Grenade"], ["CleanWater", "Glide", "Bash", "Grenade"], ["CleanWater", "DoubleJump", "Bash", "Grenade"], ["CleanWater", "DoubleJump", "Glide", "ChargeJump"], ["CleanWater", "WallJump", "Glide", "Stomp", "ChargeFlame"], ["CleanWater", "WallJump", "Glide", "Stomp", "Grenade"], ["CleanWater", "Climb", "Dash", "Glide"]], 
            "standard": [["CleanWater", "Bash", "Grenade", ("HealthCell", 4)]], 
            "expert": [["CleanWater", "WallJump", "Dash", "Glide"], ["CleanWater", "DoubleJump", "ChargeJump"], ["CleanWater", "WallJump", "AirDash"], ["CleanWater", "Climb", "ChargeFlame", "Stomp", "AirDash"], ["CleanWater", "Climb", "Grenade", "Stomp", "AirDash"], ["CleanWater", "Climb", "ChargeDash"]], 
            "master": [["CleanWater", "DoubleJump"], ["Lure", "CleanWater", "Bash"], ["Climb", "ChargeJump", ("HealthCell", 7), "UltraDefense"], ["TripleJump", ("HealthCell", 7), "UltraDefense"], ["Bash", ("HealthCell", 7), "UltraDefense"], ["WallJump", "Glide", "Stomp", "ChargeFlame", ("HealthCell", 7), "UltraDefense"], ["WallJump", "Glide", "Stomp", "Grenade", ("HealthCell", 7), "UltraDefense"], ["WallJump", "ChargeDash", ("HealthCell", 7), "UltraDefense"], ["Climb", "ChargeDash", ("HealthCell", 7), "UltraDefense"]]
        }
    },
    "SwampKeyDoorPlatform": { 
        "InnerSwampStompExp": {
            "casual": [["Stomp", "CleanWater"]], 
            "expert": [["ChargeJump", "Bash", "Grenade", "CleanWater"], ["Stomp", ("HealthCell", 3)], ["ChargeJump", "Bash", "Grenade", ("HealthCell", 3)], ["ChargeJump", "AirDash", ("HealthCell", 3)], ["ChargeJump", "AirDash", "CleanWater"]], 
            "master": [["Lure", "Bash", ("HealthCell", 3)], ["Lure", "Bash", "CleanWater"]]
        }
    },
    "SwampKeyDoorOpened": {
    },
    "SwampDrainlessArea": { 
        "SwampEntranceAbilityCell": {
            "casual": [["Free"]]
        }
    },
    "InnerSwampAboveDrainArea": {
    },
    "InnerSwampDrainBroken": { 
    },
    "InnerSwampSkyArea": { 
        "InnerSwampEnergyCell": {
            "casual": [["Free"]]
        }
    },
    "SwampWater": { 
        "InnerSwampHiddenSwimExp": {
            "casual": [["Free"]]
        },
        "InnerSwampSwimLeftKeystone": {
            "casual": [["Free"]]
        },
        "InnerSwampSwimRightKeystone": {
            "casual": [["WallJump", "ChargeJump"], ["WallJump", "Bash"], ["WallJump", "DoubleJump"], ["WallJump", "Glide"], ["Climb", "ChargeJump"], ["Climb", "Bash"], ["Climb", "DoubleJump"], ["Climb", "Glide"], ["WallJump", ("HealthCell", 3)], ["Climb", ("HealthCell", 3)]], 
            "standard": [["WallJump", "Dash"], ["Climb", "Dash"]], 
            "expert": [["DoubleJump"]]
        },
        "InnerSwampSwimMapstone": {
            "casual": [["Free"]]
        }
    },
    "RightSwamp": { 
        "StompSkillTree": {
            "casual": [["Free"]]
        },
        "StompAreaExp": {
            "casual": [["Stomp"], ["Bash"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["ChargeFlame"], ["ChargeDash", ("EnergyCell", 1)]], 
            "master": [["Grenade"]]
        },
        "StompAreaRoofExp": {
            "casual": [["ChargeJump"]], 
            "expert": [["DoubleBash"]]
        },
        "StompAreaGrenadeExp": {
            "casual": [["Grenade", "CleanWater", "Bash", "Stomp"], ["Grenade", "CleanWater", "Bash", "Glide"], ["Grenade", "CleanWater", "ChargeJump", "Stomp"], ["Grenade", "CleanWater", "ChargeJump", "Climb", "Glide"], ["Grenade", "CleanWater", "ChargeJump", ("HealthCell", 3)]], 
            "standard": [["Grenade", "CleanWater", "Bash", "DoubleJump"], ["Grenade", "CleanWater", "Bash", ("HealthCell", 3)]], 
            "expert": [["Grenade", "CleanWater", "ChargeDash", ("EnergyCell", 3)], ["Grenade", "CleanWater", "Stomp", "ChargeDash"], ["Grenade", "CleanWater", "Climb", "DoubleJump", "Stomp", "AirDash", ("HealthCell", 3)], ["Grenade", "CleanWater", "WallJump", "DoubleJump", "Stomp", ("HealthCell", 3)], ["Grenade", "Bash", ("HealthCell", 3)], ["Grenade", "ChargeJump", ("HealthCell", 4)], ["Grenade", "ChargeDash", ("HealthCell", 4), ("EnergyCell", 3)], ["Grenade", "Climb", "DoubleJump", "Stomp", "AirDash", ("HealthCell", 4)], ["Grenade", "WallJump", "DoubleJump", "Stomp", ("HealthCell", 4)], ["Grenade", "CleanWater", "DoubleBash"]], 
            "master": [["Grenade", "CleanWater", "DoubleJump", "Stomp", ("HealthCell", 5)], ["Grenade", "CleanWater", "TripleJump", "UltraDefense", ("HealthCell", 5)], ["Grenade", "DoubleJump", "Stomp", ("HealthCell", 4)], ["Grenade", "DoubleJump", ("HealthCell", 5)], ["CleanWater", "GrenadeJump"]]
        }
    },
    "HoruFields": {
    },
    "HoruFieldsPushBlock": { 
        "HoruFieldsPlant": {
            "casual": [["Bash", "ChargeFlame"], ["Bash", "Grenade"], ["ChargeJump", "Glide", "ChargeFlame"], ["ChargeJump", "Glide", "Grenade"], ["Climb", "ChargeJump", "ChargeFlame"], ["Climb", "ChargeJump", "Grenade"]], 
            "standard": [["ChargeJump", "DoubleJump", "ChargeFlame", "AirDash"], ["ChargeJump", "DoubleJump", "Grenade", "AirDash"]], 
            "expert": [["ChargeDash", ("EnergyCell", 3)]], 
            "master": [["Grenade", "DoubleJump"], ["Grenade", "Glide"], ["Grenade", "Dash"]]
        },
        "HoruFieldsEnergyCell": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"], ["ChargeJump", "DoubleJump", "Glide"]], 
            "standard": [["ChargeJump", "Glide", "AirDash"], ["ChargeJump", "DoubleJump", "AirDash"]], 
            "expert": [["ChargeDash", ("EnergyCell", 2)], ["DoubleBash"]], 
            "master": [["GrenadeJump"]]
        },
        "HoruFieldsHiddenExp": {
            "casual": [["Bash", "Grenade"], ["ChargeJump"]], 
            "standard": [["Bash"]], 
            "expert": [["ChargeDash"]]
        },
        "HoruFieldsAbilityCell": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["WallJump", "DoubleJump", "Bash"], ["Climb", "ChargeJump"]], 
            "expert": [["WallJump", "Bash", ("HealthCell", 5)]], 
            "master": [["Bash"], ["Glide", "TripleJump"], ["WallJump", "TripleJump"]]
        }
    },
    "HorufieldsHoruDoor": {
    },
    "HoruOuterDoor": {
    },
    "HoruInnerDoor": {
    },
    "HoruInnerEntrance": { 
        "HoruLavaDrainedLeftExp": {
            "casual": [["Open", "Bash"], ["Open", "ChargeJump"], ["Open", "DoubleJump", "Glide"]], 
            "standard": [["Open", "Dash", "DoubleJump"], ["Open", "AirDash", "Glide"]], 
            "expert": [["Open", "ChargeDash"]], 
            "master": [["Open", "TripleJump"]]
        },
        "HoruLavaDrainedRightExp": {
            "casual": [["Open", "Glide", "Bash"], ["Open", "Grenade", "Bash"], ["Open", "ChargeJump", "Glide"]], 
            "expert": [["Open", "ChargeDash"], ["Open", "DoubleBash"]], 
            "master": [["Open", "ChargeJump", "TripleJump"], ["Open", "Glide", "TripleJump"]]
        }
    },
    "HoruTeleporter": { 
        "HoruTeleporterExp": {
            "casual": [["Free"]]
        }
    },
    "HoruBasement": { 
        "DoorWarpExp": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        }
    },
    "HoruMapLedge": { 
        "HoruMap": {
            "casual": [[("MapStone", 9)], [("HoruMapStone", 1)]]
        },
        "HoruMapEvent": {
            "casual": [["Free"]]
        }
    },
    "L1OuterEntrance": {
    },
    "L1OuterDoor": {
    },
    "L1InnerDoor": {
    },
    "L1": { 
        "HoruL1": {
            "casual": [["Bash", "DoubleJump", "Stomp"], ["Glide", "Bash", "WallJump", "Stomp"], ["Glide", "Bash", "Climb", "Stomp"], ["Glide", "Bash", "Grenade", "Stomp"]], 
            "standard": [["Glide", "Bash", "ChargeJump", "Stomp"], ["AirDash", "Bash", "WallJump", "Stomp"], ["AirDash", "Bash", "Climb", "Stomp"], ["AirDash", "Bash", "ChargeJump", "Stomp"], ["AirDash", "Bash", "Grenade", "Stomp"]], 
            "expert": [["Glide", "Bash", "Stomp"], ["AirDash", "Bash", "Stomp"], ["ChargeDash", "Stomp", ("EnergyCell", 3)], ["ChargeDash", "Stomp", "DoubleJump", ("EnergyCell", 2)]], 
            "master": [["ChargeDash", "Stomp", "DoubleJump", ("EnergyCell", 1)], ["WallJump", "TripleJump", "Stomp", "UltraDefense", ("HealthCell", 4)], ["Climb", "TripleJump", "Stomp", "UltraDefense", ("HealthCell", 4), ("EnergyCell", 2)], ["Climb", "TripleJump", "Stomp", "UltraDefense", ("HealthCell", 5), ("EnergyCell", 1)], ["Climb", "TripleJump", "Stomp", "UltraDefense", ("HealthCell", 7)], ["Bash", "Stomp", ("HealthCell", 5)], ["ChargeJump", "Stomp", ("HealthCell", 5)]]
        }
    },
    "L2OuterEntrance": {
    },
    "L2OuterDoor": {
    },
    "L2InnerDoor": {
    },
    "L2": { 
        "HoruL2": {
            "casual": [["Stomp", "ChargeJump"], ["Stomp", "WallJump", "DoubleJump"], ["Stomp", "Bash", "Grenade"]], 
            "standard": [["Lure", "Stomp", "Bash", "DoubleJump"], ["Stomp", "WallJump", "AirDash"], ["Stomp", "Climb", "AirDash", "DoubleJump"]], 
            "expert": [["Stomp", "Climb", "DoubleJump", "Glide"], ["Stomp", "ChargeDash", ("EnergyCell", 1)], ["Stomp", "Climb", "AirDash"]], 
            "master": [["Stomp", "DoubleJump", "Glide"], ["Stomp", "DoubleJump", "AirDash"], ["Stomp", "TripleJump"]]
        }
    },
    "L3OuterEntrance": {
    },
    "L3OuterDoor": {
    },
    "L3InnerDoor": {
    },
    "L3": { 
        "HoruL3": {
            "casual": [["Stomp", "DoubleJump", "Bash"], ["Bash", "Glide", "WallJump", "Stomp"], ["Bash", "Glide", "Climb", "Stomp"]], 
            "standard": [["Bash", "Glide", "WallJump", "ChargeFlame"], ["Bash", "Glide", "Climb", "ChargeFlame"], ["ChargeFlame", "DoubleJump", "Bash"], ["Bash", "Climb", "ChargeJump"], ["Bash", "Grenade", "Stomp"], ["Bash", "Grenade", "ChargeFlame"], ["Bash", "AirDash", "Stomp"], ["Bash", "AirDash", "ChargeFlame"]], 
            "expert": [["Bash", "Grenade", "ChargeJump"], ["ChargeJump", "ChargeDash", "Climb", ("EnergyCell", 2)]], 
            "master": [["Bash", "Stomp"], ["Bash", "ChargeFlame"], ["ChargeJump", "ChargeDash", "Climb", "TripleJump", "Glide"], ["ChargeDash", "DoubleJump", "Stomp", ("EnergyCell", 2)], ["ChargeDash", ("EnergyCell", 7)], ["ChargeDash", "DoubleJump", "Glide", ("EnergyCell", 4)], ["ChargeDash", "Glide", ("EnergyCell", 6)], ["ChargeDash", "DoubleJump", "WallJump", ("EnergyCell", 6)], ["ChargeDash", "DoubleJump", "Climb", ("EnergyCell", 6)], ["ChargeDash", "Stomp", ("EnergyCell", 3)], ["Bash", "ChargeDash", ("EnergyCell", 1)], ["ChargeJump", "Climb", "DoubleJump", "Glide", ("HealthCell", 4)], ["ChargeDash", "Climb", "TripleJump", "Glide", "UltraDefense", ("EnergyCell", 2), ("HealthCell", 6)], ["ChargeDash", "Climb", "TripleJump", "Glide", "Stomp", "UltraDefense", ("EnergyCell", 1), ("HealthCell", 4)], ["ChargeJump", "Climb", "TripleJump", "UltraDefense", ("HealthCell", 3)], ["ChargeJump", "TripleJump", "Stomp", "UltraDefense", ("HealthCell", 3)], ["ChargeJump", "TripleJump", "ChargeFlame", "UltraDefense", ("HealthCell", 3)], ["GrenadeJump"]]
        }
    },
    "L4OuterEntrance": { 
    },
    "L4OuterDoor": {
    },
    "L4InnerDoor": {
    },
    "L4": {
    },
    "HoruL4LavaChasePeg": { 
        "HoruL4ChaseExp": {
            "casual": [["Free"]]
        }
    },
    "HoruL4CutscenePeg": { 
        "HoruL4": {
            "casual": [["Stomp"]]
        },
        "HoruL4LowerExp": {
            "casual": [["WallJump", "Stomp"], ["Bash", "Grenade", "Stomp"], ["ChargeJump", "Stomp"]], 
            "standard": [["Climb", "Stomp"]], 
            "expert": [["DoubleJump"], ["Bash", "Grenade"], ["ChargeJump", "Climb"], ["Glide"], ["AirDash", "Stomp"], ["ChargeDash", ("EnergyCell", 2)]], 
            "master": [["Dash", "Stomp"]]
        }
    },
    "R1OuterEntrance": {
    },
    "R1OuterDoor": {
    },
    "R1InnerDoor": {
    },
    "R1": { 
        "HoruR1HangingExp": {
            "casual": [["DoubleJump", "Glide"], ["DoubleJump", "WallJump"], ["DoubleJump", "Climb"], ["ChargeJump", "Climb"]], 
            "standard": [["Bash", "Grenade"], ["AirDash", "WallJump"], ["AirDash", "Climb"]], 
            "expert": [["DoubleJump"], ["Dash"], ["ChargeJump", ("HealthCell", 5)]], 
            "master": [["WallJump", "Glide"], ["ChargeJump", ("HealthCell", 4), "UltraDefense"]]
        }
    },
    "HoruR1MapstoneSecret": { 
        "HoruR1Mapstone": {
            "casual": [["Free"]]
        }
    },
    "HoruR1CutsceneTrigger": { 
        "HoruR1": {
            "casual": [["Free"]]
        },
        "HoruR1EnergyCell": {
            "casual": [["Climb", "ChargeJump"], ["Climb", "Bash", "Grenade"], ["Climb", "DoubleJump", "Glide"], ["WallJump", "DoubleJump"], ["WallJump", "Glide"]], 
            "standard": [["Bash", "Grenade"], ["WallJump", "AirDash"], ["Climb", "AirDash"]], 
            "expert": [["Climb", "Glide"], ["Climb", "DoubleJump"], ["Climb", "Dash"], ["WallJump", "Dash"], ["WallJump", ("HealthCell", 5)], ["Climb", ("HealthCell", 5)]], 
            "master": [["DoubleJump"], ["WallJump", ("HealthCell", 4), "UltraDefense"], ["Climb", ("HealthCell", 4), "UltraDefense"]]
        }
    },
    "R2OuterEntrance": {
    },
    "R2OuterDoor": {
    },
    "R2InnerDoor": {
    },
    "R2": { 
        "HoruR2": {
            "casual": [["Stomp", "Bash", "Glide", "DoubleJump", "WallJump"], ["Stomp", "Bash", "Glide", "DoubleJump", "Climb"], ["Stomp", "Bash", "Glide", "DoubleJump", "ChargeJump"], ["Stomp", "Bash", "Glide", "Grenade"]], 
            "standard": [["Stomp", "Bash", "Glide", "WallJump"], ["Stomp", "Bash", "Glide", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump"]], 
            "expert": [["Stomp", "Climb"], ["Stomp", "WallJump"], ["Stomp", "ChargeJump"], ["Stomp", "Bash", "Grenade"]], 
            "master": [["Stomp", "DoubleJump"]]
        }
    },
    "R3OuterEntrance": {
    },
    "R3OuterDoor": {
    },
    "R3InnerDoor": {
    },
    "R3": {
    },
    "HoruR3ElevatorLever": {
    },
    "HoruR3PlantCove": { 
        "HoruR3Plant": {
            "casual": [["Grenade"]], 
            "standard": [["ChargeFlame"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "HoruR3CutsceneTrigger": { 
        "HoruR3": {
            "casual": [["Free"]]
        }
    },
    "R4OuterEntrance": { 
    },
    "R4OuterDoor": {
    },
    "R4InnerDoor": {
    },
    "R4": { 
    },
    "HoruR4StompHideout": { 
        "HoruR4StompExp": {
            "casual": [["Free"]]
        }
    },
    "HoruR4PuzzleEntrance": { 
    },
    "HoruR4CutsceneTrigger": { 
        "HoruR4": {
            "casual": [["Free"]]
        },
        "HoruR4DrainedExp": {
            "casual": [["DoubleJump", "Glide"], ["ChargeJump", "Climb"]], 
            "standard": [["Bash", "Grenade", "Climb"], ["Glide", "AirDash"], ["DoubleJump", "AirDash"]], 
            "expert": [["Bash", "Grenade"], ["Glide", ("HealthCell", 6)], ["DoubleJump", ("HealthCell", 6)], ["AirDash", ("HealthCell", 6)], ["ChargeDash", ("EnergyCell", 1)], ["DoubleBash"]], 
            "master": [[("HealthCell", 11)], [("HealthCell", 9), "UltraDefense"], ["TripleJump"]]
        },
        "HoruR4LaserExp": {
            "casual": [["Bash", "Grenade"], ["ChargeJump"], ["WallJump", "DoubleJump"], ["Climb", "DoubleJump"]], 
            "expert": [["DoubleJump"], ["DoubleBash"]]
        }
    },
    "HoruEscapeOuterDoor": {
    },
    "HoruEscapeInnerDoor": {
        #"HoruEscape": {
        #    "casual": [["Bash", "Stomp", "ChargeJump", "Wind", "Glide", "DoubleJump"]]
        #}
    },
    "ValleyEntry": { 
        "ValleyEntryAbilityCell": {
            "casual": [["Free"]]
        }
    },
    "ValleyEntryTree": { 
        "ValleyEntryTreeExp": {
            "casual": [["Free"]]
        },
        "ValleyEntryGrenadeLongSwim": {
            "casual": [["Grenade", "CleanWater"]], 
            "master": [["Grenade", ("HealthCell", 14)], ["Grenade", "Bash", ("HealthCell", 13)], ["Grenade", ("HealthCell", 7), "UltraDefense"]]
        }
    },
    "ValleyEntryTreePlantAccess": { 
        "ValleyEntryTreePlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "ValleyPostStompDoor": { 
        "ValleyRightSwimExp": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 4)]]
        }
    },
    "ValleyTeleporter": {
    },
    "ValleyRight": {
    },
    "ValleyStomplessApproach": { 
        "ValleyRightBirdStompCell": {
            "casual": [["ChargeJump", "Climb"]], 
            "standard": [["Stomp", "WallJump"], ["Stomp", "Climb"], ["Stomp", "DoubleJump"]], 
            "insane": [["Bash"]]
        },
        "ValleyRightFastStomplessCell": {
            "casual": [["Glide", "Wind"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["Climb", "ChargeJump", ("HealthCell", 4)], ["WallJump", "ChargeJump", ("HealthCell", 4)], ["DoubleJump", "ChargeJump", ("HealthCell", 4)]], 
            "master": [["WallJump", "TripleJump", ("HealthCell", 5), "UltraDefense"], ["Climb", "TripleJump", ("HealthCell", 7), "UltraDefense"]]
        },
        "ValleyRightExp": {
            "casual": [["Bash"]], 
            "expert": [["ChargeJump", "WallJump", "DoubleJump", ("HealthCell", 4)], ["ChargeJump", "Climb", "DoubleJump", ("HealthCell", 4)]], 
            "master": [["WallJump", "TripleJump", ("HealthCell", 3)]]
        }
    },
    "ValleyStompless": { 
    },
    "ValleyMain": { 
        "GlideSkillFeather": {
            "casual": [["Free"]]
        }
    },
    "LowerValley": { 
        "LowerValleyMapstone": {
            "casual": [["WallJump"], ["Climb"], ["DoubleJump"], ["Bash"], ["ChargeJump"]], 
            "expert": [["ChargeDash"]], 
            "master": [["Free"]]
        },
        "LowerValleyExp": {
            "casual": [["Free"]]
        },
        "KuroPerchExp": {
            "casual": [["Glide", "Wind"]], 
            "expert": [["ChargeDash"], ["Climb", "ChargeJump", "DoubleJump"]], 
            "master": [["Lure", "Bash"], ["GrenadeJump"]]
        }
    },
    "LowerValleyPlantApproach": { 
        "ValleyMainPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "ValleyThreeBirdLever": { 
        "ValleyMainFACS": {
            "casual": [["Climb", "ChargeJump"]], 
            "expert": [["WallJump", "DoubleJump", "ChargeJump", "AirDash"], ["WallJump", "Glide", "Wind", "ChargeJump", "AirDash"], ["WallJump", "ChargeJump", "AirDash", ("HealthCell", 4)], ["DoubleBash"]]
        },
        "ValleyThreeBirdAbilityCell": {
            "casual": [["Glide", "Wind"], ["Bash"], ["Climb", "ChargeJump", "Glide"], ["Climb", "ChargeJump", "DoubleJump"]], 
            "expert": [["Dash", "DoubleJump"], ["ChargeDash"]], 
            "master": [["GrenadeJump"], ["TripleJump"]]
        }
    },
    "ValleyStompFloor": {
    },
    "ValleyForlornApproach": { 
        "ValleyForlornApproachMapstone": {
            "casual": [["Free"]]
        },
        "ValleyForlornApproachGrenade": {
            "casual": [["Grenade"]]
        },
        "ValleyMap": {
            "casual": [["Bash", ("MapStone", 9)], ["Bash", ("ValleyMapStone", 1)]], 
            "expert": [["ChargeFlame", "ChargeJump", ("MapStone", 9)], ["ChargeFlame", "DoubleJump", ("MapStone", 9)], ["Grenade", "ChargeJump", ("MapStone", 9)], ["Grenade", "DoubleJump", ("MapStone", 9)], ["ChargeFlame", "AirDash", ("MapStone", 9)], ["Grenade", "AirDash", ("MapStone", 9)], ["ChargeFlame", "ChargeJump", ("ValleyMapStone", 1)], ["ChargeFlame", "DoubleJump", ("ValleyMapStone", 1)], ["Grenade", "ChargeJump", ("ValleyMapStone", 1)], ["Grenade", "DoubleJump", ("ValleyMapStone", 1)], ["ChargeFlame", "AirDash", ("ValleyMapStone", 1)], ["Grenade", "AirDash", ("ValleyMapStone", 1)]]
        },
        "ValleyMapEvent": {
            "casual": [["Bash"]], 
            "expert": [["ChargeFlame", "ChargeJump"], ["ChargeFlame", "DoubleJump"], ["Grenade", "ChargeJump"], ["Grenade", "DoubleJump"], ["ChargeFlame", "AirDash"], ["Grenade", "AirDash"]]
        }
    },
    "OutsideForlornCliff": { 
        "OutsideForlornCliffExp": {
            "casual": [["WallJump"], ["Climb"], ["DoubleJump"], ["Glide"], ["Dash"], ["ChargeJump"], ["Bash"]]
        }
    },
    "OutsideForlorn": { 
        "OutsideForlornTreeExp": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["Bash"]]
        },
        "OutsideForlornWaterExp": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 4)], ["Stomp", ("HealthCell", 2)]], 
            "master": [["UltraDefense", ("HealthCell", 2)]]
        }
    },
    "ForlornOuterDoor": {
    },
    "ForlornInnerDoor": { 
        "ForlornEntranceExp": {
            "casual": [["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["ChargeJump", "DoubleJump"], ["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"], ["DoubleJump"], ["Glide", "Climb"], ["Glide", "WallJump"], ["ChargeJump"]], 
            "expert": [["WallJump", ("HealthCell", 4)]], 
            "master": [["WallJump", ("HealthCell", 3), "UltraDefense"], ["TripleJump"]], 
            "standard": [["Dash", "Climb"], ["Dash", "WallJump"]]
        }
    },
    "ForlornOrbPossession": { 
    },
    "ForlornGravityRoom": { 
        "ForlornHiddenSpiderExp": {
            "casual": [["Bash"], ["ChargeJump"]], 
            "expert": [["WallJump", "DoubleJump"], ["ChargeDash"]], 
            "master": [["TripleJump"]]
        },
        "ForlornKeystone1": {
            "casual": [["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump", "Bash"]], 
            "expert": [["Lure", "Bash"]]
        },
        "ForlornKeystone2": {
            "casual": [["Bash", "Grenade"], ["ChargeJump"], ["WallJump", "DoubleJump", "Glide"], ["Climb", "DoubleJump", "Glide"]], 
            "standard": [["Dash", "DoubleJump", "WallJump"], ["Dash", "DoubleJump", "Climb"], ["Dash", "Glide", "WallJump"], ["Dash", "Glide", "Climb"]], 
            "master": [["Lure", "Bash"], ["TripleJump"]]
        }
    },
    "ForlornMapArea": { 
        "ForlornMap": {
            "casual": [[("MapStone", 9)], [("ForlornMapStone", 1)]]
        },
        "ForlornMapEvent": {
            "casual": [["Free"]]
        },
        "ForlornKeystone4": {
            "casual": [["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "master": [["ChargeJump", "DoubleJump"], ["Bash", "Grenade", "DoubleJump"]]
        }
    },
    "ForlornTeleporter": { 
        "ForlornKeystone3": {
            "casual": [["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"], ["Bash", "Grenade", "Climb"]], 
            "standard": [["ChargeJump", "AirDash"], ["ChargeJump", ("HealthCell", 4)]], 
            "expert": [["ChargeDash", "Climb"], ["ChargeDash", "WallJump"]], 
            "master": [["Lure", "Bash"]]
        }
    },
    "ForlornPlantAccess": { 
        "ForlornPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "ForlornKeyDoor": {
    },
    "ForlornLaserRoom": { 
        "ForlornEscape": {
            "casual": [["WallJump"], ["Climb", "ChargeJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"]], 
            "master": [["Lure", "Bash"]]
        }
    },
    "ForlornStompDoor": {
    },
    "RightForlorn": { 
        "RightForlornHealthCell": {
            "casual": [["Free"]]
        },
        "RightForlornPlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "WilhelmLedge": { 
        "WilhelmExp": {
            "casual": [["Climb", "ChargeJump"], ["WallJump", "DoubleJump", "ChargeJump"], ["Bash", "Grenade", "Climb"], ["Bash", "Grenade", "WallJump", "DoubleJump"]], 
            "standard": [["Lure", "Bash", "WallJump"]], 
            "expert": [["Bash", "Climb"], ["Bash", "Grenade"], ["ChargeJump", ("HealthCell", 5)], ["DoubleBash"]], 
            "master": [["ChargeJump", ("HealthCell", 4), "UltraDefense"], ["WallJump", "TripleJump"]]
        }
    },
    "SorrowBashLedge": {
    },
    "LowerSorrow": { 
        "SorrowEntranceAbilityCell": {
            "casual": [["Free"]]
        },
        "SorrowSpikeKeystone": {
            "casual": [["Glide"], ["Bash", "DoubleJump", "WallJump"], ["Bash", "DoubleJump", "Climb"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"], ["ChargeJump", "DoubleJump", "WallJump"], ["ChargeJump", "DoubleJump", "Climb"]],
            "standard": [["Dash", "DoubleJump", "WallJump"], ["Dash", "DoubleJump", "Climb"]],
            "expert": [["Climb", "ChargeJump", ("HealthCell", 5)], ["Climb", "DoubleJump", ("HealthCell", 5)], ["WallJump", "DoubleJump", ("HealthCell", 5)], ["WallJump", "ChargeJump", ("HealthCell", 5)], ["ChargeDash"], ["DoubleBash"]],
            "master": [["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["WallJump", "TripleJump"], ["Climb", "TripleJump"], ["GrenadeJump"]]
        },
        "SorrowHiddenKeystone": {
            "casual": [["Glide"], ["Bash", "ChargeJump", "DoubleJump", "WallJump"], ["Bash", "ChargeJump", "Climb"]], 
            "standard": [["Bash", "Dash", "DoubleJump", "WallJump"], ["Bash", "Dash", "DoubleJump", "Climb"]], 
            "expert": [["Bash", "ChargeJump", "WallJump"], ["Bash", "WallJump", ("HealthCell", 5)], ["Bash", "Climb", ("HealthCell", 5)], ["ChargeDash"], ["DoubleBash"]], 
            "master": [["GrenadeJump"]]
        },
        "SorrowHealthCell": {
            "casual": [["Glide", "Bash", "ChargeJump"]], 
            "standard": [["Bash", "ChargeJump", "WallJump"], ["Bash", "ChargeJump", "Climb"]], 
            "expert": [["ChargeJump", "Climb"], ["ChargeJump", "WallJump", "DoubleJump", ("HealthCell", 5)], ["Lure", "Glide", "Stomp", "ChargeJump"], ["Lure", "Glide", "Stomp", "Bash", "Grenade"], ["Lure", "Glide", "Stomp", "Climb", "DoubleJump"], ["Lure", "Glide", "Stomp", "WallJump", "DoubleJump"], ["Lure", "Glide", "Stomp", "ChargeDash", ("EnergyCell", 2)], ["DoubleBash"]], 
            "master": [["Lure", "Glide", "Stomp", "Climb"], ["Lure", "Glide", "Stomp", "WallJump"], ["Lure", "Glide", "Stomp", "DoubleJump"]]
        },
        "SorrowLowerLeftKeystone": {
            "casual": [["Glide"]], 
            "expert": [["Bash", "DoubleJump"], ["ChargeDash", "Stomp"], ["ChargeDash", "Bash"], ["ChargeDash", "DoubleJump"], ["ChargeDash", ("EnergyCell", 2)]], 
            "master": [["GrenadeJump"], ["Bash"], ["TripleJump"], ["ChargeJump", ("HealthCell", 10), "UltraDefense"]]
        }
    },
    "SorrowMainShaftKeystoneArea": { 
        "SorrowMainShaftKeystone": {
            "casual": [["Free"]]
        }
    },
    "SorrowMapstoneArea": { 
        "SorrowMapstone": {
            "casual": [["Bash"]], 
            "expert": [["ChargeDash"]], 
            "master": [["GrenadeJump"]]
        },
        "SorrowMap": {
            "casual": [["Stomp", ("MapStone", 9)], ["Bash", ("MapStone", 9)], ["Stomp", ("SorrowMapStone", 1)], ["Bash", ("SorrowMapStone", 1)]], 
            "standard": [["Lure", ("MapStone", 9)], ["Lure", ("SorrowMapStone", 1)]]
        },
        "SorrowMapEvent": {
            "casual": [["Stomp"], ["Bash"]], 
            "standard": [["Lure"]]
        }
    },
    "LeftSorrowLowerDoor": {
    },
    "LeftSorrow": { 
        "LeftSorrowAbilityCell": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["ChargeJump", "Climb", "DoubleJump"], ["ChargeJump", "Glide"], ["Bash", "Glide"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "expert": [["ChargeJump", "WallJump", ("HealthCell", 5)], ["ChargeJump", "Climb", ("HealthCell", 5)]], 
            "master": [["ChargeJump", "WallJump", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "Climb", ("HealthCell", 4), "UltraDefense"], ["TripleJump", "WallJump"], ["TripleJump", "Climb"], ["Bash"]]
        },
        "LeftSorrowGrenade": {
            "casual": [["Grenade", "Bash", "WallJump"], ["Grenade", "Bash", "Climb"], ["Grenade", "Bash", "Glide"], ["Grenade", "ChargeJump", "WallJump", "DoubleJump"], ["Grenade", "ChargeJump", "Climb", "DoubleJump"]], 
            "expert": [["Grenade", "DoubleBash"]]
        },
        "LeftSorrowPlant": {
            "casual": [["ChargeFlame", "WallJump", "DoubleJump"], ["ChargeFlame", "ChargeJump"], ["ChargeFlame", "Bash"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "LeftSorrowKeystones": { 
        "LeftSorrowKeystone1": {
            "casual": [["Glide"], ["DoubleJump"], ["Bash", "Grenade"], ["ChargeJump", "Climb"]], 
            "standard": [["Lure", "Bash"], ["Dash"]], 
            "expert": [["ChargeJump", "WallJump"]]
        },
        "LeftSorrowKeystone2": {
            "casual": [["Glide"], ["ChargeJump", "Climb"], ["Bash", "Grenade"]], 
            "expert": [["ChargeJump", "WallJump"]], 
            "master": [["Bash"]]
        },
        "LeftSorrowKeystone3": {
            "casual": [["Glide"]], 
            "expert": [["ChargeJump", "Climb", ("HealthCell", 5)]], 
            "master": [["Bash"], ["ChargeJump", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "LeftSorrowKeystone4": {
            "casual": [["Glide"]], 
            "expert": [["ChargeJump", "Climb", "DoubleJump", ("HealthCell", 5)], ["ChargeJump", "Climb", "Dash", ("HealthCell", 5)]], 
            "master": [["Bash"], ["ChargeJump", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "LeftSorrowEnergyCell": {
            "casual": [["Glide"]], 
            "expert": [["ChargeJump", "Climb", "DoubleJump", ("HealthCell", 5)]], 
            "master": [["Bash"], ["ChargeJump", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        }
    },
    "LeftSorrowMiddleDoorClosed": {
    },
    "LeftSorrowMiddleDoorOpen": {
    },
    "MiddleSorrow": {
    },
    "UpperSorrow": { 
        "UpperSorrowRightKeystone": {
            "casual": [["Glide"]], 
            "expert": [["ChargeJump", "ChargeDash", ("HealthCell", 5)]], 
            "master": [["ChargeJump", ("HealthCell", 10), "UltraDefense"], ["ChargeJump", "TripleJump", ("HealthCell", 7), "UltraDefense"], ["ChargeJump", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "TripleJump", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "DoubleJump", "ChargeDash"]]
        },
        "UpperSorrowFarRightKeystone": {
            "casual": [["Glide"]], 
            "master": [["ChargeJump", "ChargeDash", ("HealthCell", 7), "UltraDefense"], ["ChargeJump", "TripleJump", ("HealthCell", 10), "UltraDefense"], ["Bash", "Grenade", "TripleJump", ("HealthCell", 7), "UltraDefense"], ["Bash", "Grenade", "TripleJump", "ChargeDash"]]
        },
        "UpperSorrowLeftKeystone": {
            "casual": [["Glide"]], 
            "expert": [["Bash", "Grenade"], ["ChargeJump", ("HealthCell", 5)], ["ChargeDash", ("EnergyCell", 2)]], 
            "master": [["GrenadeJump"], ["ChargeJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "UpperSorrowSpikeExp": {
            "casual": [["Glide"]], 
            "expert": [["Bash", "Grenade", "DoubleJump", ("HealthCell", 5)], ["Bash", "Grenade", "ChargeDash", ("HealthCell", 5)], ["ChargeJump", "ChargeDash", ("HealthCell", 5)], ["ChargeDash", ("HealthCell", 5), ("EnergyCell", 2)]], 
            "master": [["ChargeJump", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["ChargeDash", ("HealthCell", 4), ("EnergyCell", 2), "UltraDefense"], ["Bash", "Grenade", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "UpperSorrowFarLeftKeystone": {
            "casual": [["Glide"]], 
            "master": [["ChargeJump", "TripleJump", "ChargeDash", "WallJump", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "TripleJump", "ChargeDash", "Climb", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "TripleJump", "ChargeDash", "WallJump", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "TripleJump", "ChargeDash", "Climb", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "ChargeJump", "TripleJump", "WallJump", ("HealthCell", 7), "UltraDefense"], ["Bash", "Grenade", "ChargeJump", "TripleJump", "Climb", ("HealthCell", 7), "UltraDefense"], ["ChargeJump", "TripleJump", "WallJump", ("HealthCell", 10), "UltraDefense"], ["ChargeJump", "TripleJump", "Climb", ("HealthCell", 10), "UltraDefense"]]
        }
    },
    "ChargeJumpDoor": {
    },
    "ChargeJumpDoorOpen": {
    },
    "ChargeJumpArea": { 
        "ChargeJumpSkillTree": {
            "casual": [["Free"]]
        }
    },
    "AboveChargeJumpArea": { 
        "AboveChargeJumpAbilityCell": {
            "casual": [["ChargeJump"], ["Bash", "WallJump"], ["Bash", "Climb"], ["Bash", "Grenade"]], 
            "expert": [["DoubleBash"], ["ChargeDash"]]
        }
    },
    "SorrowTeleporter": {
    },
    "BelowSunstoneArea": {
    },
    "SunstoneArea": { 
        "Sunstone": {
            "casual": [["Free"]]
        },
        "SunstonePlant": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "MistyEntrance": { 
        "MistyEntranceStompExp": {
            "casual": [["Stomp"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["ChargeJump", "Climb", "Dash"]], 
            "master": [["Dash", "ChargeFlame"], ["ChargeDash", ("EnergyCell", 2)]]
        },
        "MistyEntranceTreeExp": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["Bash"], ["ChargeDash"]], 
            "master": [["WallJump"], ["DoubleJump"]]
        }
    },
    "MistyPostFeatherTutorial": { 
        "MistyFrogNookExp": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["DoubleJump", "Glide", "Climb"], ["DoubleJump", "Bash", "Grenade"]], 
            "standard": [["Bash"], ["Climb", "ChargeJump"], ["WallJump", "DoubleJump", "AirDash"]], 
            "expert": [["WallJump", "AirDash", ("HealthCell", 3)], ["WallJump", "Dash", ("HealthCell", 7)], ["ChargeDash"]], 
            "master": [["DoubleJump", ("HealthCell", 4)], ["TripleJump"]]
        },
        "MistyKeystone1": {
            "casual": [["Free"]]
        }
    },
    "MistyPostKeystone1": {
    },
    "MistyPreMortarCorridor": { 
        "MistyMortarCorridorUpperExp": {
            "casual": [["Bash", "Glide"]], 
            "standard": [["Bash", "Grenade"]], 
            "expert": [["Bash", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4)], ["ChargeDash"]], 
            "master": [["Bash"], ["TripleJump"], ["GrenadeJump"]]
        },
        "MistyMortarCorridorHiddenExp": {
            "casual": [["Glide"]], 
            "expert": [["DoubleJump", "Bash"], ["DoubleJump", "ChargeDash"], ["DoubleJump", "ChargeJump", ("HealthCell", 4)], ["Bash", ("HealthCell", 7)], ["AirDash", ("HealthCell", 4)], ["Bash", "Grenade", ("HealthCell", 4)]], 
            "master": [["ChargeDash"], ["Bash"], ["TripleJump"], ["DoubleJump", ("HealthCell", 4)], [("HealthCell", 7), "UltraDefense"], [("HealthCell", 10)]]
        }
    },
    "MistyPostMortarCorridor": {
    },
    "MistyPrePlantLedge": { 
        "MistyPlant": {
            "casual": [["Grenade"], ["ChargeFlame"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "MistyPreClimb": { 
        "ClimbSkillTree": {
            "casual": [["Free"]]
        }
    },
    "MistyPostClimb": {
    },
    "MistySpikeCave": {
    },
    "MistyKeystone3Ledge": { 
        "MistyKeystone3": {
            "casual": [["Free"]]
        }
    },
    "MistyPreLasers": {
    },
    "MistyPostLasers": { 
        "MistyPostClimbSpikeCave": {
            "casual": [["Bash", "Glide", "DoubleJump"]], 
            "standard": [["Bash", "Glide"]], 
            "expert": [["Glide", ("HealthCell", 4)]], 
            "master": [["Bash", ("HealthCell", 4)], ["DoubleJump", ("HealthCell", 11)]]
        }
    },
    "MistyMortarSpikeCave": { 
        "MistyPostClimbAboveSpikePit": {
            "casual": [["WallJump", "Bash", "Glide"], ["Climb", "Bash", "Glide"]], 
            "expert": [["Bash", "DoubleJump"]], 
            "master": [["Bash"]]
        }
    },
    "MistyKeystone4Ledge": { 
        "MistyKeystone4": {
            "casual": [["Free"]]
        }
    },
    "MistyBeforeDocks": {
    },
    "MistyAbove200xp": { 
        "MistyGrenade": {
            "casual": [["Grenade"]]
        }
    },
    "MistyBeforeMiniBoss": {
    },
    "MistyOrbRoom": { 
        "GumonSeal": {
            "casual": [["WallJump"], ["Climb"], ["DoubleJump"], ["Bash"]]
        }
    },
    "MistyPreKeystone2": { 
        "MistyKeystone2": {
            "casual": [["Free"]]
        },
        "MistyAbilityCell": {
            "casual": [["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash"], ["WallJump", "DoubleJump", ("HealthCell", 4)]]
        }
    }
}

connection_rules: dict[str, dict[str, dict[str, list[list[str | tuple[str, int]]]]]] = {
    "TeleporterNetwork": { 
        "SunkenGladesRunaway": {
            "casual": [["TPGlades"]]
        },
        "SpiritTreeRefined": {
            "casual": [["TPGrove"]]
        },
        "MoonGrotto": {
            "casual": [["TPGrotto"]]
        },
        "SwampTeleporter": {
            "casual": [["TPSwamp"]]
        },
        "ValleyTeleporter": {
            "casual": [["TPValley"]]
        },
        "SorrowTeleporter": {
            "casual": [["TPSorrow"]]
        },
        "GinsoTeleporter": {
            "casual": [["TPGinso"]]
        },
        "ForlornTeleporter": {
            "casual": [["TPForlorn"]]
        },
        "HoruTeleporter": {
            "casual": [["TPHoru"]]
        },
        "BlackrootGrottoConnection": {
            "casual": [["TPBlackroot"]]
        }
    },
    "SunkenGladesRunaway": { 
        "GladesFirstKeyDoor": {
            "casual": [["Free"]]
        },
        "LowerChargeFlameArea": {
            "casual": [["None"]],
            "glitched": [["Grenade"]]
        },
        "BlackrootDarknessRoom": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        },
        "DeathGauntletDoor": {
            "casual": [["ChargeJump"], ["Grenade", "Bash"], ["WallJump", ("HealthCell", 3)], ["Climb", ("HealthCell", 3)]], 
            "standard": [["Lure", "Bash"]], 
            "master": [["DoubleJump"]]
        },
        "TeleporterNetwork": {
            "casual": [["Free"]]
        }
    },
    "GladesFirstKeyDoor": { 
        "GladesFirstKeyDoorOpened": {
            "casual": [[("KeyStone", 10)], [("GladesKeyStone", 2)], ["OpenWorld"]]
        }
    },
    "GladesFirstKeyDoorOpened": { 
        "GladesMain": {
            "casual": [["Free"]]
        },
        "SunkenGladesRunaway": {
            "casual": [["Free"]]
        }
    },
    "GladesMain": { 
        "GladesMainAttic": {
            "casual": [["Bash", "WallJump"], ["Bash", "Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "standard": [["WallJump", "DoubleJump"]], 
            "expert": [["Climb", "DoubleJump"], ["Bash"], ["ChargeDash"], ["DoubleBash"]], 
            "master": [["DoubleJump"]]
        },
        "LeftGlades": {
            "casual": [["Free"]]
        },
        "SpiritCavernsDoor": {
            "casual": [["Free"]]
        },
        "GladesLaserArea": {
            "casual": [["ChargeJump", "Climb"], ["ChargeJump", "WallJump", "DoubleJump"], ["Bash", "DoubleJump", "Glide"], ["Bash", "DoubleJump", "WallJump"], ["Bash", "DoubleJump", "Climb"], ["Bash", "Grenade", "Climb"], ["Bash", "Grenade", "WallJump"]], 
            "expert": [["Bash", "WallJump"], ["Bash", "Climb"], ["ChargeDash"], ["DoubleBash"]]
        },
        "LowerChargeFlameArea": {
            "casual": [["Grenade"], ["ChargeFlame"]], 
            "expert": [["ChargeDash"]]
        },
        "GladesFirstKeyDoor": {
            "casual": [["Open"]]
        }
    },
    "GladesMainAttic": { 
        "GladesMain": {
            "casual": [["Free"]]
        },
        "LowerChargeFlameArea": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        }
    },
    "LeftGlades": { 
        "GladesMain": {
            "casual": [["Free"]]
        },
        "UpperLeftGlades": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["DoubleJump"]]
        }
    },
    "UpperLeftGlades": { 
        "LeftGlades": {
            "casual": [["Free"]]
        }
    },
    "DeathGauntletDoor": { 
        "DeathGauntletDoorOpened": {
            "casual": [[("EnergyCell", 4)]], 
            "glitched": [[("EnergyCell", 3)]], 
            "timed-level": [[("EnergyCell", 2)]]
        }
    },
    "DeathGauntletDoorOpened": { 
        "SunkenGladesRunaway": {
            "casual": [["Free"]]
        },
        "DeathGauntlet": {
            "casual": [["Grenade", "Bash"], ["DoubleJump", "Bash"], ["Glide", "Bash"], ["Climb", "DoubleJump", "Glide"], ["WallJump", "DoubleJump", "Glide"], ["WallJump", "CleanWater"], ["Climb", "CleanWater"], ["Bash", "CleanWater"]], 
            "standard": [["WallJump", ("HealthCell", 4)], ["Climb", ("HealthCell", 4)], ["Bash", ("HealthCell", 4)]], 
            "expert": [["WallJump", ("HealthCell", 3)], ["Climb", ("HealthCell", 3)], ["Bash", ("HealthCell", 3)], ["ChargeDash", ("EnergyCell", 1)]], 
            "master": [["DoubleJump"]]
        },
        "DeathGauntletMoat": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 5)]], 
            "master": [[("HealthCell", 4)]]
        }
    },
    "DeathGauntletMoat": {
    },
    "DeathGauntlet": { 
        "DeathGauntletMoat": {
            "casual": [["CleanWater"]], 
            "expert": [[("HealthCell", 4)]], 
            "master": [[("HealthCell", 3)]]
        },
        "DeathGauntletDoor": {
            "casual": [["DoubleJump"], ["Glide"], ["Climb", "ChargeJump"]]
        },
        "DeathGauntletRoof": {
            "casual": [["ChargeJump"]]
        },
        "DeathGauntletRoofPlantAccess": {
            "casual": [["None"]],
            "expert": [["ChargeFlame", "DoubleJump", "WallJump"], ["ChargeFlame", "Bash", "WallJump"], ["ChargeFlame", "DoubleJump", "Climb"], ["ChargeFlame", "Bash", "Climb"], ["ChargeFlame", "Bash", "Grenade"]], 
            "master": [["ChargeFlame", "DoubleJump"], ["ChargeFlameBurn"]]
        },
        "MoonGrotto": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump"]], 
            "master": [["Lure", "Bash"], ["Lure", "ChargeDash", ("EnergyCell", 1)]]
        },
        "MoonGrottoAboveTeleporter": {
            "casual": [["None"]],
            "master": [["Lure", "Bash"]]
        }
    },
    "DeathGauntletRoof": { 
        "DeathGauntletRoofPlantAccess": {
            "casual": [["Free"]]
        },
        "DeathGauntlet": {
            "casual": [["Stomp"]], 
            "standard": [["Lure", "Free"]]
        }
    },
    "DeathGauntletRoofPlantAccess": {
    },
    "SpiritCavernsDoor": { 
        "SpiritCavernsDoorOpened": {
            "casual": [[("KeyStone", 36)], [("GladesKeyStone", 6)]]
        }
    },
    "SpiritCavernsDoorOpened": { 
        "LowerSpiritCaverns": {
            "casual": [["Climb"], ["WallJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["ChargeDash"]], 
            "master": [["DoubleJump"]]
        },
        "GladesMain": {
            "casual": [["Free"]]
        }
    },
    "LowerSpiritCaverns": { 
        "MidSpiritCaverns": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"], ["Bash", "DoubleJump"]], 
            "expert": [["Bash", "Dash"], ["DoubleBash"]], 
            "master": [["DoubleJump"]]
        },
        "GladesLaserArea": {
            "casual": [["Bash", ("EnergyCell", 4)]]
        },
        "SpiritCavernsDoor": {
            "casual": [["Open"]]
        }
    },
    "MidSpiritCaverns": { 
        "LowerSpiritCaverns": {
            "casual": [["Free"]]
        },
        "GladesLaserArea": {
            "casual": [[("EnergyCell", 4)]], 
            "glitched": [[("EnergyCell", 3)]]
        },
        "UpperSpiritCaverns": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"], ["DoubleJump", ("HealthCell", 3)]], 
            "standard": [["Bash"]]
        }
    },
    "UpperSpiritCaverns": { 
        "MidSpiritCaverns": {
            "casual": [["Free"]]
        },
        "SpiritTreeDoor": {
            "casual": [["Free"]]
        }
    },
    "SpiritTreeDoor": { 
        "SpiritTreeDoorOpened": {
            "casual": [[("KeyStone", 36)], [("GladesKeyStone", 8)]]
        }
    },
    "SpiritTreeDoorOpened": { 
        "SpiritTreeRefined": {
            "casual": [["WallJump"], ["Climb"], ["Bash"], ["ChargeJump", ("HealthCell", 3)]], 
            "master": [["DoubleJump"]]
        },
        "UpperSpiritCaverns": {
            "casual": [["Free"]]
        }
    },
    "GladesLaserArea": { 
        "GladesMain": {
            "casual": [["Free"]]
        },
        "MidSpiritCaverns": {
            "casual": [["WallJump", ("EnergyCell", 4)], ["Climb", ("EnergyCell", 4)], ["ChargeJump", ("EnergyCell", 4)], ["Bash", "Grenade", ("EnergyCell", 4)], ["DoubleJump", ("EnergyCell", 4)]], 
            "expert": [["Dash", ("EnergyCell", 4)], ["DoubleBash", ("EnergyCell", 4)]], 
            "timed-level": [["WallJump", ("EnergyCell", 2)], ["Climb", ("EnergyCell", 2)], ["ChargeJump", ("EnergyCell", 2)], ["Bash", ("EnergyCell", 2)], ["DoubleJump", ("EnergyCell", 2)], ["Dash", ("EnergyCell", 2)]]
        }
    },
    "ChargeFlameSkillTreeChamber": { 
        "SpiritTreeRefined": {
            "casual": [["ChargeJump"]]
        },
        "ChargeFlameAreaStump": {
            "casual": [["ChargeJump"], ["Grenade"], ["ChargeFlame"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "ChargeFlameAreaStump": { 
        "ChargeFlameAreaPlantAccess": {
            "casual": [["Free"]]
        },
        "ChargeFlameSkillTreeChamber": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Grenade"], ["ChargeFlame"]], 
            "standard": [["Stomp"]], 
            "expert": [["ChargeDash"]], 
            "master": [["DoubleJump"]]
        },
        "LowerChargeFlameArea": {
            "casual": [["Free"]]
        }
    },
    "ChargeFlameAreaPlantAccess": {
    },
    "LowerChargeFlameArea": { 
        "GladesMain": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "standard": [["Stomp"]], 
            "expert": [["ChargeDash"]]
        },
        "ChargeFlameAreaStump": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"], ["Lure", "Bash", "Stomp"], ["Lure", "Bash", "ChargeFlame"], ["Lure", "Bash", "ChargeDash"]]
        }
    },
    "SpiritTreeRefined": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "SpiritTreeDoor": {
            "casual": [["Open"]]
        },
        "ChargeFlameSkillTreeChamber": {
            "casual": [["Free"]]
        },
        "ChargeFlameAreaStump": {
            "casual": [["Free"]]
        },
        "ValleyEntry": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "standard": [["Stomp", "WallJump"], ["Stomp", "Climb"], ["Stomp", "DoubleJump"], ["Stomp", "ChargeJump"]], 
            "expert": [["ChargeDash"]]
        },
        "SpiderSacArea": {
            "casual": [["ChargeFlame", "WallJump"], ["ChargeFlame", "ChargeJump"], ["ChargeFlame", "Climb", "DoubleJump"], ["ChargeFlame", "Climb", "Glide"], ["ChargeFlame", "Climb", "Dash"], ["Grenade", "WallJump"], ["Grenade", "ChargeJump"], ["Grenade", "Climb", "DoubleJump"], ["Grenade", "Climb", "Glide"], ["Grenade", "Climb", "Dash"], ["Grenade", "Bash"]], 
            "expert": [["ChargeFlame", "Climb"], ["Grenade", "Climb"], ["ChargeDash", "Climb"], ["ChargeDash", "WallJump"]], 
            "master": [["ChargeFlame", "DoubleJump"], ["Grenade", "DoubleJump"], ["ChargeDash", "DoubleJump"]]
        }
    },
    "SpiderSacTetherArea": { 
        "SpiderWaterArea": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash", "ChargeJump"], ["ChargeDash", "Bash", "Grenade"]]
        },
        "SpiderSacEnergyNook": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash", "ChargeJump"], ["ChargeDash", "Bash", "Grenade"]]
        }
    },
    "SpiderSacArea": { 
        "SpiderSacTetherArea": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        },
        "SpiderWaterArea": {
            "casual": [["DoubleJump"], ["Glide"]], 
            "expert": [["AirDash"]]
        },
        "SpiderSacEnergyNook": {
            "casual": [["DoubleJump"], ["Glide"]], 
            "expert": [["AirDash"]]
        },
        "SpiritTreeRefined": {
            "casual": [["ChargeFlame", "WallJump"], ["ChargeFlame", "Climb"], ["ChargeFlame", "ChargeJump"], ["Grenade", "WallJump"], ["Grenade", "Climb"], ["Grenade", "ChargeJump"], ["Grenade", "Bash"]], 
            "standard": [["Stomp", "WallJump"], ["Stomp", "Climb"], ["Stomp", "ChargeJump"]], 
            "master": [["ChargeFlame", "DoubleJump"], ["Grenade", "DoubleJump"], ["Stomp", "DoubleJump"]]
        }
    },
    "SpiderSacEnergyNook": { 
        "ChargeFlameAreaPlantAccess": {
            "casual": [["None"]],
            "master": [["ChargeFlameBurn"]]
        }
    },
    "SpiderWaterArea": { 
        "SpiderSacEnergyNook": {
            "casual": [["Glide"], ["Bash", "Grenade"], ["WallJump", "DoubleJump"], ["Climb", "DoubleJump"]], 
            "standard": [["Dash", "DoubleJump"], ["Bash", "DoubleJump"]], 
            "expert": [["DoubleJump"], ["DoubleBash"], ["AirDash"]], 
            "master": [["GrenadeJump"]]
        },
        "SpiderSacArea": {
            "casual": [["DoubleJump", "WallJump"], ["DoubleJump", "Climb"], ["Bash", "WallJump", "Glide"], ["Bash", "Climb", "Glide"]], 
            "standard": [["Dash", "WallJump", "Glide"], ["Dash", "Climb", "Glide"], ["Bash", "WallJump"], ["Bash", "Climb"]], 
            "expert": [["DoubleBash"], ["ChargeDash"]], 
            "master": [["ChargeJump", "Climb"]]
        },
        "HollowGrove": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["DoubleJump"], ["CleanWater"]], 
            "standard": [["Bash"]], 
            "master": [["ChargeDash"]]
        },
        "DeathGauntletRoof": {
            "casual": [["WallJump", "Stomp", "CleanWater"], ["Climb", "Stomp", "CleanWater"], ["Bash", "Stomp", "CleanWater"]], 
            "expert": [["Bash", "Stomp", ("HealthCell", 4)], ["WallJump", "Stomp", ("HealthCell", 5)], ["Climb", "Stomp", ("HealthCell", 5)], ["DoubleJump", "Stomp", ("HealthCell", 5)]], 
            "master": [["WallJump", "Stomp", "UltraDefense", ("HealthCell", 3)], ["Climb", "Stomp", "UltraDefense", ("HealthCell", 3)], ["TripleJump", "Stomp", "UltraDefense", ("HealthCell", 3)]]
        }
    },
    "BlackrootDarknessRoom": { 
        "DashArea": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "expert": [["DoubleJump"]], 
            "master": [["Bash"]]
        }
    },
    "DashArea": { 
        "DashAreaMapstoneAccess": {
            "casual": [["Free"]]
        },
        "DashPlantAccess": {
            "casual": [["ChargeJump", "Climb"], ["ChargeJump", "WallJump"], ["Glide", "WallJump"], ["Bash", "Grenade"]], 
            "standard": [["WallJump", "DoubleJump", "AirDash"], ["Climb", "DoubleJump", "AirDash"]], 
            "expert": [["DoubleJump", "Grenade"], ["ChargeJump", "Grenade"], ["Glide", "Grenade"], ["ChargeJump", "ChargeFlame"], ["WallJump", "ChargeDash", ("EnergyCell", 2)], ["Climb", "ChargeDash", ("EnergyCell", 2)], ["WallJump", "ChargeFlame", "ChargeDash"], ["Climb", "ChargeFlame", "ChargeDash"], ["Grenade", "AirDash"]], 
            "master": [["DoubleJump", "Glide"], ["DoubleJump", "Dash"], ["Bash"], ["WallJump", "ChargeFlameBurn"], ["Climb", "ChargeFlameBurn"], ["DoubleJump", "ChargeFlameBurn"], ["TripleJump"]]
        },
        "GrenadeAreaAccess": {
            "casual": [["Stomp", "ChargeJump"], ["Stomp", "Grenade", "Bash"], ["Stomp", "Dash"]], 
            "standard": [["ChargeJump", "Climb"]], 
            "expert": [["Stomp"]], 
            "master": [["Bash"]], 
            "glitched": [["Free"]], 
            "insane": [["Free"]]
        },
        "RazielNoArea": {
            "casual": [["Dash", "WallJump"], ["Dash", "ChargeJump"], ["Dash", "Bash", "Grenade"], ["Dash", "Climb", "DoubleJump"]], 
            "standard": [["Bash", "Grenade"], ["WallJump", "Rekindle"], ["ChargeJump", "Rekindle"], ["Climb", "DoubleJump", "Rekindle"], ["Climb", "AirDash"]], 
            "expert": [["Climb", "Rekindle"]], 
            "master": [["DoubleJump", "Rekindle"]]
        }
    },
    "DashAreaMapstoneAccess": {
    },
    "DashPlantAccess": { 
        "DashAreaMapstoneAccess": {
            "casual": [["Free"]]
        }
    },
    "RazielNoArea": { 
        "BlackrootGrottoConnection": {
            "casual": [["Dash", "WallJump"], ["Dash", "Climb", "DoubleJump"], ["Dash", "Bash", "Grenade"], ["Dash", "ChargeJump"]], 
            "standard": [["ChargeJump", "Climb"], ["ChargeJump", "WallJump"], ["Bash", "Grenade"]], 
            "expert": [["WallJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["AirDash", "Climb", ("HealthCell", 3)]], 
            "glitched": [["Climb"]]
        },
        "GumoHideout": {
            "casual": [["None"]],
            "glitched": [["Dash", "WallJump"], ["Dash", "Climb", "DoubleJump"], ["Dash", "Bash", "Grenade"], ["Dash", "ChargeJump"]]
        }
    },
    "BlackrootGrottoConnection": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "SideFallCell": {
            "casual": [["Stomp", "WallJump"], ["Stomp", "Climb", "DoubleJump"], ["Stomp", "Bash", "Grenade"], ["Stomp", "ChargeJump"]], 
            "standard": [["Stomp", "Climb", "AirDash"]], 
            "expert": [["Stomp", "Climb"]]
        }
    },
    "GrenadeAreaAccess": { 
        "GrenadeArea": {
            "casual": [["Dash"]], 
            "expert": [["Bash", "Grenade"], ["DoubleJump"]], 
            "master": [["GrenadeJump"]], 
            "glitched": [["Free"]], 
            "insane": [["Free"]]
        },
        "LowerBlackroot": {
            "casual": [["DoubleJump"], ["Climb", "ChargeJump"], [("HealthCell", 3)]], 
            "standard": [["Bash", "Grenade"]], 
            "expert": [["AirDash"], ["DoubleBash"]]
        }
    },
    "GrenadeArea": {
    },
    "LowerBlackroot": { 
        "LostGrove": {
            "casual": [["WallJump", "Grenade"], ["Climb", "Grenade"], ["ChargeJump", "Grenade"], ["Bash", "Grenade"]], 
            "expert": [["DoubleJump", "Grenade"]]
        }
    },
    "LostGrove": { 
        "LostGroveExit": {
            "casual": [["Grenade", "Bash", "DoubleJump", "WallJump"], ["Grenade", "Bash", "DoubleJump", "Climb"], ["Grenade", "ChargeJump", "DoubleJump", "WallJump", ("HealthCell", 3)], ["Grenade", "ChargeJump", "DoubleJump", "Climb", ("HealthCell", 3)]], 
            "expert": [["Grenade", "Bash", "WallJump"], ["Grenade", "Bash", "Climb"], ["Grenade", "Glide", "ChargeJump", "Climb"], ["Grenade", "ChargeJump", "WallJump", ("HealthCell", 7)], ["Grenade", "ChargeJump", "Climb", ("HealthCell", 7)], ["Grenade", "Dash", "ChargeJump", "WallJump", ("HealthCell", 3)], ["Grenade", "Glide", "ChargeJump", "WallJump", ("HealthCell", 3)], ["Grenade", "AirDash", "ChargeJump", "Climb"]], 
            "master": [["Grenade", "TripleJump", "WallJump"], ["Grenade", "TripleJump", "Climb"], ["GrenadeJump"]]
        }
    },
    "LostGroveExit": { 
        "LostGrove": {
            "casual": [["BashGrenade"], ["Grenade", "WallJump", "DoubleJump", "Glide"], ["Grenade", "Climb", "DoubleJump", "Glide"], ["Dash", "WallJump"], ["Dash", "Climb"], ["Dash", "ChargeJump"]], 
            "standard": [["Grenade", "Glide", "WallJump", ("HealthCell", 3)], ["Grenade", "Glide", "Climb", ("HealthCell", 3)], ["Grenade", "DoubleJump", "WallJump", ("HealthCell", 3)], ["Grenade", "DoubleJump", "Climb", ("HealthCell", 3)], ["Grenade", "Glide", "ChargeJump", ("HealthCell", 3)], ["Grenade", "DoubleJump", "ChargeJump", ("HealthCell", 3)]], 
            "expert": [["Grenade", "ChargeJump", ("HealthCell", 5)], ["Dash", "DoubleJump"]], 
            "master": [["GrenadeJump"], ["Grenade", "DoubleJump", ("HealthCell", 3)], ["Grenade", "TripleJump"]]
        }
    },
    "HollowGrove": { 
        "SpiderWaterArea": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["DoubleJump"], ["CleanWater"]], 
            "standard": [["Bash"]], 
            "master": [["Free"]]
        },
        "SwampTeleporter": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"], ["Wind", "Glide"]], 
            "master": [["DoubleJump"]]
        },
        "OuterSwampUpperArea": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"], ["Wind", "Glide"]], 
            "master": [["DoubleJump"]]
        },
        "HoruFields": {
            "casual": [["Bash"]], 
            "standard": [["WallJump", "Stomp"], ["Climb", "DoubleJump", "Stomp"], ["ChargeJump", "Stomp"], ["Climb", "Stomp", "AirDash"]], 
            "expert": [["WallJump"], ["ChargeJump"], ["Climb", "AirDash"]], 
            "master": [["DoubleJump"]]
        },
        "Iceless": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["ChargeDash"]], 
            "master": [["WallJump"], ["DoubleJump"]]
        },
        "MoonGrottoStompPlantAccess": {
            "casual": [["None"]],
            "master": [["Lure", "WallJump", ("HealthCell", 4)], ["Lure", "ChargeJump", ("HealthCell", 4)], ["Lure", "DoubleJump"], ["Lure", "WallJump", "Glide"], ["Lure", "ChargeDash"]]
        }
    },
    "SwampTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "HollowGrove": {
            "casual": [["Free"]]
        },
        "OuterSwampMortarAbilityCellLedge": {
            "casual": [["None"]],
            "glitched": [["Free"]]
        }
    },
    "OuterSwampUpperArea": { 
        "GinsoOuterDoor": {
            "casual": [["GinsoKey"]]
        },
        "OuterSwampAbilityCellNook": {
            "casual": [["Glide"], ["DoubleJump"]], 
            "standard": [["Free"]]
        },
        "OuterSwampLowerArea": {
            "casual": [["Free"]]
        },
        "OuterSwampSwarmLedge": {
            "standard": [["Free"]]
        },
        "SwampTeleporter": {
            "casual": [["Free"]]
        }
    },
    "OuterSwampAbilityCellNook": { 
        "InnerSwampSkyArea": {
            "glitched": [["Dash"]]
        }
    },
    "OuterSwampLowerArea": { 
        "OuterSwampSwarmLedge": {
            "casual": [["WallJump"], ["Climb"], ["Bash"], ["ChargeJump"], ["DoubleJump"], ["Glide", "Wind"]], 
            "expert": [["ChargeDash", ("EnergyCell", 1)]]
        },
        "OuterSwampAbilityCellNook": {
            "casual": [["Bash", "Grenade"], ["Glide", "Wind"]], 
            "standard": [["Bash"], ["WallJump"], ["Climb"]]
        },
        "OuterSwampUpperArea": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"], ["Glide", "Wind"]], 
            "expert": [["WallJump"], ["Climb"], ["ChargeDash", ("EnergyCell", 1)]]
        }
    },
    "OuterSwampSwarmLedge": { 
        "OuterSwampMortarPlantAccess": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["WallJump", "Glide"], ["Climb", "Glide"], ["Bash"], ["ChargeJump"]], 
            "standard": [["DoubleJump"], ["Glide"], ["AirDash"]], 
            "expert": [["Dash"]]
        },
        "OuterSwampMortarAbilityCellLedge": {
            "casual": [["ChargeJump", "DoubleJump"], ["Bash", "DoubleJump"], ["Bash", "Grenade"]], 
            "standard": [["ChargeJump"], ["Bash"]], 
            "expert": [["ChargeDash", ("EnergyCell", 1)]], 
            "master": [["WallJump", "TripleJump"]]
        },
        "UpperGrotto": {
            "casual": [["WallJump"], ["Climb"], ["Bash"], ["ChargeJump"]], 
            "expert": [["Free"]]
        },
        "OuterSwampLowerArea": {
            "casual": [["Free"]]
        },
        "SwampEntryArea": {
            "casual": [["Free"]]
        }
    },
    "OuterSwampMortarAbilityCellLedge": { 
        "UpperGrotto": {
            "casual": [["Free"]]
        }
    },
    "OuterSwampMortarPlantAccess": {
    },
    "GinsoOuterDoor": { 
        "GinsoInnerDoor": {
            "casual": [["Free"]]
        },
        "OuterSwampUpperArea": {
            "casual": [["GinsoKey"]]
        }
    },
    "GinsoInnerDoor": { 
        "LowerGinsoTree": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"], ["ChargeDash", "WallJump"], ["ChargeDash", "Climb"]]
        },
        "GinsoOuterDoor": {
            "casual": [["Free"]]
        }
    },
    "LowerGinsoTree": { 
        "GinsoMiniBossDoor": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "Glide"], ["Climb", "DoubleJump"], ["Climb", "Glide"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"], ["Bash", "Grenade", "DoubleJump"], ["Bash", "Grenade", "Glide"]], 
            "standard": [["WallJump", ("HealthCell", 3)], ["Climb", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 3)], ["WallJump", "AirDash"], ["Climb", "AirDash"], ["ChargeJump", "AirDash"]], 
            "expert": [["WallJump"]], 
            "master": [["DoubleJump"], ["Bash"]]
        },
        "R4InnerDoor": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        }
    },
    "GinsoMiniBossDoor": { 
        "BashTreeDoorClosed": {
            "casual": [["Free"]]
        }
    },
    "BashTreeDoorClosed": { 
        "BashTreeDoorOpened": {
            "casual": [[("KeyStone", 36)], [("GinsoKeyStone", 8)]]
        }
    },
    "BashTreeDoorOpened": { 
        "GinsoMiniBossDoor": {
            "casual": [["Open"]]
        },
        "BashTree": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"]]
        }
    },
    "BashTree": { 
        "BashTreeDoorClosed": {
            "casual": [["Open"]]
        },
        "UpperGinsoRedirectArea": {
            "casual": [["Bash"], ["ChargeJump", "Dash", "DoubleJump"], ["ChargeJump", "DoubleJump", "Glide"]], 
            "standard": [["ChargeJump", ("HealthCell", 4)]], 
            "expert": [["ChargeJump", ("HealthCell", 3)], ["ChargeJump", "ChargeDash"]], 
            "master": [["DoubleJump", "Dash"], ["DoubleJump", "WallJump"], ["DoubleJump", "Climb"], ["TripleJump"]]
        }
    },
    "UpperGinsoRedirectArea": { 
        "UpperGinsoTree": {
            "casual": [["Bash"], ["ChargeJump"]], 
            "master": [["TripleJump", "Stomp", "WallJump"], ["TripleJump", "ChargeFlame", "WallJump"], ["TripleJump", "Grenade", "WallJump"], ["TripleJump", "Stomp", "Climb"], ["TripleJump", "ChargeFlame", "Climb"], ["TripleJump", "Grenade", "Climb"]]
        },
        "BashTree": {
            "casual": [["Bash"], ["DoubleJump"]], 
            "standard": [["AirDash"], ["Dash", ("HealthCell", 4)], ["WallJump", ("HealthCell", 4)], ["Climb", ("HealthCell", 4)], ["Glide", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4)]]
        }
    },
    "UpperGinsoTree": { 
        "UpperGinsoDoorClosed": {
            "casual": [["Free"]]
        },
        "UpperGinsoRedirectArea": {
            "casual": [["Stomp"], ["ChargeJump", "Bash"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["ChargeJump", "ChargeFlame"], ["ChargeJump", "AirDash"]], 
            "master": [["Bash"]]
        }
    },
    "UpperGinsoDoorClosed": { 
        "UpperGinsoDoorOpened": {
            "casual": [[("KeyStone", 36)], [("GinsoKeyStone", 8)]]
        }
    },
    "UpperGinsoDoorOpened": { 
        "GinsoTeleporter": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"]], 
            "standard": [["Bash"]], 
            "expert": [["ChargeJump", "DoubleJump", ("HealthCell", 3)], ["ChargeJump", ("HealthCell", 5)]], 
            "master": [["WallJump", "TripleJump", ("HealthCell", 5), "UltraDefense"]]
        },
        "UpperGinsoTree": {
            "casual": [["Open", "Bash"], ["Open", "DoubleJump"], ["Open", "Glide"], ["Open", ("HealthCell", 3)]], 
            "standard": [["Open", "AirDash"]]
        }
    },
    "GinsoTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "TopGinsoTree": {
            "casual": [["Bash", "WallJump", "DoubleJump"], ["Bash", "Climb", "DoubleJump"], ["ChargeJump", "WallJump"], ["ChargeJump", "Climb"]], 
            "standard": [["WallJump", "DoubleJump", "ChargeFlame"], ["WallJump", "DoubleJump", "Grenade"]], 
            "expert": [["WallJump", "DoubleJump", "Stomp"], ["ChargeJump"]], 
            "master": [["TripleJump", "ChargeFlame"], ["TripleJump", "Grenade"], ["TripleJump", "Stomp"]]
        },
        "UpperGinsoDoorClosed": {
            "casual": [["Open"]]
        }
    },
    "TopGinsoTree": { 
        "GinsoEscape": {
            "casual": [["Bash", "Grenade"], ["Bash", "ChargeJump"], ["Bash", "DoubleJump"]], 
            "standard": [["Bash"], ["Stomp", "ChargeJump"], ["Stomp", "Dash", "WallJump", "DoubleJump", ("HealthCell", 3)], ["Stomp", "Dash", "Climb", "DoubleJump", ("HealthCell", 3)], ["Stomp", "WallJump", "DoubleJump", "Glide", ("HealthCell", 3)], ["Stomp", "Climb", "DoubleJump", "Glide", ("HealthCell", 3)]], 
            "expert": [["Stomp", "ChargeDash"]], 
            "master": [["Stomp", "TripleJump"], ["Stomp", "DoubleJump", "Glide", ("HealthCell", 3)], ["Stomp", "DoubleJump", "Dash", ("HealthCell", 3)]]
        }
    },
    "GinsoEscape": { 
        "GinsoEscapeComplete": {
            "casual": [["Bash", "DoubleJump", "WallJump"], ["Bash", "DoubleJump", "Climb"]], 
            "standard": [["Bash", "Climb"], ["Bash", "WallJump"]], 
            "expert": [["ChargeJump", "Climb", "DoubleJump"], ["ChargeJump", "WallJump", ("HealthCell", 9)], ["ChargeJump", "Climb", ("HealthCell", 3)], ["ChargeJump", "DoubleJump", "ChargeDash", ("HealthCell", 3)], ["DoubleBash"]], 
            "master": [["ChargeJump", "DoubleJump", ("HealthCell", 7)], ["WallJump", "TripleJump", "UltraDefense", ("HealthCell", 6)], ["Climb", "TripleJump", "UltraDefense", ("HealthCell", 10)]], 
            "insane": [["TripleJump", "UltraDefense", ("HealthCell", 12)]]
        }
    },
    "GinsoEscapeComplete": { 
        "Swamp": {
            "casual": [["Free"]]
        }
    },
    "UpperGrotto": { 
        "MoonGrottoStompPlantAccess": {
            "casual": [["Stomp"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "master": [["Bash"]]
        },
        "OuterSwampSwarmLedge": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "expert": [["DoubleJump"]]
        },
        "Iceless": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["WallJump", "Glide"]], 
            "standard": [["Bash", "Grenade"], ["WallJump", "ChargeJump", ("HealthCell", 4)], ["Climb", "ChargeJump", ("HealthCell", 4)], ["Climb", "AirDash"]], 
            "master": [["ChargeJump", "DoubleJump"], ["Bash"], ["GrenadeJump"]]
        },
        "MoonGrottoAboveTeleporter": {
            "casual": [["WallJump"], ["Climb"], ["Dash"], ["DoubleJump"], ["Glide"]], 
            "standard": [["Bash", "Grenade"]], 
            "glitched": [["Free"]]
        }
    },
    "MoonGrottoStompPlantAccess": {
    },
    "MoonGrottoAboveTeleporter": { 
        "UpperGrotto": {
            "casual": [["WallJump"], ["Climb", "DoubleJump"], ["Climb", "ChargeJump"]], 
            "standard": [["Bash", "Grenade"]], 
            "expert": [["Climb", "Glide"]], 
            "master": [["DoubleJump"], ["Bash", "AirDash"]]
        },
        "MoonGrottoStompPlantAccess": {
            "expert": [["ChargeFlame"]]
        },
        "MoonGrottoSwampAccessArea": {
            "casual": [["ChargeJump", "DoubleJump"], ["Bash"], ["DoubleJump", ("HealthCell", 3)]], 
            "standard": [["ChargeJump", ("HealthCell", 3)]], 
            "expert": [["Dash", ("HealthCell", 4)], ["ChargeDash"]], 
            "master": [["GrenadeJump"]]
        },
        "MoonGrotto": {
            "casual": [["Free"]]
        },
        "DeathGauntletRoof": {
            "master": [["Lure", "Bash"]]
        }
    },
    "MoonGrotto": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "MoonGrottoAboveTeleporter": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "master": [["DoubleJump"]], 
            "expert": [["ChargeDash", ("EnergyCell", 1)]]
        },
        "DeathGauntlet": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"], ["DoubleJump"]]
        },
        "GumoHideout": {
            "casual": [["Free"]]
        },
        "LeftGumoHideout": {
            "casual": [["Free"]]
        },
        "SideFallCell": {
            "casual": [["Free"]]
        },
        "WaterVeinArea": {
            "casual": [["DoubleJump"], ["Glide"], ["Climb", "ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["WallJump"], ["Climb"], ["ChargeJump"], ["Dash"]], 
            "expert": [["Free"]], 
            "master": [["Lure", "Bash"]]
        }
    },
    "Iceless": { 
        "HollowGrove": {
            "casual": [["Free"]]
        },
        "UpperGrotto": {
            "casual": [["DoubleJump"], ["Glide"]], 
            "standard": [["Bash", "Grenade"], [("HealthCell", 4)]], 
            "master": [["GrenadeJump"]]
        }
    },
    "MoonGrottoSwampAccessArea": { 
        "InnerSwampAboveDrainArea": {
            "casual": [["ChargeJump"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["Lure", "WallJump", "DoubleJump", "Stomp"], ["Lure", "Climb", "DoubleJump", "Stomp"], ["Lure", "WallJump", "ChargeFlame"], ["Lure", "Climb", "ChargeFlame"]], 
            "master": [["Lure", "DoubleJump", "Grenade"]]
        }
    },
    "SideFallCell": { 
        "LeftGumoHideout": {
            "casual": [["Free"]]
        },
        "GumoHideout": {
            "casual": [["Free"]]
        }
    },
    "GumoHideout": { 
        "DoubleJumpKeyDoor": {
            "casual": [[("KeyStone", 40)], [("GrottoKeyStone", 2)]]
        },
        "LeftGumoHideout": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Grenade", "Bash"]], 
            "expert": [["ChargeJump"]], 
            "master": [["WallJump", "Bash"], ["Climb", "Bash"], ["TripleJump"]]
        },
        "LowerLeftGumoHideout": {
            "master": [["DoubleJump"], ["Dash", "WallJump"], ["Dash", "Climb"]]
        },
        "SideFallCell": {
            "casual": [["WallJump", "Bash", "Grenade"], ["Climb", "Bash", "Grenade"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Glide", "Wind"]], 
            "expert": [["DoubleBash"]]
        }
    },
    "DoubleJumpKeyDoor": { 
        "DoubleJumpKeyDoorOpened": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "expert": [["DoubleJump"]]
        }
    },
    "DoubleJumpKeyDoorOpened": {
    },
    "LeftGumoHideout": { 
        "LowerLeftGumoHideout": {
            "casual": [["Free"]]
        },
        "WaterVeinArea": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Bash", "Grenade"], ["Glide", "Wind"]], 
            "standard": [["Climb", "DoubleJump"], ["WallJump", "AirDash"], ["Climb", "AirDash"]], 
            "master": [["DoubleJump"], ["WallJump", "Dash"]]
        },
        "GumoHideout": {
            "casual": [["Free"]]
        }
    },
    "LowerLeftGumoHideout": { 
        "LowerBlackroot": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        },
        "GumoHideoutRedirectArea": {
            "casual": [["Free"]]
        },
        "GumoHideout": {
            "casual": [["Free"]]
        }
    },
    "WaterVeinArea": { 
        "LeftGumoHideout": {
            "casual": [["Free"]]
        },
        "LowerLeftGumoHideout": {
            "casual": [["DoubleJump"], ["Glide"], ["ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["Dash"]]
        },
        "MoonGrotto": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump", "DoubleJump"], ["WallJump", "Glide"], ["Climb", "Glide"], ["ChargeJump", "Glide"], ["Climb", "ChargeJump"], ["Bash", "Grenade"]], 
            "standard": [["WallJump", "Dash"], ["Climb", "Dash"]]
        },
        "GumoHideout": {
            "casual": [["Free"]]
        },
        "SideFallCell": {
            "casual": [["Free"]]
        }
    },
    "GumoHideoutRedirectArea": { 
        "GumoHideoutRedirectEnergyVault": {
            "casual": [[("EnergyCell", 4)]], 
            "glitched": [["Free"]]
        }
    },
    "GumoHideoutRedirectEnergyVault": {
    },
    "SwampEntryArea": { 
        "SwampDrainlessArea": {
            "casual": [["Stomp", "WallJump"], ["Stomp", "Climb"], ["Stomp", "Bash", "Grenade"], ["Stomp", "ChargeJump"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["Lure", "Bash", "WallJump"], ["Lure", "Bash", "Climb"], ["Lure", "Bash", "Grenade"], ["Lure", "Bash", "ChargeJump"]]
        },
        "Swamp": {
            "casual": [["Stomp", "ChargeJump"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["Lure", "Bash", "WallJump"], ["Lure", "Bash", "Climb"], ["Lure", "Bash", "Grenade"], ["Lure", "Bash", "ChargeJump"]]
        }
    },
    "Swamp": { 
        "SwampDrainlessArea": {
            "casual": [["Stomp"]], 
            "expert": [["ChargeJump", "Climb"]]
        },
        "SwampKeyDoorPlatform": {
            "casual": [["CleanWater"], ["DoubleJump"], ["Glide"], ["Bash", "Grenade"], ["ChargeJump"], [("HealthCell", 3)]], 
            "standard": [["Dash"]]
        },
        "SwampWater": {
            "casual": [["CleanWater"]], 
            "master": [[("HealthCell", 15)], [("HealthCell", 7), "UltraDefense"]]
        }
    },
    "SwampKeyDoorPlatform": { 
        "SwampKeyDoorOpened": {
            "casual": [[("KeyStone", 40)], [("SwampKeyStone", 2)]]
        },
        "InnerSwampSkyArea": {
            "casual": [["Wind", "Glide"]], 
            "standard": [["ChargeJump", "Climb", "Glide"], ["ChargeJump", "Climb", "DoubleJump"]], 
            "expert": [["DoubleBash"]], 
            "master": [["GrenadeJump"]]
        }
    },
    "SwampKeyDoorOpened": { 
        "RightSwamp": {
            "casual": [["WallJump", "DoubleJump", "Bash"], ["Climb", "ChargeJump", "Bash"], ["Climb", "Bash", "Grenade"]], 
            "standard": [["Climb", "DoubleJump", "Bash"], ["Bash", "Grenade"], ["Climb", "ChargeJump", "Glide"], ["WallJump", "ChargeJump", "Glide"], ["Climb", "ChargeJump", ("HealthCell", 3)], ["WallJump", "ChargeJump", ("HealthCell", 3)], ["WallJump", "DoubleJump", "Glide", ("HealthCell", 3)], ["Climb", "DoubleJump", "Glide", ("HealthCell", 3)]], 
            "expert": [["WallJump", "DoubleJump", ("HealthCell", 5)], ["Climb", "DoubleJump", ("HealthCell", 5)], ["CleanWater", "WallJump", "Bash", ("HealthCell", 3)], ["ChargeJump", "DoubleJump", ("HealthCell", 3)], ["Bash", "ChargeDash", ("HealthCell", 3), ("EnergyCell", 3)], ["WallJump", "ChargeDash", ("HealthCell", 3)], ["Climb", "ChargeDash", ("HealthCell", 3)], ["Climb", "ChargeDash", ("EnergyCell", 2)], ["WallJump", "ChargeDash", ("EnergyCell", 2)], ["CleanWater", "DoubleBash"], ["DoubleBash", ("HealthCell", 5)]], 
            "master": [["CleanWater", "WallJump", "UltraDefense", ("HealthCell", 5)], ["WallJump", "UltraDefense", ("HealthCell", 7)], ["CleanWater", "WallJump", ("HealthCell", 9)], ["WallJump", ("HealthCell", 12)], ["TripleJump", "UltraDefense", ("HealthCell", 4)], ["DoubleJump", ("HealthCell", 7)], ["DoubleJump", "ChargeDash", ("EnergyCell", 2)], ["GrenadeJump"]]
        }
    },
    "SwampDrainlessArea": { 
        "UpperGrotto": {
            "casual": [["ChargeJump"]]
        },
        "OuterSwampLowerArea": {
            "casual": [["ChargeJump"]]
        },
        "Swamp": {
            "casual": [["ChargeJump"]]
        }
    },
    "InnerSwampAboveDrainArea": { 
        "InnerSwampDrainBroken": {
            "casual": [["Grenade"], ["ChargeFlame", "CleanWater"], ["ChargeFlame", ("HealthCell", 3)]]
        }
    },
    "InnerSwampDrainBroken": { 
        "Swamp": {
            "casual": [["ChargeJump", "WallJump", "DoubleJump"], ["ChargeJump", "Climb", "DoubleJump"], ["ChargeJump", "WallJump", "Glide"], ["ChargeJump", "Climb", "Glide"], ["ChargeJump", "WallJump", ("HealthCell", 3)], ["ChargeJump", "Climb", ("HealthCell", 3)], ["CleanWater", "WallJump", "DoubleJump"], ["CleanWater", "WallJump", "Glide"], ["CleanWater", "Climb", "ChargeJump"], ["CleanWater", "Climb", "Bash", "Grenade"], ["CleanWater", "Climb", "Glide", ("HealthCell", 3)]], 
            "expert": [["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["ChargeJump", ("HealthCell", 3)], ["CleanWater", "DoubleJump"], ["CleanWater", "Climb", ("HealthCell", 3)]], 
            "master": [["Bash"], ["WallJump", ("HealthCell", 13)], ["Climb", ("HealthCell", 13)], ["DoubleJump", ("HealthCell", 13)], ["WallJump", ("HealthCell", 7), "UltraDefense"], ["Climb", ("HealthCell", 7), "UltraDefense"], ["TripleJump", ("HealthCell", 7), "UltraDefense"]], 
            "standard": [["CleanWater", "Climb", "DoubleJump"], ["CleanWater", "WallJump", "AirDash"], ["CleanWater", "Climb", "AirDash"]]
        }
    },
    "InnerSwampSkyArea": { 
        "Swamp": {
            "casual": [["Free"]]
        },
        "SwampKeyDoorPlatform": {
            "casual": [["Free"]]
        }
    },
    "SwampWater": {
    },
    "RightSwamp": {
    },
    "HoruFields": { 
        "HoruFieldsPushBlock": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"]], 
            "standard": [["Bash", "Grenade"], ["ChargeJump", "DoubleJump", "Glide", "Climb"], ["ChargeJump", "DoubleJump", "Glide", "WallJump"], ["ChargeJump", "Glide", "Climb", "AirDash"], ["ChargeJump", "Glide", "WallJump", "AirDash"]], 
            "expert": [["ChargeJump", "DoubleJump", "Glide"], ["ChargeJump", "Glide", "ChargeDash", ("EnergyCell", 3)], ["ChargeJump", "ChargeDash", ("EnergyCell", 4)], ["DoubleBash"]], 
            "master": [["WallJump", "TripleJump", "ChargeDash", ("EnergyCell", 5)], ["Climb", "TripleJump", "ChargeDash", ("EnergyCell", 4)], ["GrenadeJump"]]
        },
        "HorufieldsHoruDoor": {
            "casual": [["Bash", "DoubleJump", "WallJump"], ["Bash", "DoubleJump", "Climb"], ["Bash", "Glide", "WallJump"], ["Bash", "Glide", "Climb"]], 
            "standard": [["Bash", "Grenade"], ["ChargeJump", "Glide"]], 
            "master": [["Bash"], ["WallJump", "Stomp", "Glide", "TripleJump"], ["WallJump", "TripleJump", "ChargeDash", ("EnergyCell", 3)], ["Climb", "TripleJump", "ChargeDash"], ["GrenadeJump"]]
        }
    },
    "HoruFieldsPushBlock": { 
        "HollowGrove": {
            "casual": [["None"]],
            "master": [["Lure", "Bash"]]
        }
    },
    "HorufieldsHoruDoor": { 
        "HoruOuterDoor": {
            "casual": [["HoruKey"]]
        },
        "HoruFieldsPushBlock": {
            "casual": [["Bash", "Grenade"], ["Bash", "Glide"], ["Bash", "ChargeJump", "DoubleJump"], ["ChargeJump", "DoubleJump", "Climb"], ["ChargeJump", "DoubleJump", "WallJump"]], 
            "standard": [["Dash", "Bash", "DoubleJump"], ["ChargeJump", "Glide", "Climb", "AirDash"], ["ChargeJump", "Glide", "WallJump", "AirDash"]], 
            "expert": [["ChargeJump", "DoubleJump", "Glide"], ["ChargeJump", "ChargeDash"]], 
            "master": [["ChargeJump", "DoubleJump"], ["Bash", "TripleJump"], ["GrenadeJump"]]
        }
    },
    "HoruOuterDoor": { 
        "HoruInnerDoor": {
            "casual": [["Free"]]
        },
        "HorufieldsHoruDoor": {
            "casual": [["HoruKey"]]
        }
    },
    "HoruInnerDoor": { 
        "HoruInnerEntrance": {
            "casual": [["Free"]]
        },
        "HoruOuterDoor": {
            "casual": [["Free"]]
        }
    },
    "HoruInnerEntrance": { 
        "HoruInnerDoor": {
            "casual": [["Free"]]
        },
        "HoruMapLedge": {
            "casual": [["Bash", "DoubleJump", "Glide", "WallJump"], ["Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Bash", "Glide", "ChargeJump", "WallJump"], ["Bash", "DoubleJump", "Glide", "Climb"], ["Bash", "DoubleJump", "ChargeJump", "Climb"], ["Bash", "Glide", "ChargeJump", "Climb"]], 
            "expert": [["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"], ["DoubleBash"]], 
            "master": [["ChargeJump", "WallJump", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "L1OuterEntrance": {
            "casual": [["Bash", "DoubleJump", "Glide", "WallJump"], ["Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Bash", "Glide", "ChargeJump", "WallJump"], ["Bash", "DoubleJump", "Glide", "Climb"], ["Bash", "DoubleJump", "ChargeJump", "Climb"], ["Bash", "Glide", "ChargeJump", "Climb"]], 
            "expert": [["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"], ["DoubleBash"]], 
            "master": [["ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        },
        "L2OuterEntrance": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open", "ChargeJump", "Bash", "DoubleJump", "WallJump"], ["Open", "ChargeJump", "Bash", "DoubleJump", "Climb"], ["Open", "ChargeJump", "Bash", "Glide", "WallJump"], ["Open", "ChargeJump", "Bash", "Glide", "Climb"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"], ["ChargeJump", "WallJump", ("HealthCell", 5)], ["Open", "ChargeDash", "WallJump"], ["Open", "ChargeDash", "Climb"], ["Open", "DoubleBash"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"], ["Open", "ChargeJump", "TripleJump"], ["Open", "GrenadeJump"]], 
            "standard": [["Open", "Bash", "Grenade"], ["Open", "Bash", "DoubleJump", "Glide"], ["Open", "ChargeJump", "Bash", "WallJump"], ["Open", "ChargeJump", "Bash", "Climb"], ["Open", "ChargeJump", "WallJump", "DoubleJump"], ["Open", "ChargeJump", "WallJump", "Glide"]]
        },
        "L3OuterEntrance": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open", "ChargeJump", "Bash", "DoubleJump", "WallJump"], ["Open", "ChargeJump", "Bash", "DoubleJump", "Climb"], ["Open", "ChargeJump", "Bash", "Glide", "WallJump"], ["Open", "ChargeJump", "Bash", "Glide", "Climb"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"], ["ChargeJump", "WallJump", ("HealthCell", 5)], ["Open", "ChargeDash", "WallJump"], ["Open", "ChargeDash", "Climb"], ["Open", "DoubleBash"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"], ["Open", "ChargeJump", "TripleJump"], ["Open", "GrenadeJump"]], 
            "standard": [["Open", "Bash", "Grenade"], ["Open", "Bash", "DoubleJump", "Glide"], ["Open", "ChargeJump", "Bash", "WallJump"], ["Open", "ChargeJump", "Bash", "Climb"], ["Open", "ChargeJump", "WallJump", "DoubleJump"], ["Open", "ChargeJump", "WallJump", "Glide"]]
        },
        "L4OuterEntrance": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open", "Bash"], ["Open", "ChargeJump"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"], ["Open", "ChargeDash"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        },
        "R1OuterEntrance": {
            "casual": [["Bash", "DoubleJump", "Glide", "WallJump"], ["Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Bash", "Glide", "ChargeJump", "WallJump"], ["Bash", "DoubleJump", "Glide", "Climb"], ["Bash", "DoubleJump", "ChargeJump", "Climb"], ["Bash", "Glide", "ChargeJump", "Climb"]], 
            "expert": [["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"], ["DoubleBash"]], 
            "master": [["ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        },
        "R2OuterEntrance": {
            "casual": [["Bash", "DoubleJump", "Glide", "WallJump"], ["Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Bash", "Glide", "ChargeJump", "WallJump"], ["Bash", "DoubleJump", "Glide", "Climb"], ["Bash", "DoubleJump", "ChargeJump", "Climb"], ["Bash", "Glide", "ChargeJump", "Climb"], ["Open", "ChargeJump", "Bash", "DoubleJump", "WallJump"], ["Open", "ChargeJump", "Bash", "DoubleJump", "Climb"], ["Open", "ChargeJump", "Bash", "Glide", "WallJump"], ["Open", "ChargeJump", "Bash", "Glide", "Climb"]], 
            "expert": [["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"], ["Open", "ChargeDash", "WallJump"], ["Open", "ChargeDash", "Climb"], ["Open", "DoubleBash"]], 
            "master": [["ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"], ["Open", "ChargeJump", "TripleJump"], ["Open", "GrenadeJump"]], 
            "standard": [["Open", "Bash", "Grenade"], ["Open", "Bash", "DoubleJump", "Glide"], ["Open", "ChargeJump", "Bash", "WallJump"], ["Open", "ChargeJump", "Bash", "Climb"], ["Open", "ChargeJump", "Dash", "DoubleJump", "WallJump"], ["Open", "ChargeJump", "Dash", "Glide", "WallJump"]]
        },
        "R3OuterEntrance": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open", "ChargeJump", "Bash", "DoubleJump", "WallJump"], ["Open", "ChargeJump", "Bash", "DoubleJump", "Climb"], ["Open", "ChargeJump", "Bash", "Glide", "WallJump"], ["Open", "ChargeJump", "Bash", "Glide", "Climb"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"], ["ChargeJump", "WallJump", ("HealthCell", 5)], ["Open", "ChargeDash", "WallJump"], ["Open", "ChargeDash", "Climb"], ["Open", "DoubleBash"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"], ["Open", "ChargeJump", "TripleJump"], ["Open", "GrenadeJump"]], 
            "standard": [["Open", "Bash", "Grenade"], ["Open", "Bash", "DoubleJump", "Glide"], ["Open", "ChargeJump", "Bash", "WallJump"], ["Open", "ChargeJump", "Bash", "Climb"], ["Open", "ChargeJump", "WallJump", "DoubleJump"], ["Open", "ChargeJump", "WallJump", "Glide"]]
        },
        "R4OuterEntrance": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open", "Bash", "Grenade"], ["Open", "ChargeJump", "WallJump"], ["Open", "ChargeJump", "Climb"], ["Open", "ChargeJump", "DoubleJump"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"], ["Open", "ChargeDash"], ["Open", "DoubleBash"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        },
        "HoruBasement": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open"]], 
            "expert": [["Free"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        },
        "HoruTeleporter": {
            "casual": [["Stomp", "Bash", "DoubleJump", "Glide", "WallJump"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "WallJump"], ["Stomp", "Bash", "Glide", "ChargeJump", "WallJump"], ["Stomp", "Bash", "DoubleJump", "Glide", "Climb"], ["Stomp", "Bash", "DoubleJump", "ChargeJump", "Climb"], ["Stomp", "Bash", "Glide", "ChargeJump", "Climb"], ["Open"]], 
            "expert": [["Stomp", "Bash", "Grenade", "WallJump"], ["Stomp", "Bash", "Grenade", "Climb"]], 
            "master": [["Stomp", "ChargeJump", "WallJump", "TripleJump", "Glide", ("HealthCell", 8), "UltraDefense"]]
        }
    },
    "HoruTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "ChargeJump", "WallJump"], ["Open", "ChargeJump", "Climb"], ["Open", "Bash", "Grenade"]], 
            "expert": [["Open", "DoubleBash"]], 
            "master": [["Open", "ChargeJump", "DoubleJump"], ["Open", "WallJump", "TripleJump"]]
        }
    },
    "HoruBasement": { 
        "HoruEscapeOuterDoor": {
            "casual": [["WallJump"], ["Climb"], ["DoubleJump"], ["Dash"], ["ChargeJump", "Glide"], ["Bash", "Grenade"]]
        }
    },
    "HoruMapLedge": {
    },
    "L1OuterEntrance": { 
        "L1OuterDoor": {
            "casual": [["Free"]]
        },
        "R1OuterEntrance": {
            "casual": [["Bash"]]
        },
        "HoruMapLedge": {
            "casual": [["Bash", "Glide"], ["ChargeJump", "Glide"]], 
            "standard": [["AirDash", "ChargeJump", "DoubleJump"]]
        },
        "L3OuterEntrance": {
            "casual": [["Open", "Bash", "Glide"]]
        },
        "L2OuterEntrance": {
            "casual": [["Open", "ChargeJump", "Glide"]], 
            "standard": [["Open", "AirDash", "ChargeJump", "DoubleJump"]]
        },
        "R2OuterEntrance": {
            "casual": [["Open", "ChargeJump", "Glide"]], 
            "standard": [["Open", "AirDash", "ChargeJump", "DoubleJump"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Bash", "Glide"], ["ChargeJump", "Glide"]]
        }
    },
    "L1OuterDoor": { 
        "L1OuterEntrance": {
            "casual": [["Free"]]
        },
        "L1InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L1InnerDoor": { 
        "L1": {
            "casual": [["Free"]]
        },
        "L1OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "L1": { 
        "L1InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L2OuterEntrance": { 
        "L2OuterDoor": {
            "casual": [["Free"]]
        },
        "L3OuterEntrance": {
            "casual": [["Open", "Glide"], ["Open", "ChargeJump", "DoubleJump"]], 
            "standard": [["Open", "ChargeJump", "Climb"], ["Open", "DoubleJump", "Climb"], ["Open", "DoubleJump", "WallJump"], ["Open", "BashGrenade"], ["Open", "AirDash"]], 
            "expert": [["Open", "DoubleJump"], ["Open", "ChargeJump"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "Glide"], ["Open", "ChargeJump", "DoubleJump"]], 
            "standard": [["Open", "ChargeJump", "Climb"], ["Open", "DoubleJump", "Climb"], ["Open", "DoubleJump", "WallJump"], ["Open", "BashGrenade"], ["Open", "AirDash"]], 
            "expert": [["Open", "DoubleJump"], ["Open", "ChargeJump"]]
        }
    },
    "L2OuterDoor": { 
        "L2OuterEntrance": {
            "casual": [["Free"]]
        },
        "L2InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L2InnerDoor": { 
        "L2": {
            "casual": [["Free"]]
        },
        "L2OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "L2": { 
        "L2InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L3OuterEntrance": { 
        "L3OuterDoor": {
            "casual": [["Free"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        },
        "L4OuterEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        },
        "R4OuterEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        }
    },
    "L3OuterDoor": { 
        "L3OuterEntrance": {
            "casual": [["Free"]]
        },
        "L3InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L3InnerDoor": { 
        "L3": {
            "casual": [["Free"]]
        },
        "L3OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "L3": { 
        "L3InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L4OuterEntrance": { 
        "L4OuterDoor": {
            "casual": [["Free"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "Free"]]
        }
    },
    "L4OuterDoor": { 
        "L4OuterEntrance": {
            "casual": [["Free"]]
        },
        "L4InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "L4InnerDoor": { 
        "L4": {
            "casual": [["Free"]]
        },
        "L4OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "L4": { 
        "L4InnerDoor": {
            "casual": [["Free"]]
        },
        "HoruL4LavaChasePeg": {
            "casual": [["Bash"]], 
            "master": [["GrenadeJump"]]
        },
        "HoruL4CutscenePeg": {
            "casual": [["None"]],
            "expert": [["Free"]]
        }
    },
    "HoruL4LavaChasePeg": { 
        "HoruL4CutscenePeg": {
            "casual": [["Bash", "Stomp", "ChargeJump"], ["Bash", "Stomp", "Grenade"]], 
            "standard": [["Bash", "Stomp", "WallJump", "DoubleJump"]], 
            "expert": [["Bash", "Stomp", "Climb", "DoubleJump"], ["Bash", "Stomp", "ChargeDash", ("EnergyCell", 2)]], 
            "master": [["Bash", "Stomp", "DoubleJump"]]
        }
    },
    "HoruL4CutscenePeg": {
    },
    "R1OuterEntrance": { 
        "R1OuterDoor": {
            "casual": [["Free"]]
        },
        "L1OuterEntrance": {
            "casual": [["None"]],
            "expert": [["Free"]]
        }
    },
    "R1OuterDoor": { 
        "R1OuterEntrance": {
            "casual": [["Free"]]
        },
        "R1InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "R1InnerDoor": { 
        "R1": {
            "casual": [["Free"]]
        },
        "R1OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "R1": { 
        "R1InnerDoor": {
            "casual": [["Free"]]
        },
        "HoruR1MapstoneSecret": {
            "casual": [["Glide"], ["DoubleJump"]], 
            "standard": [["Bash", "Grenade"], ["AirDash"]], 
            "expert": [["Bash", ("HealthCell", 5)], ["Dash", ("HealthCell", 5)], ["ChargeJump", "Climb", ("HealthCell", 5)]], 
            "master": [[("HealthCell", 9)], [("HealthCell", 7), "UltraDefense"], ["Bash", ("HealthCell", 4), "UltraDefense"], ["ChargeDash", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "Climb", ("HealthCell", 4), "UltraDefense"], ["GrenadeJump", ("HealthCell", 5)], ["GrenadeJump", ("HealthCell", 4), "UltraDefense"], ["GrenadeJump", "Stomp"]]
        }
    },
    "HoruR1MapstoneSecret": { 
        "HoruR1CutsceneTrigger": {
            "casual": [["Bash", "ChargeJump", "Glide"], ["Bash", "ChargeJump", "DoubleJump"], ["Bash", "Grenade", "Glide"], ["Bash", "Grenade", "DoubleJump"]], 
            "expert": [["Bash", "DoubleJump", "Glide"], ["ChargeJump", "DoubleJump", "Glide", ("HealthCell", 5)], ["ChargeJump", "ChargeDash", ("HealthCell", 5), ("EnergyCell", 1)], ["DoubleBash", "Glide"], ["DoubleBash", "DoubleJump"], ["DoubleBash", "AirDash"]], 
            "master": [["Bash", "DoubleJump"], ["TripleJump", "ChargeDash", ("HealthCell", 7), "UltraDefense", ("EnergyCell", 4)], ["GrenadeJump", "DoubleJump", ("HealthCell", 5)], ["GrenadeJump", "TripleJump", ("HealthCell", 4), "UltraDefense"], ["GrenadeJump", "Glide", ("HealthCell", 5)], ["GrenadeJump", "Glide", ("HealthCell", 4), "UltraDefense"], ["GrenadeJump", ("HealthCell", 9)]]
        },
        "R1": {
            "casual": [["Climb", "ChargeJump", "Glide", "Bash"], ["WallJump", "ChargeJump", "Glide", "Bash"], ["Climb", "DoubleJump", "Bash"], ["WallJump", "DoubleJump", "Bash"]], 
            "standard": [["ChargeJump", "Glide", "DoubleJump", "WallJump"], ["ChargeJump", "Glide", "DoubleJump", "Climb"], ["DoubleJump", "AirDash", "WallJump"], ["DoubleJump", "AirDash", "Climb"]], 
            "expert": [["DoubleJump", "Dash"], ["Bash", "DoubleJump"], ["BashGrenade"], ["DoubleJump", "Glide", "WallJump"], ["DoubleJump", "Glide", "Climb"], ["Bash", "ChargeJump", "Glide"], ["ChargeJump", "Glide", "DoubleJump"], ["ChargeJump", "DoubleJump", ("HealthCell", 5)], ["ChargeJump", "Glide", ("HealthCell", 5)], ["ChargeJump", "Bash", ("HealthCell", 5)]], 
            "master": [["DoubleBash", "Glide"], ["DoubleBash", "ChargeJump"], ["DoubleBash", "Dash"], ["TripleJump"], ["ChargeJump", ("HealthCell", 9)]]
        }
    },
    "HoruR1CutsceneTrigger": { 
        "LowerGinsoTree": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        }
    },
    "R2OuterEntrance": { 
        "R2OuterDoor": {
            "casual": [["Free"]]
        },
        "R3OuterEntrance": {
            "casual": [["Open", "DoubleJump", "Glide", "WallJump"], ["Open", "DoubleJump", "Glide", "Climb"], ["Open", "ChargeJump", "Glide", "WallJump"], ["Open", "ChargeJump", "Glide", "Climb"]], 
            "standard": [["Open", "AirDash", "DoubleJump", "WallJump"], ["Open", "AirDash", "DoubleJump", "Climb"], ["Open", "AirDash", "Glide", "WallJump"], ["Open", "AirDash", "Glide", "Climb"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "ChargeJump", "DoubleJump"], ["Open", "DoubleJump", "Glide"]], 
            "standard": [["Open", "BashGrenade"], ["Open", "AirDash", "DoubleJump"], ["Open", "AirDash", "ChargeJump"], ["Open", "AirDash", "Glide"]]
        },
        "R4OuterEntrance": {
            "casual": [["Open", "ChargeJump", "DoubleJump"], ["Open", "DoubleJump", "Glide"]], 
            "standard": [["Open", "BashGrenade"], ["Open", "AirDash", "DoubleJump"], ["Open", "AirDash", "ChargeJump"], ["Open", "AirDash", "Glide"]]
        },
        "L4OuterEntrance": {
            "casual": [["Open", "ChargeJump", "DoubleJump"], ["Open", "DoubleJump", "Glide"]], 
            "standard": [["Open", "BashGrenade"], ["Open", "AirDash", "DoubleJump"], ["Open", "AirDash", "ChargeJump"], ["Open", "AirDash", "Glide"]]
        }
    },
    "R2OuterDoor": { 
        "R2OuterEntrance": {
            "casual": [["Free"]]
        },
        "R2InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "R2InnerDoor": { 
        "R2": {
            "casual": [["Free"]]
        },
        "R2OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "R2": { 
        "R2InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "R3OuterEntrance": { 
        "R3OuterDoor": {
            "casual": [["Free"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        },
        "R4OuterEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        },
        "L4OuterEntrance": {
            "casual": [["Open", "Glide"], ["Open", "DoubleJump"]], 
            "standard": [["Open", "AirDash"], ["Open", "BashGrenade"], ["Open", "ChargeJump"]]
        }
    },
    "R3OuterDoor": { 
        "R3OuterEntrance": {
            "casual": [["Free"]]
        },
        "R3InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "R3InnerDoor": { 
        "R3": {
            "casual": [["Free"]]
        },
        "R3OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "R3": { 
        "R3InnerDoor": {
            "casual": [["Free"]]
        },
        "HoruR3ElevatorLever": {
            "casual": [["WallJump", "DoubleJump"], ["ChargeJump", "Climb"], ["Bash", "Grenade", "Climb"]], 
            "expert": [["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "DoubleJump"]], 
            "master": [["Climb", "TripleJump"], ["ChargeJump", "TripleJump"]]
        }
    },
    "HoruR3ElevatorLever": { 
        "HoruR3CutsceneTrigger": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "ChargeJump"], ["WallJump", "Glide"], ["WallJump", "Bash"], ["Climb", "ChargeJump", ("HealthCell", 2)]], 
            "standard": [["WallJump"]], 
            "master": [["Bash", "Grenade"], ["ChargeJump", "DoubleJump"], ["TripleJump"]]
        },
        "HoruR3PlantCove": {
            "master": [["Glide", "ChargeDash", ("EnergyCell", 1)], ["DoubleJump", "ChargeDash", ("EnergyCell", 1)], ["ChargeJump", "ChargeDash", ("EnergyCell", 1)], ["ChargeDash", ("EnergyCell", 2)]]
        }
    },
    "HoruR3PlantCove": {
    },
    "HoruR3CutsceneTrigger": { 
        "HoruR3PlantCove": {
            "casual": [["Free"]]
        }
    },
    "R4OuterEntrance": { 
        "R4OuterDoor": {
            "casual": [["Free"]]
        },
        "HoruInnerEntrance": {
            "casual": [["Open", "Free"]]
        },
        "L4OuterEntrance": {
            "casual": [["Open", "Glide"]], 
            "standard": [["Open", "AirDash", "DoubleJump"]]
        }
    },
    "R4OuterDoor": { 
        "R4OuterEntrance": {
            "casual": [["Free"]]
        },
        "R4InnerDoor": {
            "casual": [["Free"]]
        }
    },
    "R4InnerDoor": { 
        "R4": {
            "casual": [["Free"]]
        },
        "R4OuterDoor": {
            "casual": [["Free"]]
        }
    },
    "R4": { 
        "R4InnerDoor": {
            "casual": [["Free"]]
        },
        "HoruR4StompHideout": {
            "casual": [["ChargeFlame", "ChargeJump"], ["ChargeFlame", "Bash", "Grenade"], ["Stomp", "ChargeJump"], ["Stomp", "Bash", "Grenade"], ["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "standard": [["ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["Bash", "ChargeFlame"], ["Bash", "Stomp"], ["Bash", "ChargeDash"], ["Bash", ("HealthCell", 6)], ["DoubleBash"]]
        }
    },
    "HoruR4StompHideout": { 
        "HoruR4PuzzleEntrance": {
            "casual": [["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"], ["Bash", "Grenade"], ["Bash", "DoubleJump"], ["Bash", "Glide", "WallJump"], ["Bash", "Glide", "Climb"]], 
            "standard": [["ChargeJump", "AirDash"], ["Bash", "AirDash"]], 
            "expert": [["ChargeJump", ("HealthCell", 5)], ["Bash", ("HealthCell", 5)], ["DoubleBash"]], 
            "master": [["TripleJump", ("HealthCell", 4), "UltraDefense"], ["GrenadeJump"]]
        },
        "HoruR4CutsceneTrigger": {
            "expert": [["Bash", "ChargeJump"], ["ChargeJump", "DoubleJump", ("HealthCell", 5)], ["DoubleBash"]]
        }
    },
    "HoruR4PuzzleEntrance": { 
        "HoruR4CutsceneTrigger": {
            "casual": [["Bash", "Grenade"], ["Bash", "ChargeJump"]], 
            "expert": [["ChargeJump", "ChargeDash", ("EnergyCell", 2)]], 
            "master": [["GrenadeJump"]]
        }
    },
    "HoruR4CutsceneTrigger": { 
        "HoruR4PuzzleEntrance": {
            "casual": [["Free"]]
        },
        "R4": {
            "casual": [["Free"]]
        },
        "HoruR4StompHideout": {
            "casual": [["Stomp"], ["Climb", "ChargeJump"]], 
            "standard": [["Free"]]
        }
    },
    "HoruEscapeOuterDoor": { 
        "HoruEscapeInnerDoor": {
            "casual": [["Free"]]
        },
        "HoruBasement": {
            "casual": [["Free"]]
        }
    },
    "HoruEscapeInnerDoor": { 
        "HoruEscapeOuterDoor": {
            "casual": [["Free"]]
        }
    },
    "ValleyEntry": { 
        "ValleyEntryTree": {
            "casual": [["WallJump"], ["Bash", "Climb"], ["DoubleJump", "Climb"], ["ChargeJump", "Climb"]], 
            "standard": [["Lure", "Bash"]], 
            "expert": [["ChargeJump", ("HealthCell", 4)], ["ChargeDash"]]
        },
        "ValleyEntryTreePlantAccess": {
            "casual": [["ChargeJump", "ChargeFlame"], ["ChargeJump", "Grenade"], ["Bash", "Grenade"]], 
            "expert": [["WallJump", "ChargeFlame"], ["Grenade"], ["ChargeDash", ("EnergyCell", 2)]]
        },
        "ValleyPostStompDoor": {
            "casual": [["Stomp", "WallJump", "DoubleJump"], ["Stomp", "WallJump", "Bash"], ["Stomp", "WallJump", "ChargeJump"], ["Stomp", "Climb", "ChargeJump"], ["Stomp", "Climb", "DoubleJump"], ["WallJump", "DoubleJump", "OpenWorld"], ["WallJump", "Bash", "OpenWorld"], ["WallJump", "ChargeJump", "OpenWorld"], ["Climb", "ChargeJump", "OpenWorld"], ["Climb", "DoubleJump", "OpenWorld"]], 
            "expert": [["Lure", "Bash", "WallJump"], ["Lure", "Bash", "Climb", "ChargeJump"], ["Lure", "Bash", "Climb", "DoubleJump"], ["Bash", "ChargeJump", ("HealthCell", 4)], ["Stomp", "ChargeJump", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4), "OpenWorld"]]
        },
        "ValleyThreeBirdLever": {
            "casual": [["Glide", "Wind", "OpenWorld"], ["Bash", "OpenWorld"], ["Climb", "ChargeJump", "Glide", "OpenWorld"], ["Climb", "ChargeJump", "DoubleJump", "OpenWorld"]], 
            "standard": [["Dash", "DoubleJump", "ChargeJump", "OpenWorld"]], 
            "expert": [["ChargeDash", "OpenWorld"]], 
            "master": [["GrenadeJump", "OpenWorld"]]
        },
        "ValleyStompFloor": {
            "casual": [["Bash", "OpenWorld"], ["Glide", "Wind", "OpenWorld"], ["Glide", "DoubleJump", "OpenWorld"], ["ChargeJump", "DoubleJump", "OpenWorld"], ["ChargeJump", "Glide", "OpenWorld"], ["ChargeJump", "Climb", "OpenWorld"]], 
            "standard": [["Dash", "Glide", "OpenWorld"], ["Dash", "DoubleJump", "OpenWorld"], ["ChargeJump", "AirDash", "OpenWorld"], [("HealthCell", 4), "OpenWorld"]], 
            "expert": [["ChargeDash", "OpenWorld"]]
        },
        "SpiritTreeRefined": {
            "casual": [["ChargeFlame"], ["Grenade"]], 
            "expert": [["ChargeDash"]]
        }
    },
    "ValleyEntryTree": { 
        "ValleyEntryTreePlantAccess": {
            "casual": [["ChargeJump", "Climb"], ["ChargeJump", "DoubleJump"], ["Bash"], ["Glide"]], 
            "expert": [["Grenade"], ["ChargeDash"]]
        },
        "ValleyPostStompDoor": {
            "casual": [["OpenWorld"]]
        }
    },
    "ValleyEntryTreePlantAccess": {
    },
    "ValleyPostStompDoor": { 
        "ValleyRight": {
            "casual": [["Bash", "WallJump"], ["Bash", "Climb"], ["Bash", "ChargeJump"], ["Bash", "Grenade"]], 
            "expert": [["WallJump", "DoubleJump", "ChargeJump", ("HealthCell", 7)], ["DoubleBash"]], 
            "master": [["WallJump", "TripleJump", "ChargeJump", "UltraDefense", ("HealthCell", 3)], ["Climb", "TripleJump", "ChargeJump", "UltraDefense", ("HealthCell", 3)], ["WallJump", "TripleJump", ("HealthCell", 11), "UltraDefense"], ["GrenadeJump", "Stomp", "DoubleJump", ("HealthCell", 4)], ["GrenadeJump", "Stomp", "TripleJump"], ["GrenadeJump", "ChargeDash"], ["GrenadeJump", ("HealthCell", 7)], ["GrenadeJump", ("HealthCell", 5), "UltraDefense"]]
        },
        "ValleyEntry": {
            "casual": [["OpenWorld"]]
        },
        "ValleyEntryTree": {
            "casual": [["OpenWorld", "WallJump"], ["OpenWorld", "Climb"], ["OpenWorld", "DoubleJump"], ["OpenWorld", "ChargeJump"], ["OpenWorld", "Bash"]], 
            "standard": [["OpenWorld", "Dash"]]
        }
    },
    "ValleyTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "ValleyPostStompDoor": {
            "casual": [["Bash"], ["Glide"]], 
            "expert": [["ChargeDash", ("EnergyCell", 3)], ["ChargeDash", "DoubleJump"]], 
            "master": [["DoubleJump"]]
        },
        "ValleyRight": {
            "casual": [["Bash"], ["Climb", "ChargeJump", "Glide"], ["WallJump", "DoubleJump", "Glide"], ["Climb", "DoubleJump", "Glide"]], 
            "expert": [["WallJump", "DoubleJump", ("HealthCell", 4)], ["Climb", "DoubleJump", ("HealthCell", 4)], ["WallJump", "Glide", ("HealthCell", 4)], ["Climb", "Glide", ("HealthCell", 4)], ["ChargeDash"]], 
            "master": [["GrenadeJump"], ["TripleJump"]]
        },
        "MistyEntrance": {
            "casual": [["Glide", "OpenWorld"]], 
            "standard": [["Bash", "Grenade", "DoubleJump", "OpenWorld"], ["ChargeJump", "DoubleJump", "AirDash", "OpenWorld"]], 
            "expert": [["Bash", "Grenade", "OpenWorld"], ["Bash", "ChargeJump", "DoubleJump", "OpenWorld"], ["Dash", "ChargeJump", "DoubleJump", "OpenWorld"], ["AirDash", "DoubleJump", "OpenWorld"], ["ChargeDash", "OpenWorld"]]
        },
        "LowerValley": {
            "casual": [["OpenWorld"]]
        },
        "LowerValleyPlantApproach": {
            "casual": [["OpenWorld"]]
        },
        "ValleyStompless": {
            "casual": [["Glide", "Wind", "OpenWorld"], ["Climb", "ChargeJump", "OpenWorld"]], 
            "expert": [["Climb", "Bash", "Grenade", "OpenWorld"], ["WallJump", "Bash", "Grenade", "OpenWorld"], ["ChargeDash", "OpenWorld"]], 
            "master": [["WallJump", "TripleJump", "OpenWorld"], ["Lure", "Bash", "WallJump", "OpenWorld"]]
        }
    },
    "ValleyRight": { 
        "ValleyPostStompDoor": {
            "casual": [["None"]],
            "expert": [["DoubleJump", ("HealthCell", 4)]], 
            "master": [[("HealthCell", 7)], [("HealthCell", 5), "UltraDefense"]]
        },
        "ValleyStomplessApproach": {
            "casual": [["WallJump", "DoubleJump"], ["WallJump", "Bash"], ["Climb", "ChargeJump"], ["Climb", "DoubleJump", "Bash"], ["Bash", "Grenade", "Climb"], ["Glide", "Wind"]], 
            "expert": [["WallJump", "ChargeDash"]]
        }
    },
    "ValleyStomplessApproach": { 
        "ValleyStompless": {
            "casual": [["Bash"]], 
            "expert": [["ChargeJump", "WallJump", "DoubleJump", ("HealthCell", 4)], ["ChargeJump", "Climb", "DoubleJump", ("HealthCell", 4)], ["ChargeDash", "WallJump", "DoubleJump", ("EnergyCell", 2)], ["ChargeDash", "Climb", "DoubleJump", ("EnergyCell", 2)]], 
            "master": [["WallJump", "TripleJump", ("HealthCell", 3)]]
        },
        "ValleyRight": {
            "casual": [["Free"]]
        }
    },
    "ValleyStompless": { 
        "WilhelmLedge": {
            "casual": [["Wind", "Glide"], ["Bash"]], 
            "expert": [["ChargeDash", ("EnergyCell", 2)], ["ChargeDash", "DoubleJump"]]
        },
        "ValleyMain": {
            "casual": [["None"]],
            "expert": [["Bash"]], 
            "master": [["ChargeFlame"], ["Grenade"]]
        },
        "ValleyStomplessApproach": {
            "casual": [["Glide"], ["Bash"]], 
            "expert": [["DoubleJump", ("HealthCell", 4)], ["AirDash", ("HealthCell", 4)], ["ChargeDash", ("EnergyCell", 3)]], 
            "master": [["ChargeJump", ("HealthCell", 7)], ["ChargeJump", ("HealthCell", 5), "UltraDefense"], [("HealthCell", 10)], [("HealthCell", 7), "UltraDefense"]]
        },
        "MistyEntrance": {
            "casual": [["Glide", "OpenWorld"], ["Bash", "OpenWorld"], ["DoubleJump", "OpenWorld"], ["Climb", "ChargeJump", "OpenWorld"], ["Dash", "OpenWorld"]]
        },
        "LowerValley": {
            "casual": [["OpenWorld"]]
        },
        "LowerValleyPlantApproach": {
            "casual": [["OpenWorld"]]
        }
    },
    "ValleyMain": { 
        "WilhelmLedge": {
            "casual": [["Wind", "Glide"], ["Bash"]], 
            "expert": [["ChargeDash", ("EnergyCell", 2)]], 
            "master": [["GrenadeJump"]]
        },
        "MistyEntrance": {
            "casual": [["Glide"], ["Bash"], ["DoubleJump"], ["Climb", "ChargeJump"], ["Dash"]]
        },
        "LowerValley": {
            "casual": [["Free"]]
        },
        "LowerValleyPlantApproach": {
            "casual": [["Free"]]
        },
        "ValleyStompless": {
            "casual": [["Free"]]
        }
    },
    "LowerValley": { 
        "LowerValleyPlantApproach": {
            "casual": [["Bash", "DoubleJump"], ["Bash", "Glide"], ["Bash", "Grenade"], ["ChargeJump", "DoubleJump"], ["ChargeJump", "Glide"], ["Glide", "Wind"]], 
            "standard": [["Lure", "Bash"]]
        },
        "ValleyThreeBirdLever": {
            "casual": [["Glide", "Wind"], ["Glide", "DoubleJump"]], 
            "standard": [["Dash", "DoubleJump"], ["Dash", "Glide"], ["Lure", "Bash", "Glide"], ["Lure", "Bash", "DoubleJump"], [("HealthCell", 4)]], 
            "expert": [[("HealthCell", 2)], ["DoubleBash"]]
        },
        "MistyEntrance": {
            "casual": [["Glide", "Wind"], ["Climb", "ChargeJump"]], 
            "standard": [["Climb", "Bash", "Grenade"]], 
            "expert": [["ChargeDash"], ["DoubleBash", "WallJump"], ["DoubleBash", "Climb"]], 
            "master": [["Lure", "Bash"]]
        },
        "ValleyTeleporter": {
            "casual": [["Glide", "Wind", "OpenWorld"], ["Climb", "ChargeJump", "Glide", "OpenWorld"], ["Climb", "ChargeJump", "DoubleJump", "OpenWorld"], ["Climb", "ChargeJump", "Bash", "OpenWorld"]], 
            "standard": [["Climb", "Bash", "Grenade", "OpenWorld"], ["Bash", "Grenade", "WallJump", "DoubleJump", "OpenWorld"], ["ChargeJump", "WallJump", "DoubleJump", "OpenWorld"]], 
            "expert": [["ChargeDash", "OpenWorld"]], 
            "master": [["Lure", "Bash", "OpenWorld"]]
        }
    },
    "LowerValleyPlantApproach": {
    },
    "ValleyThreeBirdLever": { 
        "ValleyEntry": {
            "casual": [["Glide"], ["DoubleJump"], ["Bash"], ["Climb", "ChargeJump"]], 
            "standard": [["AirDash"], [("HealthCell", 7)]], 
            "expert": [["ChargeJump", ("HealthCell", 2)], ["WallJump", ("HealthCell", 2)], ["Climb", ("HealthCell", 2)]]
        },
        "LowerValley": {
            "casual": [["Glide", "Wind"], ["Glide", "DoubleJump"]], 
            "standard": [["Dash", "DoubleJump"], ["Dash", "Glide"], ["AirDash"], [("HealthCell", 7)]], 
            "expert": [[("HealthCell", 5)], ["DoubleBash"]]
        },
        "ValleyStompFloor": {
            "casual": [["Free"]]
        }
    },
    "ValleyStompFloor": { 
        "ValleyForlornApproach": {
            "casual": [["Stomp"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["Lure", "Bash"]]
        },
        "ValleyThreeBirdLever": {
            "casual": [["Bash"], ["ChargeJump", "Climb"], ["ChargeJump", "WallJump", "DoubleJump"]]
        },
        "ValleyEntry": {
            "casual": [["Bash", "OpenWorld"], ["ChargeJump", "DoubleJump", "OpenWorld"], ["ChargeJump", "Glide", "OpenWorld"]], 
            "standard": [["ChargeJump", ("HealthCell", 4), "OpenWorld"]], 
            "expert": [["ChargeJump", ("HealthCell", 3), "OpenWorld"], ["DoubleJump", ("HealthCell", 3), "OpenWorld"], ["ChargeDash", "OpenWorld"]]
        }
    },
    "ValleyForlornApproach": { 
        "OutsideForlornCliff": {
            "casual": [["ChargeJump"], ["Bash"]], 
            "standard": [["Stomp"]]
        },
        "ValleyStompFloor": {
            "casual": [["None"]],
            "expert": [["ChargeJump"]], 
            "casual": [["ChargeJump", "DoubleJump"], ["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["ChargeJump", "Bash", "Grenade"]], 
            "master": [["Bash"]]
        }
    },
    "OutsideForlornCliff": { 
        "ValleyForlornApproach": {
            "casual": [["Stomp", "Bash", "WallJump"], ["Stomp", "Bash", "Climb", "DoubleJump"], ["Stomp", "Bash", "ChargeJump"], ["Stomp", "Bash", "Grenade"]], 
            "expert": [["Stomp", "ChargeFlame", "WallJump"], ["Stomp", "ChargeFlame", "Climb", "DoubleJump"], ["Stomp", "ChargeFlame", "ChargeJump"]], 
            "master": [["Bash"]]
        },
        "OutsideForlorn": {
            "casual": [["Free"]]
        }
    },
    "OutsideForlorn": { 
        "OutsideForlornCliff": {
            "casual": [["WallJump", "ChargeJump"], ["Climb", "ChargeJump"], ["Bash", "Glide"], ["Bash", "DoubleJump"], ["Bash", "Grenade"]], 
            "expert": [["ChargeDash"], ["DoubleBash"]], 
            "master": [["ChargeJump", "DoubleJump"]]
        },
        "ForlornOuterDoor": {
            "casual": [["ForlornKey"]]
        },
        "RightForlorn": {
            "casual": [["None"]],
            "glitched": [["Free"]]
        }
    },
    "ForlornOuterDoor": { 
        "ForlornInnerDoor": {
            "casual": [["Free"]]
        },
        "OutsideForlorn": {
            "casual": [["Free"]]
        }
    },
    "ForlornInnerDoor": { 
        "ForlornOuterDoor": {
            "casual": [["ForlornKey"]]
        },
        "ForlornOrbPossession": {
            "casual": [["DoubleJump", "Open"], ["Glide", "Climb", "Open"], ["Glide", "WallJump", "Open"], ["ChargeJump", "Open"], ["Bash", "Grenade", "Open"]], 
            "standard": [["Dash", "Climb", "Open"], ["Dash", "WallJump", "Open"]], 
            "expert": [["Open"]]
        },
        "ForlornGravityRoom": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["Climb", "DoubleJump", "Glide"], ["Bash", "Grenade"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [["Dash", "DoubleJump", "WallJump"], ["Dash", "DoubleJump", "Climb"], ["ChargeJump", ("HealthCell", 4)], ["WallJump", "DoubleJump", ("HealthCell", 4)], ["Climb", "DoubleJump", ("HealthCell", 4)], ["ChargeJump", "AirDash"]], 
            "expert": [["ChargeJump"], ["WallJump", ("HealthCell", 4)]], 
            "master": [["WallJump", ("HealthCell", 3), "UltraDefense"]]
        }
    },
    "ForlornOrbPossession": { 
        "ForlornPlantAccess": {
            "casual": [["Free"]]
        },
        "ForlornMapArea": {
            "casual": [["Free"]]
        },
        "ForlornKeyDoor": {
            "casual": [["Free"]]
        },
        "ForlornInnerDoor": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["Climb", "DoubleJump", "Glide"], ["Bash"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [[("HealthCell", 4)], ["Dash", "DoubleJump"], ["ChargeJump", "AirDash"]], 
            "expert": [["ChargeJump"]], 
            "master": [[("HealthCell", 3), "UltraDefense"]]
        }
    },
    "ForlornGravityRoom": { 
        "ForlornMapArea": {
            "casual": [["Bash", "Grenade"], ["ChargeJump"], ["Climb", "DoubleJump"], ["WallJump", "DoubleJump"]], 
            "master": [["DoubleJump"], ["Lure", "Bash"]]
        },
        "ForlornInnerDoor": {
            "casual": [["WallJump", "DoubleJump", "Glide"], ["Climb", "DoubleJump", "Glide"], ["Bash"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [[("HealthCell", 4)], ["Dash", "DoubleJump"], ["ChargeJump", "AirDash"]], 
            "expert": [["ChargeJump"]], 
            "master": [[("HealthCell", 3), "UltraDefense"]]
        }
    },
    "ForlornMapArea": { 
        "ForlornTeleporter": {
            "casual": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["Bash", "Grenade"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [["WallJump", "AirDash", "Glide"], ["Climb", "AirDash", "Glide"], ["ChargeJump", "AirDash"], ["ChargeJump", ("HealthCell", 4)]], 
            "master": [["DoubleJump"], ["Lure", "Bash"], ["ChargeJump", ("HealthCell", 3), "UltraDefense"]]
        },
        "ForlornPlantAccess": {
            "casual": [["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "master": [["ChargeJump", "DoubleJump"], ["Bash", "Grenade", "DoubleJump"]]
        },
        "ForlornKeyDoor": {
            "casual": [["Free"]]
        },
        "ForlornGravityRoom": {
            "casual": [["Free"]]
        }
    },
    "ForlornTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "ForlornOrbPossession": {
            "casual": [["Open"]]
        },
        "ForlornMapArea": {
            "casual": [["WallJump"], ["Climb"], ["ChargeJump"], ["Bash", "Grenade"], ["DoubleJump"], ["Glide"]]
        },
        "ForlornGravityRoom": {
            "casual": [["Free"]]
        }
    },
    "ForlornPlantAccess": {
    },
    "ForlornKeyDoor": { 
        "ForlornLaserRoom": {
            "casual": [[("KeyStone", 40)], [("ForlornKeyStone", 4)]]
        }
    },
    "ForlornLaserRoom": { 
        "ForlornStompDoor": {
            "casual": [["Stomp", "Bash", "Grenade"], ["Stomp", "ChargeJump", "Glide"]], 
            "standard": [["Stomp", "ChargeJump", "AirDash", "DoubleJump"], ["Stomp", "ChargeJump", "AirDash", ("HealthCell", 4)], ["Stomp", "Glide", "AirDash", "DoubleJump", ("HealthCell", 4)], ["Stomp", "ChargeJump", "DoubleJump", ("HealthCell", 4)]], 
            "expert": [["Stomp", "ChargeDash", "WallJump"], ["Stomp", "ChargeDash", "Climb"], ["Stomp", "ChargeDash", "DoubleJump"], ["Stomp", "ChargeDash", "ChargeJump"]], 
            "master": [["Stomp", "ChargeJump", "TripleJump"], ["Stomp", "Glide", "TripleJump"], ["Lure", "Stomp", "Bash"], ["Stomp", "GrenadeJump"]]
        }
    },
    "ForlornStompDoor": { 
        "RightForlorn": {
            "casual": [["WallJump", "Bash"], ["Climb", "Bash"], ["ChargeJump", "Bash"], ["DoubleJump", "Bash"], ["Bash", "Grenade"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [["ChargeJump", "AirDash"], ["WallJump", "DoubleJump", "AirDash"], ["Climb", "DoubleJump", "AirDash"], ["WallJump", "DoubleJump", ("HealthCell", 4)], ["Climb", "DoubleJump", ("HealthCell", 4)]], 
            "expert": [["WallJump", ("HealthCell", 4)], ["Climb", ("HealthCell", 4)]], 
            "master": [["WallJump", ("HealthCell", 3), "UltraDefense"], ["Climb", ("HealthCell", 3), "UltraDefense"], ["Lure", "Bash"], ["TripleJump"]]
        }
    },
    "RightForlorn": {
    },
    "WilhelmLedge": { 
        "SorrowBashLedge": {
            "casual": [["Bash"], ["Wind", "Glide"], ["ChargeJump", "Glide", "Climb"], ["ChargeJump", "Glide", "WallJump"], ["Dash", "DoubleJump", "WallJump"]], 
            "standard": [["Dash", "DoubleJump", "Glide", "Climb"]], 
            "expert": [["ChargeDash", "WallJump"], ["ChargeDash", "Climb"]], 
            "master": [["WallJump", "TripleJump"], ["Climb", "TripleJump"]]
        },
        "ValleyStompless": {
            "casual": [["Glide"], ["Bash"]], 
            "standard": [["DoubleJump", "AirDash"]], 
            "expert": [["ChargeDash"]], 
            "master": [["TripleJump"]]
        },
        "ValleyMain": {
            "casual": [["Stomp"]], 
            "standard": [["Lure", "HoruKey"], ["Climb", "ChargeJump"]], 
            "expert": [["ChargeJump", "Bash", "Grenade"]], 
            "master": [["ChargeJump", "AirDash"], ["Bash"]], 
            "glitched": [["ChargeJump"]]
        }
    },
    "SorrowBashLedge": { 
        "LowerSorrow": {
            "casual": [["Wind", "Glide"]], 
            "expert": [["Lure", "Glide", "DoubleJump", "Bash", "Dash", "WallJump"], ["Lure", "Glide", "DoubleJump", "Bash", "Dash", "Climb"], ["DoubleBash"], ["ChargeJump", "WallJump", ("HealthCell", 9)], ["ChargeJump", "Climb", ("HealthCell", 9)]], 
            "master": [["ChargeJump", "WallJump", ("HealthCell", 7), "UltraDefense"], ["ChargeJump", "Climb", ("HealthCell", 7), "UltraDefense"], ["WallJump", "TripleJump", ("HealthCell", 13), "UltraDefense"]]
        }
    },
    "LowerSorrow": { 
        "WilhelmLedge": {
            "casual": [["Glide", "DoubleJump"], ["Glide", "Wind"]], 
            "standard": [["Glide", "AirDash"], ["BashGrenade", "DoubleJump"], ["BashGrenade", "Glide"], ["BashGrenade", "AirDash"]], 
            "expert": [["Glide", ("HealthCell", 5)], ["DoubleJump", ("HealthCell", 5)], ["ChargeDash", ("EnergyCell", 2)], ["ChargeDash", "Stomp"], ["ChargeDash", "Bash"], ["BashGrenade", ("HealthCell", 5)], ["DoubleBash"]], 
            "master": [["AirDash", "DoubleJump"], ["Glide", ("HealthCell", 4), "UltraDefense"], ["DoubleJump", ("HealthCell", 4), "UltraDefense"], ["TripleJump"]]
        },
        "SorrowMainShaftKeystoneArea": {
            "casual": [["Glide"], ["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["Bash", "WallJump"], ["Bash", "Climb"]], 
            "expert": [["ChargeDash"], ["DoubleBash"]]
        },
        "SorrowMapstoneArea": {
            "casual": [["ChargeJump", "WallJump"], ["ChargeJump", "Climb"], ["Bash", "WallJump"], ["Bash", "Climb"]], 
            "standard": [["Lure", "WallJump", "Glide"], ["Lure", "Climb", "Glide"]], 
            "expert": [["DoubleBash"]]
        },
        "LeftSorrowLowerDoor": {
            "casual": [[("KeyStone", 36)], [("SorrowKeyStone", 8)]]
        },
        "LeftSorrow": {
            "casual": [["Glide", "Bash"], ["Glide", "ChargeJump"]], 
            "master": [["GrenadeJump"], ["ChargeJump", ("HealthCell", 10), "UltraDefense"], ["ChargeJump", "TripleJump"]], 
            "expert": [["ChargeDash", "Bash"], ["ChargeDash", "ChargeJump", ("EnergyCell", 2)], ["ChargeDash", "Stomp", "ChargeJump"], ["ChargeDash", "DoubleJump", "ChargeJump"], ["DoubleBash"]]
        },
        "MiddleSorrow": {
            "casual": [["Climb", "ChargeJump"]], 
            "expert": [["Bash", "Glide"], ["ChargeDash"]], 
            "master": [["Bash"]], 
            "glitched": [["ChargeJump", "Glide"]]
        },
        "SunstoneArea": {
            "casual": [["None"]],
            "expert": [["DoubleBash", "Glide"]]
        }
    },
    "SorrowMainShaftKeystoneArea": { 
        "LowerSorrow": {
            "casual": [["Free"]]
        }
    },
    "SorrowMapstoneArea": { 
        "HoruInnerEntrance": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        },
        "LowerSorrow": {
            "casual": [["Stomp"], ["Climb", "ChargeJump"], ["Bash"]], 
            "standard": [["Lure", "Free"]]
        }
    },
    "LeftSorrowLowerDoor": { 
        "LeftSorrow": {
            "casual": [["Glide", "Bash", "Stomp"]], 
            "standard": [["Bash", "ChargeJump", "Stomp", "WallJump"], ["Bash", "ChargeJump", "Stomp", "Climb"], ["ChargeJump", "Climb", "DoubleJump"]], 
            "expert": [["ChargeJump", "Climb", ("HealthCell", 5)], ["DoubleBash", "Stomp", ("HealthCell", 5)], ["DoubleBash", "Grenade", "Stomp"], ["DoubleBash", "DoubleJump", "Stomp"]]
        }
    },
    "LeftSorrow": { 
        "LeftSorrowKeystones": {
            "casual": [["Glide"], ["ChargeJump", "Climb", "DoubleJump"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "expert": [["ChargeJump", "WallJump", ("HealthCell", 5)]], 
            "master": [["ChargeJump", "WallJump", ("HealthCell", 4), "UltraDefense"], ["TripleJump", "WallJump"], ["TripleJump", "Climb"], ["Bash"]]
        }
    },
    "LeftSorrowKeystones": { 
        "LeftSorrowMiddleDoorClosed": {
            "casual": [["Free"]]
        },
        "MiddleSorrow": {
            "casual": [["None"]],
            "standard": [["Bash", "Dash", "DoubleJump", "Climb"], ["Bash", "Dash", "DoubleJump", "WallJump"]], 
            "expert": [["Bash", "ChargeDash", "Climb"], ["Bash", "ChargeDash", "WallJump"], ["DoubleBash"]], 
            "master": [["ChargeJump", "Stomp", "Glide", "TripleJump", "WallJump"], ["ChargeJump", "Stomp", "AirDash", "Climb"], ["ChargeJump", "Stomp", "ChargeDash", "WallJump"], ["ChargeJump", "Stomp", "TripleJump", "Climb"]]
        },
        "LeftSorrow": {
            "casual": [["Glide"]], 
            "standard": [["AirDash"], ["DoubleJump"], ["BashGrenade"], ["Climb", "ChargeJump"]], 
            "expert": [[("HealthCell", 5)]]
        }
    },
    "LeftSorrowMiddleDoorClosed": { 
        "LeftSorrowMiddleDoorOpen": {
            "casual": [[("KeyStone", 36)], [("SorrowKeyStone", 8)]]
        }
    },
    "LeftSorrowMiddleDoorOpen": { 
        "MiddleSorrow": {
            "casual": [["Glide", "Bash", "Stomp", "WallJump"], ["Glide", "Bash", "Stomp", "Climb"], ["DoubleJump", "Bash", "Stomp", "WallJump"], ["DoubleJump", "Bash", "Stomp", "Climb"]], 
            "standard": [["Bash", "Stomp", "WallJump"], ["Bash", "Stomp", "Climb"], ["Bash", "Stomp", "DoubleJump"]], 
            "expert": [["ChargeJump", "Climb", "DoubleJump", "Bash", ("HealthCell", 5)]], 
            "master": [["Bash", "ChargeDash", "Stomp"], ["Bash", "ChargeDash", "ChargeJump", "Climb"], ["Bash", "Climb", "ChargeJump", "TripleJump", ("HealthCell", 4), "UltraDefense"]], 
            "glitched": [["Dash"]]
        },
        "LeftSorrowKeystones": {
            "casual": [["Stomp", "DoubleJump"], ["Climb", "ChargeJump", "DoubleJump"]], 
            "standard": [["Stomp", "BashGrenade"], ["Climb", "ChargeJump"], ["Stomp", "AirDash", "Climb"], ["Stomp", "AirDash", "WallJump"]], 
            "expert": [["Stomp", "Dash", "Climb"], ["Stomp", "Dash", "WallJump"], ["Stomp", "ChargeDash", ("EnergyCell", 1)], ["Stomp", ("HealthCell", 5)], ["BashGrenade", "ChargeJump"]]
        }
    },
    "MiddleSorrow": { 
        "UpperSorrow": {
            "casual": [["Glide"], ["Bash", "Grenade", "WallJump"], ["Bash", "Grenade", "Climb"]], 
            "master": [["GrenadeJump"], ["ChargeJump", "Climb", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "WallJump", ("HealthCell", 4), "UltraDefense"]], 
            "expert": [["ChargeJump", "Climb", ("HealthCell", 5)], ["ChargeJump", "WallJump", ("HealthCell", 5)]]
        },
        "LeftSorrow": {
            "casual": [["None"]],
            "expert": [["ChargeDash", "Stomp", "WallJump"], ["ChargeDash", "Stomp", "Climb"]]
        },
        "LeftSorrowKeystones": {
            "casual": [["None"]],
            "expert": [["ChargeDash", "Stomp", "WallJump"], ["ChargeDash", "Stomp", "Climb"]]
        },
        "SorrowMainShaftKeystoneArea": {
            "casual": [["Stomp"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["ChargeJump", "Bash", "Grenade"], ["ChargeJump", "AirDash"]]
        },
        "LowerSorrow": {
            "casual": [["Stomp"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["ChargeJump", "Bash", "Grenade"], ["ChargeJump", "AirDash"]]
        },
        "SunstoneArea": {
            "casual": [["None"]],
            "expert": [["Bash", "Glide"]]
        }
    },
    "UpperSorrow": { 
        "MiddleSorrow": {
            "casual": [["Free"]]
        },
        "SunstoneArea": {
            "casual": [["None"]],
            "glitched": [["Glide", "ChargeJump"]]
        },
        "SorrowTeleporter": {
            "casual": [["None"]],
            "glitched": [["Glide", "ChargeJump", "Climb"]]
        },
        "ChargeJumpDoor": {
            "casual": [["Free"]]
        }
    },
    "ChargeJumpDoor": { 
        "ChargeJumpDoorOpen": {
            "casual": [[("KeyStone", 40)], [("SorrowKeyStone", 12)]]
        }
    },
    "ChargeJumpDoorOpen": { 
        "ChargeJumpArea": {
            "casual": [["Glide"]], 
            "master": [["ChargeJump", "TripleJump", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "WallJump", "TripleJump", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["Bash", "Grenade", "ChargeJump", "TripleJump", ("HealthCell", 7), "UltraDefense"], ["ChargeJump", "TripleJump", ("HealthCell", 10), "UltraDefense"], ["Bash", "Grenade", "WallJump", "TripleJump", ("HealthCell", 13), "UltraDefense"]]
        }
    },
    "ChargeJumpArea": { 
        "AboveChargeJumpArea": {
            "casual": [["ChargeJump", "Bash", "Climb"], ["ChargeJump", "Bash", "DoubleJump", "WallJump"]], 
            "master": [["GrenadeJump"], ["Bash", "Climb"], ["Bash", "WallJump"]], 
            "expert": [["ChargeJump", "Bash", "WallJump", ("HealthCell", 5)], ["ChargeJump", "Dash", ("HealthCell", 5)], ["ChargeJump", "ChargeDash", "Climb"]]
        },
        "ChargeJumpDoor": {
            "casual": [["Open"]]
        }
    },
    "AboveChargeJumpArea": { 
        "SorrowTeleporter": {
            "casual": [["ChargeJump", "Climb"], ["Bash", "WallJump", "DoubleJump", "Glide"], ["Bash", "Climb", "Grenade"]], 
            "expert": [["ChargeJump", "WallJump", "Dash", ("HealthCell", 5)]], 
            "master": [["Bash"]]
        },
        "ChargeJumpArea": {
            "casual": [["None"]],
            "standard": [["Lure", "Bash", "Stomp", "WallJump"], ["Lure", "Bash", "Stomp", "Climb"]], 
            "expert": [["ChargeJump", "Climb", "Bash"], ["ChargeJump", "Bash", "Grenade", "WallJump"], ["ChargeJump", "Bash", "AirDash"], ["ChargeJump", "Climb", "ChargeDash"], ["ChargeDash", "Stomp", "WallJump"], ["ChargeDash", "Stomp", "Climb"], ["ChargeJump", "ChargeDash", ("HealthCell", 6)], ["ChargeJump", "Bash", ("HealthCell", 6)], ["DoubleBash", "WallJump"], ["DoubleBash", "Climb"]], 
            "master": [["GrenadeJump", "Dash"], ["GrenadeJump", ("HealthCell", 6)], ["Bash"]]
        }
    },
    "SorrowTeleporter": { 
        "TeleporterNetwork": {
            "casual": [["Free"]]
        },
        "BelowSunstoneArea": {
            "casual": [["ChargeJump", "Climb", "DoubleJump"]], 
            "standard": [["ChargeJump", "Climb", "Glide"], ["ChargeJump", "Climb", "Bash"]], 
            "master": [["GrenadeJump"], ["Stomp", "Bash", "Climb"], ["Stomp", "Bash", "WallJump"], ["ChargeJump", "Bash"], ["ChargeJump", "Climb", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "WallJump", "Glide", ("HealthCell", 4), "UltraDefense"], ["ChargeJump", "WallJump", "ChargeDash", ("HealthCell", 4), "UltraDefense"], ["WallJump", "TripleJump", "Stomp", ("HealthCell", 4), "UltraDefense"]], 
            "expert": [["ChargeJump", "Climb", ("HealthCell", 5)], ["Stomp", "Bash", "Grenade", ("HealthCell", 5)], ["ChargeJump", "WallJump", "Glide", ("HealthCell", 5)], ["ChargeJump", "WallJump", "AirDash", ("HealthCell", 5)]]
        },
        "AboveChargeJumpArea": {
            "casual": [["ChargeJump", "Climb", "Stomp"]], 
            "standard": [["ChargeJump", "Climb"]], 
            "expert": [["Stomp", "WallJump", "DoubleJump", "Glide"], ["ChargeJump", "WallJump", "DoubleJump", "Glide", "Bash", "Grenade"], ["ChargeJump", "AirDash", "WallJump", "DoubleJump"], ["ChargeJump", "WallJump", "DoubleJump", "Glide", ("HealthCell", 5)]], 
            "master": [["Stomp", "Bash"], ["ChargeJump", "Bash"]]
        }
    },
    "BelowSunstoneArea": { 
        "SunstoneArea": {
            "casual": [["Stomp", "Glide"]], 
            "standard": [["ChargeJump", "Climb", "Glide"]], 
            "expert": [["ChargeJump", "Dash", "Glide"], ["ChargeJump", "Bash", "Grenade", "Glide"]], 
            "master": [["GrenadeJump"], ["Bash"], ["ChargeJump", "Climb", "TripleJump", ("HealthCell", 4), "UltraDefense"]]
        },
        "UpperSorrow": {
            "casual": [["Stomp"]], 
            "standard": [["ChargeJump", "Climb"]], 
            "expert": [["ChargeJump", "Bash", "Grenade"], ["ChargeJump", "AirDash"]], 
            "master": [["Bash"]]
        }
    },
    "SunstoneArea": { 
        "UpperSorrow": {
            "casual": [["Stomp"]], 
            "standard": [["Climb", "ChargeJump"]]
        },
        "SorrowTeleporter": {
            "casual": [["Climb", "ChargeJump", "DoubleJump"]], 
            "expert": [["ChargeJump", "WallJump", "DoubleJump", ("HealthCell", 5)]]
        }
    },
    "MistyEntrance": { 
        "MistyPostFeatherTutorial": {
            "casual": [["WallJump", "Bash", "Glide"], ["Bash", "Glide", "Climb"], ["DoubleJump", "Bash", "Glide"]], 
            "standard": [["Bash", "Glide"], ["DoubleJump", "Glide", "Climb", "ChargeJump", "AirDash"], ["DoubleJump", "Glide", "WallJump", "ChargeJump", "AirDash"]], 
            "expert": [["DoubleJump", "Glide", "Climb", "ChargeJump"], ["WallJump", "ChargeJump", ("HealthCell", 7)], ["DoubleJump", "ChargeJump", ("HealthCell", 4)], ["DoubleJump", "Glide", "ChargeJump", "AirDash"], ["ChargeDash", ("EnergyCell", 4)]], 
            "master": [["Bash"], ["GrenadeJump", ("HealthCell", 4)]]
        },
        "ValleyTeleporter": {
            "casual": [["Glide", "Wind", "OpenWorld"], ["ChargeJump", "Glide", "DoubleJump", "WallJump", "OpenWorld"], ["ChargeJump", "Glide", "DoubleJump", "Climb", "OpenWorld"]], 
            "standard": [["BashGrenade", "DoubleJump", "WallJump", "OpenWorld"], ["BashGrenade", "DoubleJump", "Climb", "OpenWorld"], ["BashGrenade", "AirDash", "WallJump", "OpenWorld"], ["BashGrenade", "AirDash", "Climb", "OpenWorld"]], 
            "expert": [["BashGrenade", "AirDash", "OpenWorld"], ["BashGrenade", "DoubleJump", "OpenWorld"]]
        },
        "LowerValley": {
            "casual": [["OpenWorld"]]
        }
    },
    "MistyPostFeatherTutorial": { 
        "MistyPostKeystone1": {
            "casual": [["Free"]]
        }
    },
    "MistyPostKeystone1": { 
        "MistyPreMortarCorridor": {
            "casual": [["Bash", "Glide"]], 
            "expert": [["Glide"], [("HealthCell", 9)], ["DoubleJump", ("HealthCell", 4)], ["AirDash", ("HealthCell", 4)]], 
            "master": [["Bash"], ["DoubleJump", "ChargeDash"], ["TripleJump"], ["UltraDefense", ("HealthCell", 4)], [("HealthCell", 6)]]
        }
    },
    "MistyPreMortarCorridor": { 
        "MistyPostMortarCorridor": {
            "casual": [["Glide"]], 
            "expert": [["DoubleJump", "AirDash", ("HealthCell", 4)], ["DoubleJump", "ChargeJump", ("HealthCell", 4)]], 
            "master": [["DoubleJump", "Bash", "Grenade"], ["ChargeDash"], [("HealthCell", 9), "UltraDefense"], [("HealthCell", 10)]]
        },
        "RightForlorn": {
            "casual": [["None"]],
            "glitched": [["Free"]]
        }
    },
    "MistyPostMortarCorridor": { 
        "MistyPrePlantLedge": {
            "casual": [["Bash"]], 
            "standard": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["WallJump", "ChargeJump"], ["Climb", "ChargeJump"]], 
            "master": [["DoubleJump"], ["ChargeDash"]]
        }
    },
    "MistyPrePlantLedge": { 
        "MistyPreClimb": {
            "casual": [["ChargeJump"], ["WallJump", "Glide", "DoubleJump"], ["Climb", "Glide", "DoubleJump"]], 
            "standard": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"]], 
            "expert": [["WallJump", "Bash"], ["Climb", "Bash"]], 
            "master": [["DoubleJump"], ["Bash"]]
        }
    },
    "MistyPreClimb": { 
        "MistyPostClimb": {
            "casual": [["Climb", "DoubleJump", "Stomp"], ["Climb", "ChargeJump"], ["Bash", "Grenade", "Stomp"]], 
            "expert": [["Bash", "Grenade", "WallJump", "DoubleJump"], ["Bash", "Grenade", "Climb", "DoubleJump"]], 
            "master": [["DoubleJump", "Stomp"], ["Bash", "Grenade", "DoubleJump"]]
        },
        "ForlornTeleporter": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        },
        "RightForlorn": {
            "casual": [["None"]],
            "glitched": [["Dash"]]
        }
    },
    "MistyPostClimb": { 
        "MistySpikeCave": {
            "casual": [["WallJump", "Climb", "DoubleJump"]], 
            "standard": [["Climb", "ChargeJump"]], 
            "expert": [["ChargeJump"], ["Bash", "ChargeDash"], ["DoubleBash"]], 
            "master": [["DoubleJump"]]
        }
    },
    "MistySpikeCave": { 
        "MistyKeystone3Ledge": {
            "casual": [["WallJump", "Climb", "DoubleJump"]], 
            "standard": [["Bash", "Glide", "DoubleJump"]], 
            "expert": [["DoubleJump"]], 
            "master": [["Bash"], ["ChargeJump", ("HealthCell", 4)]]
        }
    },
    "MistyKeystone3Ledge": { 
        "MistyPreLasers": {
            "casual": [["Glide"]], 
            "standard": [["ChargeDash"], ["TripleJump"]], 
            "expert": [["Dash", "DoubleJump"], ["Bash", "Grenade"], ["DoubleJump", ("HealthCell", 4)], ["ChargeJump", ("HealthCell", 4)]], 
            "master": [["WallJump", ("HealthCell", 7)], ["GrenadeJump"]]
        }
    },
    "MistyPreLasers": { 
        "MistyPostLasers": {
            "casual": [["WallJump", "Climb", "Glide"]], 
            "standard": [["WallJump", "DoubleJump"], ["Climb", "DoubleJump"], ["ChargeJump", "Glide"], ["ChargeJump", "DoubleJump"]], 
            "expert": [["Dash", "WallJump"], ["Dash", "Climb"], ["Dash", "ChargeJump"], ["Bash", "Grenade"]], 
            "master": [["DoubleJump"], ["Bash"]]
        }
    },
    "MistyPostLasers": { 
        "MistyMortarSpikeCave": {
            "casual": [["Bash", "Glide", "DoubleJump"]], 
            "standard": [["Bash", "Glide"]], 
            "expert": [["Glide"]], 
            "master": [["Bash"]]
        }
    },
    "MistyMortarSpikeCave": { 
        "MistyKeystone4Ledge": {
            "casual": [["WallJump", "Bash", "Glide"], ["Climb", "Bash", "Glide"]], 
            "standard": [["Bash", "Glide", "DoubleJump"]], 
            "expert": [["Bash", "Glide"], ["Bash", "ChargeDash"]], 
            "master": [["Bash"], ["ChargeJump", "TripleJump"], ["ChargeDash"]]
        }
    },
    "MistyKeystone4Ledge": { 
        "MistyBeforeDocks": {
            "casual": [["WallJump", "DoubleJump", "Bash", "Glide"], ["Climb", "DoubleJump", "Bash", "Glide"], ["Climb", "ChargeJump", "Bash", "Glide"]], 
            "standard": [["WallJump", "Bash", "DoubleJump"], ["Climb", "Bash", "DoubleJump"]], 
            "master": [["ChargeDash"], ["ChargeJump", "DoubleJump", ("HealthCell", 10)], ["Lure", "Bash"]]
        }
    },
    "MistyBeforeDocks": { 
        "MistyAbove200xp": {
            "casual": [["ChargeJump", "Climb"], ["ChargeJump", "WallJump"], ["ChargeJump", "DoubleJump"], ["Bash", "Glide", "Climb", "DoubleJump"]], 
            "standard": [["ChargeJump", "Glide"], ["ChargeJump", "AirDash"], ["Bash", "ChargeDash"]], 
            "expert": [["ChargeDash"]], 
            "master": [["Bash"]]
        }
    },
    "MistyAbove200xp": { 
        "MistyBeforeMiniBoss": {
            "casual": [["Glide"], ["ChargeJump", "DoubleJump"]], 
            "standard": [["Dash", "DoubleJump"], ["Bash", "Grenade"], ["ChargeDash"], ["TripleJump"]], 
            "master": [["Bash"]]
        }
    },
    "MistyBeforeMiniBoss": { 
        "MistyOrbRoom": {
            "casual": [[("KeyStone", 40)], [("MistyKeyStone", 4)]]
        }
    },
    "MistyOrbRoom": { 
        "MistyPreKeystone2": {
            "casual": [["WallJump"], ["Climb"], ["Bash", "Grenade"], ["ChargeJump"]], 
            "master": [["DoubleJump"]]
        }
    },
    "MistyPreKeystone2": {
    }
}