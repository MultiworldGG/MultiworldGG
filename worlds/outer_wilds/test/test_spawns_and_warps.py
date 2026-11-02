from .bases import OuterWildsTestBase
from ..options import EarlyKeyItem, Spawn


class TestRandomWarpDeterminism(OuterWildsTestBase):
    options = {
        "randomize_warp_platforms": True,
    }
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)

    def test_determinism(self):
        self.assertListEqual(self.world.warps.mappings, [
            ('SS', 'ATT'),
            ('ATP', 'ET'),
            ('BHF', 'BHT'),
            ('GD', 'THT'),
            ('BHNG', 'WHS'),
            ('ST', 'ETT'),
            ('GDT', 'TH'),
        ])


class TestHGTSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
    }


class TestHGTSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
    }


class TestTHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
    }


class TestTHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "randomize_warp_platforms": True,
    }


class TestGDSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
    }


class TestGDSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
        "randomize_warp_platforms": True,
    }


class TestHGTSpawnRandomWarpEKI(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
        "early_key_item": EarlyKeyItem.option_nomai_warp_codes,
    }


class TestStrangerSpawnSLMEKI(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_stranger,
        "early_key_item": EarlyKeyItem.option_stranger_light_modulator,
    }


class TestRandomNonVanillaSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_random_non_vanilla,
    }


class TestRandomNonVanillaSpawnWithDLC(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_random_non_vanilla,
    }


class TestBHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
    }

    def test_warp_path(self):
        self.assertReachableWith("BH: Riebeck's Surface Campsite Note", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        # on vanilla warps, BH core -> WHS -> BH NH is a closed loop with no way to HCC
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes", "Launch Codes"])


class TestBHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "randomize_warp_platforms": True,
    }


# Regression test: Previously apply_warp_plando() would try to double-delete
# a plando warp that exactly matches a vanilla warp.
class TestBHSpawnPlandoVanillaWarps(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "warp_platform_plando": {
            "SS": "ST",
            "ET": "ETT",
            "ATP": "ATT",
            "TH": "THT",
            "BHNG": "WHS",
            "BHF": "BHT",
            "GD": "GDT",
        },
    }


class TestBHSpawnDirectWarpToHCC(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "warp_platform_plando": {
            "BHNG": "BHT",
            "WHS": "BHF",
            # leave the other warps vanilla
            "SS": "ST",
            "ET": "ETT",
            "ATP": "ATT",
            "TH": "THT",
            "GD": "GDT",
        },
    }

    def test_warp_path(self):
        self.assertReachableWith("BH: Riebeck's Surface Campsite Note", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        # now there is a shipless warp path from BH spawn to HCC
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])


class TestBHSpawnWarpPathToHCC(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "warp_platform_plando": {
            "BHNG": "ATP", # dead end
            "WHS": "BHT", # start of path
            "ATT": "BHF", # end of path (2 warp steps is the longest possible path)
            # leave the other warps vanilla
            "SS": "ST",
            "ET": "ETT",
            "TH": "THT",
            "GD": "GDT",
        },
    }

    def test_warp_path(self):
        self.assertReachableWith("BH: Riebeck's Surface Campsite Note", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        # now there is a shipless warp path from BH spawn to HCC
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])


class TestOtherSpawnWarpPathToHCC(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "warp_platform_plando": {
            "TH": "BHNG",
            "WHS": "BHT",
            "THT": "BHF",
            # leave the other warps vanilla
            "SS": "ST",
            "ET": "ETT",
            "ATP": "ATT",
            "GD": "GDT",
        },
    }

    def test_warp_path(self):
        self.assertReachableWith("TH: Talk to Hornfels", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        # now there is a shipless warp path from spawn to HCC
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])


class TestBHSpawnThreaderWarpPathThroughHCC(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "enable_eh_mod": 1,
        "warp_platform_plando": {
            "BHF": "SS", # would be an illegal dead end pair without EH
            "BHT": "ST",
            # leave the rest vanilla
            "ET": "ETT",
            "ATP": "ATT",
            "TH": "THT",
            "BHNG": "WHS",
            "GD": "GDT",
        },
    }

    def test_warp_path(self):
        self.assertReachableWith("BH: Riebeck's Surface Campsite Note", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])
        # this time the Forge is reachable directly with Threader
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Threader"])  # ignoring Spacesuit since it's precollected

        # and the HCC/BHF warp is no longer a dead end, so it can be used to reach another dead end
        self.assertNotReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Threader"])
        self.assertNotReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Nomai Warp Codes"])
        self.assertReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Threader", "Nomai Warp Codes"])


class TestVanillaSpawnThreaderWarpPathThroughHCC(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_vanilla,
        "shuffle_spacesuit": True,
        "enable_eh_mod": 1,
        "warp_platform_plando": {
            "TH": "BHNG",
            "BHF": "SS", # would be an illegal dead end pair without EH
            "BHT": "ST",
            "THT": "WHS",
            # leave the rest vanilla
            "ET": "ETT",
            "ATP": "ATT",
            "GD": "GDT",
        },
    }

    def test_warp_path(self):
        self.assertReachableWith("TH: Talk to Hornfels", [])

        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator"])
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Nomai Warp Codes"])
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Spacesuit"])
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Threader"])
        # this time the Forge is reachable directly with Threader *and* Spacesuit is explicitly required
        self.assertReachableWith("BH: Forge (2nd Scroll)", ["Translator", "Spacesuit", "Threader"])

        # and the HCC/BHF warp is no longer a dead end, so it can be used to reach another dead end
        self.assertNotReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Threader"])
        self.assertNotReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Nomai Warp Codes"])
        # due to Launch Codes being locked on vanilla spawn the Ship & Warps path is still available, so asserting on the final location is not meaningful
        self.assertReachableWith("Sun Station (Projection Stone Text)", ["Translator", "Spacesuit", "Nomai Warp Codes"])
        # instead we settle for asserting on the HCC regions
        self.assertRegionNotReachableWith("Raise Forge then HCC via Threader", ["Threader"])
        self.assertRegionNotReachableWith("Raise Forge then HCC via Threader", ["Spacesuit"])
        self.assertRegionReachableWith("Raise Forge then HCC via Threader", ["Spacesuit", "Threader"])
        self.assertRegionNotReachableWith("Raise Forge then HCC via Ship & Warps", ["Spacesuit", "Threader"])
        self.assertRaises(KeyError, lambda: self.multiworld.get_region("Raise Forge then HCC via Warps Only", self.player)) # region not created since there's no warp-only path

