from .bases import OuterWildsTestBase
from ..options import Spawn


class TestGDTowerControl(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "split_translator": True,
    }

    def test_control(self):
        self.assertNotReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)"
        ])
        self.assertReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)", "Imaging Rule"
        ])
        # when Echo Hike is disabled, Threader logic is never created
        self.assertNotReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)", "Threader"
        ])


class TestGDTowerThreaderLogic(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "split_translator": True,
        "enable_eh_mod": True,
    }

    def test_threader(self):
        self.assertNotReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)"
        ])
        # the normal path is still in logic
        self.assertReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)", "Imaging Rule"
        ])
        self.assertReachableWith("GD: Complete the Tower (Text Wall)", [
            "Spacesuit", "Launch Codes", "Translator (Giant's Deep)", "Threader"
        ])


class TestBHFControl(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "split_translator": True,
    }

    def test_control(self):
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Translator (Brittle Hollow)"
        ])
        self.assertReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Launch Codes", "Translator (Brittle Hollow)"
        ])
        # when Echo Hike is disabled, Threader logic is never created
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Translator (Brittle Hollow)", "Threader"
        ])


class TestBHFThreaderLogic(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "split_translator": True,
        "enable_eh_mod": True,
    }

    def test_threader(self):
        self.assertNotReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Translator (Brittle Hollow)"
        ])
        # the normal path is still in logic
        self.assertReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Launch Codes", "Translator (Brittle Hollow)"
        ])
        self.assertReachableWith("BH: Forge (2nd Scroll)", [
            "Spacesuit", "Nomai Warp Codes", "Translator (Brittle Hollow)", "Threader"
        ])


class TestStrangerControl(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_stranger,
    }

    def test_control(self):
        self.assertNotReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit"
        ])
        self.assertReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit", "Stranger Light Modulator"
        ])
        # when Echo Hike is disabled, Threader logic is never created
        self.assertNotReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit", "Threader"
        ])


class TestStrangerThreaderLogic(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": True,
        "spawn": Spawn.option_stranger,
        "enable_eh_mod": True,
    }

    def test_threader(self):
        self.assertNotReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit"
        ])
        # the normal path is still in logic
        self.assertReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit", "Stranger Light Modulator"
        ])
        self.assertReachableWith("EotE: Hidden Gorge Slide Reel", [
            "Spacesuit", "Threader"
        ])


class TestFCLabControl(OuterWildsTestBase):
    options = {
        "enable_fc_mod": True,
        "spawn": Spawn.option_deep_bramble,
        "split_translator": True,
        "logsanity": True,
    }

    def test_control(self):
        self.assertNotReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)"
        ])
        self.assertReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)", "Crystal Repair Manual"
        ])
        # when Echo Hike is disabled, Threader logic is never created
        self.assertNotReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)", "Threader"
        ])


class TestFCLabThreaderLogic(OuterWildsTestBase):
    options = {
        "enable_fc_mod": True,
        "spawn": Spawn.option_deep_bramble,
        "split_translator": True,
        "logsanity": True,
        "enable_eh_mod": True,
    }

    def test_threader(self):
        self.assertNotReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)"
        ])
        # the normal path is still in logic
        self.assertReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)", "Crystal Repair Manual"
        ])
        self.assertReachableWith("FC Ship Log: Eye Signal Lab 1 - Signal", [
            "Spacesuit", "Launch Codes", "Deep Bramble Coordinates", "Signalscope", "Nomai Trailmarkers Frequency", "Geothermal Activity Signal",
            "Thermal Insulation", "Translator (Deep Bramble)", "Threader"
        ])
