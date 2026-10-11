from .Addresses import RAM, NTSCU11RAM, NTSCU10RAM
#from .Enums import LevelInGameIDs

class LevelData:
    Name = ""
    OrbCount = 0
    LevelId = 0
    HasTalisman = False
    IsBoss = False
    MoneybagsAddresses = []
    SkillPointAddresses = []
    LifeBottleAddresses = []
    SpiritParticles = 0
    GemMaskAddress = 0x0
    TotalGemCount = 0
    GemSkipIndices = []

    def __init__(
        self,
        name,
        level_id,
        orb_count,
        has_talisman,
        is_boss,
        moneybags_addresses,
        skill_point_addresses,
        life_bottle_addresses,
        spirit_particles,
        gem_mask_address = 0x0,
        total_gem_count = 0,
        gem_skip_indices = None
    ):
        self.Name = name
        self.OrbCount = orb_count
        self.LevelId = level_id
        self.HasTalisman = has_talisman
        self.IsBoss = is_boss
        self.MoneybagsAddresses = moneybags_addresses
        self.SkillPointAddresses = skill_point_addresses
        self.LifeBottleAddresses = life_bottle_addresses
        self.SpiritParticles = spirit_particles
        self.GemMaskAddress = gem_mask_address
        self.TotalGemCount = total_gem_count
        if gem_skip_indices is None:
            gem_skip_indices = []
        self.GemSkipIndices = gem_skip_indices

def GetLevelData():
    return [
        LevelData(
            "Summer Forest",
            LevelInGameIDs.SummerForest,
            4,
            False,
            False,
            [RAM.SwimUnlock, RAM.WallToAquariaUnlock],
            [],
            [RAM.SummerLifeBottle1Address, RAM.SummerLifeBottle2Address, RAM.SummerLifeBottle3Address],
            0,
            RAM.SummerGemMask,
            138,
            [27, 41, 42, 43, 44, 45, 46, 47, 61, 62, 63, 72, 73, 81, 82, 95, 96, 97, 98, 99, 100, 108, 126, 127, 128]
        ),
        # Removed Moneybags as a location in Glimmer because it leads to an overly restrictive start.
        LevelData("Glimmer", LevelInGameIDs.Glimmer, 3, True, False, [], [], [], 14, RAM.GlimmerGemMask, 133, [1, 2, 3, 4, 5, 6, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 152]),
        LevelData("Idol Springs", LevelInGameIDs.IdolSprings, 2, True, False, [], [RAM.IdolTikiSkillPoint], [RAM.IdolLifeBottleAddress], 11, RAM.IdolGemMask, 149, [63, 88, 90, 122, 127, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145]),
        LevelData("Colossus", LevelInGameIDs.Colossus, 3, True, False, [], [RAM.ColossusHockeySkillPoint], [RAM.ColossusLifeBottleAddress], 13, RAM.ColossusGemMask, 137, [1, 2, 3, 4, 5, 6, 7, 25, 32, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 71, 117, 118, 119, 127, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178]),
        LevelData("Hurricos", LevelInGameIDs.Hurricos, 3, True, False, [], [RAM.HurricosWindmillSkillPoint], [RAM.HurricosLifeBottleAddress], 22, RAM.HurricosGemMask, 114, [42, 43, 44, 45, 46, 83, 85, 86, 87, 94, 116, 123, 126, 127, 128, 129, 130, 131]),
        LevelData("Aquaria Towers", LevelInGameIDs.AquariaTowers, 3, True, False, [RAM.AquariaSubUnlock], [RAM.AquariaSeaweedSkillPoint], [RAM.AquariaLifeBottleAddress], 29, RAM.AquariaGemMask, 137, [85, 86, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 109, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 167]),
        LevelData("Sunny Beach", LevelInGameIDs.SunnyBeach, 3, True, False, [], [], [], 17, RAM.SunnyGemMask, 118, [1, 2, 3, 4, 5, 6, 53, 91, 105, 106, 107, 109]),
        LevelData("Ocean Speedway", LevelInGameIDs.OceanSpeedway, 1, False, False, [], [RAM.OceanTimeAttackSkillPoint], [], 0),
        LevelData("Crush's Dungeon", LevelInGameIDs.CrushsDungeon, 0, False, True, [], [RAM.CrushPerfectSkillPoint], [], 0),
        LevelData("Autumn Plains", LevelInGameIDs.AutumnPlains, 2, False, False, [RAM.ZephyrPortalUnlock, RAM.ClimbUnlock, RAM.ShadyPortalUnlock, RAM.IcyPortalUnlock], [], [RAM.AutumnLifeBottleAddress], 0, RAM.AutumnGemMask, 106, [1, 2, 3, 4, 5, 6, 102, 103, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133]),
        LevelData("Skelos Badlands", LevelInGameIDs.SkelosBadlands, 3, True, False, [], [RAM.SkelosCactiSkillPoint, RAM.SkelosCatbatSkillPoint], [RAM.SkelosLifeBottleAddress], 28, RAM.SkelosGemMask, 95, [1, 2, 3, 48, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 138, 139, 140, 141, 142, 143, 144, 155, 156, 157, 158, 159, 160, 161]),
        LevelData("Crystal Glacier", LevelInGameIDs.CrystalGlacier, 2, True, False, [RAM.CrystalBridgeUnlock], [], [RAM.CrystalLifeBottleAddress], 38, RAM.CrystalGemMask, 105, [1, 2, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]),
        LevelData("Breeze Harbor", LevelInGameIDs.BreezeHarbor, 2, True, False, [], [], [RAM.BreezeLifeBottle1Address, RAM.BreezeLifeBottle2Address], 16, RAM.BreezeGemMask, 97, [1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 18, 19, 85, 90, 100, 111, 112]),
        LevelData("Zephyr", LevelInGameIDs.Zephyr, 4, True, False, [], [], [RAM.ZephyrLifeBottleAddress], 30, RAM.ZephyrGemMask, 135, [1, 2, 8, 9, 10, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 105, 107, 117, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 149, 150, 151, 153, 167, 168]),
        LevelData("Metro Speedway", LevelInGameIDs.MetroSpeedway, 1, False, False, [], [RAM.MetroTimeAttackSkillPoint], [], 0),
        LevelData("Scorch", LevelInGameIDs.Scorch, 2, True, False, [], [RAM.ScorchTreesSkillPoint], [RAM.ScorchLifeBottleAddress], 28, RAM.ScorchGemMask, 125, [1, 2, 3, 4, 5, 93, 94, 95, 96, 97, 98, 99, 100, 101, 106, 115, 134, 135, 136, 137, 142, 143, 144, 148]),
        LevelData("Shady Oasis", LevelInGameIDs.ShadyOasis, 2, True, False, [], [], [RAM.ShadyLifeBottleAddress], 21, RAM.ShadyGemMask, 119, [1, 2, 3, 4, 5, 6, 7, 28, 29, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 138, 140, 141, 142, 143, 148, 155, 168, 169]),
        LevelData("Magma Cone", LevelInGameIDs.MagmaCone, 3, True, False, [RAM.MagmaElevatorUnlock], [], [RAM.MagmaLifeBottle1Address, RAM.MagmaLifeBottle2Address, RAM.MagmaLifeBottle3Address, RAM.MagmaLifeBottle4Address], 19, RAM.MagmaGemMask, 119, [1, 2, 48, 78, 121, 122, 123]),
        LevelData("Fracture Hills", LevelInGameIDs.FractureHills, 3, True, False, [], [RAM.FractureSuperchargeSkillPoint], [RAM.FractureLifeBottleAddress], 29, RAM.FractureGemMask, 115, [1, 2, 3, 20, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91]),
        LevelData("Icy Speedway", LevelInGameIDs.IcySpeedway, 1, False, False, [], [RAM.IcyTimeAttackSkillPoint], [], 0),
        LevelData("Gulp's Overlook", LevelInGameIDs.GulpsOverlook, 0, False, True, [], [RAM.GulpPerfectSkillPoint, RAM.GulpRiptoSkillPoint], [], 0),
        LevelData("Winter Tundra", LevelInGameIDs.WinterTundra, 3, False, False, [RAM.CanyonPortalUnlock, RAM.HeadbashUnlock], [], [], 0, RAM.WinterGemMask, 101, [1, 2, 3, 4, 5, 6, 7, 13, 14, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]),
        LevelData("Mystic Marsh", LevelInGameIDs.MysticMarsh, 3, False, False, [], [], [RAM.MysticLifeBottle1Address, RAM.MysticLifeBottle2Address], 36, RAM.MysticGemMask, 139, [1, 112, 113, 114, 115, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157]),
        LevelData("Cloud Temples", LevelInGameIDs.CloudTemples, 3, False, False, [], [], [RAM.CloudLifeBottleAddress], 23, RAM.CloudGemMask, 111, [1, 34, 54, 55, 101, 102, 103]),
        LevelData("Canyon Speedway", LevelInGameIDs.CanyonSpeedway, 1, False, False, [], [RAM.CanyonTimeAttackSkillPoint], [], 0),
        LevelData("Robotica Farms", LevelInGameIDs.RoboticaFarms, 3, False, False, [], [], [], 20, RAM.RoboticaGemMask, 127, [1, 2, 3, 4, 5, 6, 7, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 130, 138, 139, 147, 148, 149, 150, 151, 152, 179, 180, 181, 182, 183]),
        LevelData("Metropolis", LevelInGameIDs.Metropolis, 4, False, False, [], [], [], 22, RAM.MetropolisGemMask, 126, [38, 45, 65, 91, 97, 105, 129, 130, 131, 132]),
        LevelData("Dragon Shores", LevelInGameIDs.DragonShores, 0, False, False, [], [], [], 0),
        LevelData("Ripto's Arena", LevelInGameIDs.RiptosArena, 0, False, True, [], [RAM.RiptoPerfectSkillPoint], [], 0),
    ]
