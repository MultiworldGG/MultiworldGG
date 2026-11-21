from .bases import NineSolsTestBase


class TestERFixedSeed(NineSolsTestBase):
    options = {
        "randomize_entrances": True,
    }
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)

    def test_default(self):
        pass


class TestUncoupledERFixedSeed(NineSolsTestBase):
    options = {
        "randomize_entrances": True,
        "coupled_entrances": False,
    }
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)

    def test_default(self):
        pass

# GER has proven too unreliable to test without a fixed seed.

# class TestER(NineSolsTestBase):
#     options = {
#         "randomize_entrances": True,
#     }
#
#     def test_default(self):
#         pass
#
#
# class TestUncoupledER(NineSolsTestBase):
#     options = {
#         "randomize_entrances": True,
#         "coupled_entrances": False,
#     }
#
#     def test_default(self):
#         pass

